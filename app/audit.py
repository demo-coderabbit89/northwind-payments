"""Audit trail. Every money movement must be recorded here (SOX control NW-AUD-01)."""
import json
import sqlite3


def record(conn: sqlite3.Connection, actor_id: int, action: str, entity: str,
           entity_id: int, detail: dict | None = None) -> None:
    conn.execute(
        "INSERT INTO audit_log (actor_id, action, entity, entity_id, detail) VALUES (?, ?, ?, ?, ?)",
        (actor_id, action, entity, entity_id, json.dumps(detail or {})),
    )
