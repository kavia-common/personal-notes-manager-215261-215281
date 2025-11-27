from __future__ import annotations

from threading import Lock
from typing import Dict, List, Optional, Any

from .models import Note, _now_iso


class InMemoryNotesRepository:
    """Thread-safe in-memory repository for managing Note entities.

    This repository auto-manages incremental IDs and ISO8601 timestamps.
    """

    def __init__(self) -> None:
        self._lock = Lock()
        self._notes: Dict[int, Note] = {}
        self._next_id: int = 1

    # PUBLIC_INTERFACE
    def list(self, q: Optional[str] = None, include_archived: bool = False) -> List[Dict[str, Any]]:
        """List notes with optional text query and archive filtering.

        Args:
            q: Optional text to match in title or content (case-insensitive).
            include_archived: If False, archived notes are excluded.

        Returns:
            A list of note dictionaries sorted by updated_at descending.
        """
        with self._lock:
            notes = list(self._notes.values())

            if not include_archived:
                notes = [n for n in notes if not n.archived]

            if q:
                q_lower = q.lower()
                notes = [
                    n for n in notes
                    if q_lower in n.title.lower() or q_lower in n.content.lower()
                ]

            # Sort by updated_at descending (newest first)
            notes.sort(key=lambda n: n.updated_at, reverse=True)
            return [n.to_dict() for n in notes]

    # PUBLIC_INTERFACE
    def get(self, id_: int) -> Optional[Dict[str, Any]]:
        """Get a single note by ID.

        Args:
            id_: The note ID.

        Returns:
            The note dict if found, otherwise None.
        """
        with self._lock:
            note = self._notes.get(id_)
            return note.to_dict() if note else None

    # PUBLIC_INTERFACE
    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new note.

        Args:
            payload: Dict with 'title' and 'content' as strings.

        Returns:
            The created note as a dict.
        """
        title = str(payload.get("title", "")).strip()
        content = str(payload.get("content", "")).strip()

        if title == "" and content == "":
            # Ensure at least some content
            title = "Untitled"

        with self._lock:
            new_id = self._next_id
            self._next_id += 1
            note = Note.from_payload(new_id, {"title": title, "content": content})
            self._notes[new_id] = note
            return note.to_dict()

    # PUBLIC_INTERFACE
    def update(self, id_: int, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing note.

        Args:
            id_: The note ID.
            payload: Dict with optional 'title', 'content', 'archived' fields.

        Returns:
            The updated note dict if found, otherwise None.
        """
        with self._lock:
            note = self._notes.get(id_)
            if not note:
                return None

            if "title" in payload and payload["title"] is not None:
                note.title = str(payload["title"]).strip()
            if "content" in payload and payload["content"] is not None:
                note.content = str(payload["content"]).strip()
            if "archived" in payload and payload["archived"] is not None:
                note.archived = bool(payload["archived"])

            note.updated_at = _now_iso()
            self._notes[id_] = note
            return note.to_dict()

    # PUBLIC_INTERFACE
    def delete(self, id_: int) -> bool:
        """Delete a note by ID.

        Args:
            id_: The note ID.

        Returns:
            True if a note was deleted, False otherwise.
        """
        with self._lock:
            return self._notes.pop(id_, None) is not None


# Expose a singleton repository instance for easy import by routes
# PUBLIC_INTERFACE
notes_repo = InMemoryNotesRepository()
"""A process-wide, thread-safe singleton repository for notes."""
