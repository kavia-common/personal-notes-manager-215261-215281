from __future__ import annotations

from flask_smorest import Blueprint, abort
from flask.views import MethodView

from ..schemas import NoteCreateSchema, NoteUpdateSchema, NoteSchema, NotesListQuerySchema
from ..storage import notes_repo

blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/api/notes",
    description="CRUD operations for personal notes",
)


@blp.route("/")
class NotesCollection(MethodView):
    """Collection endpoints for notes."""
    # PUBLIC_INTERFACE
    @blp.arguments(NotesListQuerySchema, location="query")
    @blp.response(200, NoteSchema(many=True))
    def get(self, args):
        """List notes with optional filtering.
        ---
        summary: List notes
        description: Returns a list of notes, optionally filtered by text query and archive inclusion.
        """
        q = args.get("q")
        include_archived = bool(args.get("include_archived")) if args.get("include_archived") is not None else False
        notes = notes_repo.list(q=q, include_archived=include_archived)
        return notes

    # PUBLIC_INTERFACE
    @blp.arguments(NoteCreateSchema)
    @blp.response(201, NoteSchema)
    def post(self, payload):
        """Create a new note.
        ---
        summary: Create note
        description: Creates a new note with an optional title and content.
        """
        created = notes_repo.create(payload or {})
        return created


@blp.route("/<int:note_id>")
class NoteItem(MethodView):
    """Item endpoints for a specific note."""
    # PUBLIC_INTERFACE
    @blp.response(200, NoteSchema)
    def get(self, note_id: int):
        """Get a specific note by ID.
        ---
        summary: Get note
        description: Returns a single note by ID.
        """
        note = notes_repo.get(note_id)
        if not note:
            abort(404, message="Note not found")
        return note

    # PUBLIC_INTERFACE
    @blp.arguments(NoteUpdateSchema)
    @blp.response(200, NoteSchema)
    def patch(self, payload, note_id: int):
        """Update a note by ID.
        ---
        summary: Update note
        description: Partially updates a note's fields.
        """
        updated = notes_repo.update(note_id, payload or {})
        if not updated:
            abort(404, message="Note not found")
        return updated

    # PUBLIC_INTERFACE
    @blp.response(204)
    def delete(self, note_id: int):
        """Delete a note by ID.
        ---
        summary: Delete note
        description: Deletes a note. Returns no content on success.
        """
        success = notes_repo.delete(note_id)
        if not success:
            abort(404, message="Note not found")
        return ""
