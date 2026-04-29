import csv
import json
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any

from sqlalchemy import event, inspect
from sqlalchemy.orm import Mapper

from app.core.config import settings


_CSV_HEADERS = [
    "timestamp",
    "operation",
    "model",
    "entity_id",
    "table_name",
    "source",
    "payload_json",
]

_lock = Lock()
_initialized = False
_registered = False


def _ensure_csv_file() -> Path:
    global _initialized

    csv_path = Path(settings.CRUD_AUDIT_CSV_PATH)
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


def _extract_entity_id(mapper: Mapper, target: Any) -> str:
    values: list[str] = []

    for pk_column in mapper.primary_key:
        pk_name = pk_column.key
        pk_value = getattr(target, pk_name, None)
        values.append(str(pk_value))

    return "|".join(values) if values else ""


def _extract_row_data(mapper: Mapper, target: Any) -> dict[str, Any]:
    row_data: dict[str, Any] = {}

    for column in mapper.columns:
        row_data[column.key] = _safe_serialize(getattr(target, column.key, None))

    return row_data


def _extract_changed_fields(target: Any) -> dict[str, dict[str, Any]]:
    changed: dict[str, dict[str, Any]] = {}
    state = inspect(target)

    for attr in state.attrs:
        history = attr.history
        if not history.has_changes():
            continue

        old_value = history.deleted[0] if history.deleted else None
        new_value = history.added[0] if history.added else getattr(target, attr.key, None)
        changed[attr.key] = {
            "old": _safe_serialize(old_value),
            "new": _safe_serialize(new_value),
        }

    return changed


def _write_csv_row(operation: str, model: str, entity_id: str, table_name: str, source: str, payload: dict[str, Any]) -> None:
    if not settings.CRUD_AUDIT_ENABLED:
        return

    csv_path = _ensure_csv_file()
    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "operation": operation,
        "model": model,
        "entity_id": entity_id,
        "table_name": table_name,
        "source": source,
        "payload_json": json.dumps(payload, ensure_ascii=False, default=str),
    }

    with _lock:
        with csv_path.open("a", newline="", encoding="utf-8") as file_obj:
            writer = csv.DictWriter(file_obj, fieldnames=_CSV_HEADERS)
            writer.writerow(row)


def _extract_models_from_statement(statement: Any) -> list[str]:
    try:
        column_descriptions = getattr(statement, "column_descriptions", []) or []
        model_names = []

        for description in column_descriptions:
            entity = description.get("entity")
            if entity is None:
                continue
            model_names.append(entity.__name__)

        return model_names
    except Exception:
        return []


def register_csv_audit_listeners(session_cls: Any, base_cls: Any) -> None:
    global _registered

    if _registered or not settings.CRUD_AUDIT_ENABLED:
        return

    _ensure_csv_file()

    @event.listens_for(base_cls, "after_insert", propagate=True)
    def _after_insert(mapper: Mapper, connection: Any, target: Any) -> None:
        try:
            _write_csv_row(
                operation="CREATE",
                model=target.__class__.__name__,
                entity_id=_extract_entity_id(mapper, target),
                table_name=mapper.local_table.name,
                source="sqlalchemy_mapper_event",
                payload={"new_values": _extract_row_data(mapper, target)},
            )
        except Exception:
            return

    @event.listens_for(base_cls, "after_update", propagate=True)
    def _after_update(mapper: Mapper, connection: Any, target: Any) -> None:
        try:
            _write_csv_row(
                operation="UPDATE",
                model=target.__class__.__name__,
                entity_id=_extract_entity_id(mapper, target),
                table_name=mapper.local_table.name,
                source="sqlalchemy_mapper_event",
                payload={
                    "changed_fields": _extract_changed_fields(target),
                    "current_values": _extract_row_data(mapper, target),
                },
            )
        except Exception:
            return

    @event.listens_for(base_cls, "after_delete", propagate=True)
    def _after_delete(mapper: Mapper, connection: Any, target: Any) -> None:
        try:
            _write_csv_row(
                operation="DELETE",
                model=target.__class__.__name__,
                entity_id=_extract_entity_id(mapper, target),
                table_name=mapper.local_table.name,
                source="sqlalchemy_mapper_event",
                payload={"old_values": _extract_row_data(mapper, target)},
            )
        except Exception:
            return

    @event.listens_for(session_cls, "do_orm_execute")
    def _do_orm_execute(orm_execute_state: Any) -> None:
        try:
            if not orm_execute_state.is_select:
                return
            if orm_execute_state.is_column_load or orm_execute_state.is_relationship_load:
                return

            statement_text = str(orm_execute_state.statement)
            if len(statement_text) > 1200:
                statement_text = f"{statement_text[:1200]}..."

            model_names = _extract_models_from_statement(orm_execute_state.statement)
            if not model_names:
                model_names = ["Unknown"]

            for model_name in model_names:
                _write_csv_row(
                    operation="READ",
                    model=model_name,
                    entity_id="",
                    table_name="",
                    source="sqlalchemy_session_event",
                    payload={"statement": statement_text},
                )
        except Exception:
            return

    _registered = True
