# app/services/flight_service.py
from app.repos import flight_repo
from typing import Dict, Any
from datetime import datetime

def create_flight(data: Dict[str, Any]):
    # basic validation: flight_id unique
    existing = flight_repo.get_flight_by_id(data.get("flight_id"))
    if existing:
        raise ValueError("flight_id already exists")
    # ensure created_at/updated_at
    if not data.get("created_at"):
        data["created_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    if not data.get("updated_at"):
        data["updated_at"] = data["created_at"]
    return flight_repo.insert_flight(data)

def list_flights(query_params: Dict[str, Any]):
    page = int(query_params.get("page", 1))
    size = int(query_params.get("size", 20))
    sort_by = query_params.get("sort_by", "departure_time")
    order = query_params.get("order", "asc")
    filters = {
        "origin": query_params.get("origin"),
        "destination": query_params.get("destination"),
        "status": query_params.get("status"),
        "aircraft_type": query_params.get("aircraft_type"),
        "departure_from": query_params.get("departure_from"),
        "departure_to": query_params.get("departure_to"),
    }
    total = flight_repo.count_flights(filters)
    items = flight_repo.get_flights(filters, page=page, size=size, sort_by=sort_by, order=order)
    return {"total": total, "page": page, "size": size, "items": items}

def get_flight(fid: int):
    return flight_repo.get_flight_by_id(fid)

def update_flight(fid: int, changes: Dict[str, Any]):
    prev = flight_repo.get_flight_by_id(fid)
    if not prev:
        return None
    # set updated_at
    changes["updated_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    flight_repo.update_flight(fid, changes)
    new = flight_repo.get_flight_by_id(fid)
    flight_repo.insert_flight_log(fid, prev, new, note="update")
    return new

def delete_flight(fid: int):
    prev = flight_repo.get_flight_by_id(fid)
    if not prev:
        return False
    flight_repo.delete_flight(fid)
    flight_repo.insert_flight_log(fid, prev, {}, note="delete")
    return True
