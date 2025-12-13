from fastapi import APIRouter, HTTPException, Request, status
from app.schemas.flight import FlightCreate, FlightOut, FlightUpdate
from app.services import flight_service
from typing import Dict

router = APIRouter(prefix="/flights", tags=["flights"])

@router.post("", status_code=status.HTTP_201_CREATED)
def create_flight(f: FlightCreate):
    try:
        flight_service.create_flight(f.dict())
        return {"message": "created"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="internal error")

@router.get("", response_model=Dict)
def list_flights(request: Request,
                 page: int = 1, size: int = 20,
                 sort_by: str = "departure_time", order: str = "asc",
                 origin: str = None, destination: str = None, status: str = None,
                 aircraft_type: str = None, departure_from: str = None, departure_to: str = None):
    qp = {
        "page": page, "size": size, "sort_by": sort_by, "order": order,
        "origin": origin, "destination": destination, "status": status,
        "aircraft_type": aircraft_type, "departure_from": departure_from, "departure_to": departure_to
    }
    try:
        return flight_service.list_flights(qp)
    except Exception:
        raise HTTPException(status_code=500, detail="internal error")

@router.get("/{flight_id}", response_model=FlightOut)
def get_flight(flight_id: int):
    f = flight_service.get_flight(flight_id)
    if not f:
        raise HTTPException(status_code=404, detail="flight not found")
    return f

@router.put("/{flight_id}")
def update_flight(flight_id: int, updates: FlightUpdate):
    new = flight_service.update_flight(flight_id, updates.dict(exclude_unset=True))
    if new is None:
        raise HTTPException(status_code=404, detail="flight not found")
    return {"message": "updated", "flight": new}

@router.delete("/{flight_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flight(flight_id: int):
    ok = flight_service.delete_flight(flight_id)
    if not ok:
        raise HTTPException(status_code=404, detail="flight not found")
    return {}
