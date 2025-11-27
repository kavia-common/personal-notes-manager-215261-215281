from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Dict, Any


def _now_iso() -> str:
    """Return current UTC time as ISO8601 string with 'Z' suffix."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# PUBLIC_INTERFACE
@dataclass
class Note:
    """Represents a note entity for the in-memory store.

    Attributes:
        id: Unique integer identifier.
        title: Title of the note.
        content: Body content of the note.
        created_at: ISO8601 timestamp when the note was created (UTC).
        updated_at: ISO8601 timestamp when the note was last updated (UTC).
        archived: Whether the note is archived.
    """
    id: int
    title: str
    content: str
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    archived: bool = False

    # PUBLIC_INTERFACE
    def to_dict(self) -> Dict[str, Any]:
        """Serialize the Note to a plain dict suitable for JSON responses."""
        return asdict(self)

    # PUBLIC_INTERFACE
    @staticmethod
    def from_payload(id_: int, payload: Dict[str, Any]) -> "Note":
        """Create a Note from an incoming payload and provided id.

        This initializes timestamps to now and archived to False by default.
        """
        title = str(payload.get("title", "")).strip()
        content = str(payload.get("content", "")).strip()
        return Note(id=id_, title=title, content=content)
