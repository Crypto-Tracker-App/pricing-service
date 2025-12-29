import dataclasses
from typing import Any


def to_jsonable(obj: Any) -> Any:
    """Recursively convert dataclass, pydantic and SDK objects to JSON-serializable primitives.
    - Dataclasses -> dict
    - Pydantic v2 -> model_dump()
    - Pydantic v1 -> dict()
    - Objects with to_dict() -> dict
    - Lists/Tuples/Sets -> list
    - Dicts -> dict with converted values
    - Primitive types passed through
    """
    try:
        if obj is None:
            return None
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        if hasattr(obj, "model_dump") and callable(obj.model_dump):  # Pydantic v2
            return obj.model_dump()
        if hasattr(obj, "dict") and callable(obj.dict):  # Pydantic v1
            return obj.dict()
        if hasattr(obj, "to_dict") and callable(obj.to_dict):
            return obj.to_dict()
        if isinstance(obj, (list, tuple, set)):
            return [to_jsonable(x) for x in obj]
        if isinstance(obj, dict):
            return {k: to_jsonable(v) for k, v in obj.items()}
        # Fallback: try basic types; if not serializable, cast to string
        if isinstance(obj, (str, int, float, bool)):
            return obj
        return str(obj)
    except Exception:
        # Last resort fallback to string to avoid breaking responses
        return str(obj)
