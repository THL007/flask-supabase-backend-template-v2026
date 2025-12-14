"""Helper utility functions."""
from datetime import datetime
from typing import Any, Dict


def format_datetime(dt: datetime | str) -> str:
    """Format datetime to ISO string."""
    if isinstance(dt, str):
        return dt
    return dt.isoformat() if dt else None


def sanitize_dict(data: Dict[str, Any], allowed_keys: list = None) -> Dict[str, Any]:
    """Sanitize dictionary to only include allowed keys."""
    if allowed_keys is None:
        return data
    return {k: v for k, v in data.items() if k in allowed_keys}


def paginate_query(query, page: int = 1, per_page: int = 10):
    """Paginate a SQLAlchemy query."""
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    return {
        "items": [item.to_dict() if hasattr(item, "to_dict") else item for item in pagination.items],
        "total": pagination.total,
        "page": page,
        "per_page": per_page,
        "pages": pagination.pages,
    }

