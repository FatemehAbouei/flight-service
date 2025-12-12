# app/repos/flight_repo.py
from app.db.database import execute, fetchall, fetchone
import json
from typing import Dict, Any, Tuple, Optional, List

ALLOWED_SORT_COLUMNS = {
    "flight_id","flight_number","origin","destination","departure_time","arrival_time",
    "duration_minutes","aircraft_type","seats_total","seats_available","status","created_at","updated_at"
}

def insert_flight(data: Dict[str, Any]) -> int:
    q = """
    INSERT INTO flights (
      flight_id, flight_number, origin, destination,
      departure_time, arrival_time, duration_minutes, aircraft_type,
      seats_total, seats_available, status, created_at, updated_at, process_id
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    params = (
        data.get("flight_id"),
        data.get("flight_number"),
        data.get("origin"),
        data.get("destination"),
        data.get("departure_time"),
        data.get("arrival_time"),
        data.get("duration_minutes"),
        data.get("aircraft_type"),
        data.get("seats_total"),
        data.get("seats_available"),
        data.get("status"),
        data.get("created_at"),
        data.get("updated_at"),
        data.get("process_id"),
    )
    return execute(q, params, commit=True)

def _build_filters(params: Dict[str, Any]) -> Tuple[str, Tuple]:
    filters = []
    vals = []
    if params.get("origin"):
        filters.append("origin = %s"); vals.append(params["origin"])
    if params.get("destination"):
        filters.append("destination = %s"); vals.append(params["destination"])
    if params.get("status"):
        filters.append("status = %s"); vals.append(params["status"])
    if params.get("aircraft_type"):
        filters.append("aircraft_type = %s"); vals.append(params["aircraft_type"])
    if params.get("departure_from"):
        filters.append("departure_time >= %s"); vals.append(params["departure_from"])
    if params.get("departure_to"):
        filters.append("departure_time <= %s"); vals.append(params["departure_to"])
    where = ("WHERE " + " AND ".join(filters)) if filters else ""
    return where, tuple(vals)

def get_flights(params: Dict[str, Any], page: int =1, size: int =20, sort_by: str="departure_time", order: str="asc") -> List[Dict]:
    if sort_by not in ALLOWED_SORT_COLUMNS:
        sort_by = "departure_time"
    order = order.lower()
    if order not in ("asc","desc"):
        order = "asc"
    where_clause, vals = _build_filters(params)
    offset = (page - 1) * size
    q = f"SELECT * FROM flights {where_clause} ORDER BY {sort_by} {order} LIMIT %s OFFSET %s"
    params = tuple(vals) + (size, offset)
    rows = fetchall(q, params)
    return rows

def count_flights(params: Dict[str, Any]) -> int:
    where_clause, vals = _build_filters(params)
    q = f"SELECT COUNT(*) as cnt FROM flights {where_clause}"
    row = fetchone(q, tuple(vals))
    return row["cnt"] if row else 0

def get_flight_by_id(fid: int) -> Optional[Dict]:
    return fetchone("SELECT * FROM flights WHERE flight_id = %s", (fid,))

def update_flight(fid: int, changes: Dict[str, Any]) -> int:
    keys = []
    vals = []
    for k,v in changes.items():
        keys.append(f"{k} = %s")
        vals.append(v)
    if not keys:
        return 0
    vals.append(fid)
    q = f"UPDATE flights SET {', '.join(keys)} WHERE flight_id = %s"
    return execute(q, tuple(vals), commit=True)

def delete_flight(fid: int) -> int:
    return execute("DELETE FROM flights WHERE flight_id = %s", (fid,), commit=True)

def insert_flight_log(flight_id: int, previous_state: Dict, new_state: Dict, note: str = "") -> int:
    q = "INSERT INTO flight_logs (flight_id, previous_state, new_state, note) VALUES (%s, %s, %s, %s)"
    prev = json.dumps(previous_state) if previous_state is not None else None
    new = json.dumps(new_state) if new_state is not None else None
    return execute(q, (flight_id, prev, new, note), commit=True)
