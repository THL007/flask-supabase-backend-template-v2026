"""Marshmallow schemas for API validation."""
from marshmallow import Schema, fields, validate


class HealthSchema(Schema):
    """Health check schema."""
    pass


class HealthResponseSchema(Schema):
    """Health check response schema."""
    status = fields.Str(required=True)
    version = fields.Str(required=True)
    service = fields.Str(required=True)


class ErrorSchema(Schema):
    """Error response schema."""
    error = fields.Str(required=True)
    message = fields.Str(required=False)

