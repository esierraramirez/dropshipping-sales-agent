import csv
import json
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any, Optional

from fastapi import Request, Response
from jose import JWTError, jwt

from app.core.config import settings


_CSV_HEADERS = [
    "timestamp",
    "method",
    "path",
    "status_code",
    "duration_ms",
    "endpoint",
    "vendor_id",
    "user_email",
    "query_params",
    "source",
    "payload_json",
]

_lock = Lock()
_initialized = False

_SENSITIVE_KEYS = {
    "password",
    "password_hash",
    "access_token",
    "refresh_token",
    "token",
    "verify_token",
    "jwt",
    "secret",
    "authorization",
}


def _ensure_csv_file() -> Path:
    global _initialized

    csv_path = Path(settings.ENDPOINT_AUDIT_CSV_PATH)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    if _initialized:
        return csv_path

    with _lock:
        if _initialized:
            return csv_path

        if not csv_path.exists() or csv_path.stat().st_size == 0:
            with csv_path.open("w", newline="", encoding="utf-8") as file_obj:
                writer = csv.DictWriter(file_obj, fieldnames=_CSV_HEADERS)
                writer.writeheader()

        _initialized = True

    return csv_path


def _safe_serialize(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()

    try:
        json.dumps(value)
        return value
    except TypeError:
        return str(value)


def _redact_value(key: str, value: Any) -> Any:
    normalized_key = key.lower()
    if any(sensitive in normalized_key for sensitive in _SENSITIVE_KEYS):
        return "[REDACTED]"

    if isinstance(value, dict):
        return {nested_key: _redact_value(nested_key, nested_value) for nested_key, nested_value in value.items()}

    if isinstance(value, list):
        return [_redact_value(key, item) for item in value]

    return _safe_serialize(value)


def _sanitize_query_params(query_params: dict[str, Any]) -> dict[str, Any]:
    return {key: _redact_value(key, value) for key, value in query_params.items()}


def _sanitize_json_body(body_text: str) -> dict[str, Any]:
    try:
        parsed = json.loads(body_text)
    except Exception:
        return {
            "body_type": "non_json",
            "body_length": len(body_text),
        }

    if isinstance(parsed, dict):
        return {
            "body_type": "json",
            "body": {key: _redact_value(key, value) for key, value in parsed.items()},
        }

    if isinstance(parsed, list):
        return {
            "body_type": "json",
            "body": [_safe_serialize(item) for item in parsed],
        }

    return {
        "body_type": "json",
        "body": _safe_serialize(parsed),
    }


def _extract_vendor_context(request: Request) -> tuple[Optional[int], Optional[str]]:
    authorization = request.headers.get("authorization")
    if not authorization or not authorization.startswith("Bearer "):
        return None, None

    token = authorization.replace("Bearer ", "").strip()

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        vendor_id = payload.get("sub")
        email = payload.get("email")
        return int(vendor_id) if vendor_id is not None else None, str(email) if email is not None else None
    except (JWTError, ValueError, TypeError):
        return None, None


def _write_csv_row(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    endpoint: str,
    vendor_id: Optional[int],
    user_email: Optional[str],
    query_params: dict[str, Any],
    payload: dict[str, Any],
) -> None:
    if not settings.ENDPOINT_AUDIT_ENABLED:
        return

    csv_path = _ensure_csv_file()
    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": method,
        "path": path,
        "status_code": status_code,
        "duration_ms": round(duration_ms, 2),
        "endpoint": endpoint,
        "vendor_id": vendor_id if vendor_id is not None else "",
        "user_email": user_email or "",
        "query_params": json.dumps(query_params, ensure_ascii=False, default=str),
        "source": "fastapi_middleware",
        "payload_json": json.dumps(payload, ensure_ascii=False, default=str),
    }

    with _lock:
        with csv_path.open("a", newline="", encoding="utf-8") as file_obj:
            writer = csv.DictWriter(file_obj, fieldnames=_CSV_HEADERS)
            writer.writerow(row)


async def endpoint_csv_audit_middleware(request: Request, call_next):
    start = datetime.utcnow()
    status_code = 500
    response_payload: dict[str, Any] = {}

    body_text = ""
    try:
        body_bytes = await request.body()
        if body_bytes:
            body_text = body_bytes.decode("utf-8", errors="replace")
    except Exception:
        body_text = ""

    try:
        response: Response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        duration_ms = (datetime.utcnow() - start).total_seconds() * 1000.0
        vendor_id, user_email = _extract_vendor_context(request)
        endpoint_name = request.scope.get("endpoint")
        endpoint_label = getattr(endpoint_name, "__name__", "unknown_endpoint") if endpoint_name else "unknown_endpoint"

        query_params = _sanitize_query_params(dict(request.query_params))
        if body_text:
            response_payload = _sanitize_json_body(body_text)

        try:
            _write_csv_row(
                method=request.method,
                path=request.url.path,
                status_code=status_code,
                duration_ms=duration_ms,
                endpoint=endpoint_label,
                vendor_id=vendor_id,
                user_email=user_email,
                query_params=query_params,
                payload=response_payload,
            )
        except Exception:
            return