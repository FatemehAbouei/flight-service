import json
from app.db.database import fetchone, execute

def load_sample(path: str = "flights_sample.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for rec in data:
        existing = fetchone("SELECT flight_id FROM flights WHERE flight_id = %s", (rec["flight_id"],))
        if existing:
            continue
        execute("""
        INSERT INTO flights (
            flight_id, flight_number, origin, destination, departure_time, arrival_time,
            duration_minutes, aircraft_type, seats_total, seats_available, status, created_at, updated_at, process_id
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            rec["flight_id"], rec["flight_number"], rec["origin"], rec["destination"],
            rec["departure_time"], rec["arrival_time"], rec["duration_minutes"],
            rec.get("aircraft_type"), rec.get("seats_total"), rec.get("seats_available"),
            rec.get("status"), rec.get("created_at"), rec.get("updated_at"), rec.get("process_id")
        ), commit=True)
    print("sample data loaded.")

if __name__ == "__main__":
    load_sample()
