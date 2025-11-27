from __future__ import annotations

from marshmallow import Schema, fields, validate


# PUBLIC_INTERFACE
class NoteCreateSchema(Schema):
    """Schema for creating a note."""
    title = fields.String(required=False, allow_none=True, validate=validate.Length(max=500), description="Title of the note")
    content = fields.String(required=False, allow_none=True, description="Content/body of the note")


# PUBLIC_INTERFACE
class NoteUpdateSchema(Schema):
    """Schema for updating a note (partial)."""
    title = fields.String(required=False, allow_none=True, validate=validate.Length(max=500), description="Title of the note")
    content = fields.String(required=False, allow_none=True, description="Content/body of the note")
    archived = fields.Boolean(required=False, allow_none=True, description="Archive state")


# PUBLIC_INTERFACE
class NoteSchema(Schema):
    """Schema representing a Note entity returned from the API."""
    id = fields.Integer(required=True, description="Unique note ID")
    title = fields.String(required=True, description="Title of the note")
    content = fields.String(required=True, description="Content/body of the note")
    created_at = fields.String(required=True, description="ISO8601 timestamp when created (UTC)")
    updated_at = fields.String(required=True, description="ISO8601 timestamp when last updated (UTC)")
    archived = fields.Boolean(required=True, description="Whether the note is archived")


# PUBLIC_INTERFACE
class NotesListQuerySchema(Schema):
    """Query parameters for listing notes."""
    q = fields.String(required=False, allow_none=True, description="Search query to match in title or content")
    include_archived = fields.Boolean(required=False, missing=False, description="Whether to include archived notes")
