A FastAPI based backend service for managing flight data, with direct MySQL queries (no ORM). Supports CRUD operations, pagination, filtering, sorting, and change logging.

🚀 Features

Create, read, update, and delete flights
Filter by origin, destination, aircraft type, status, and departure date range
Sort by any column (flight number, departure time, arrival time, etc.)
Pagination for listing flights
Track changes with flight logs (previous and new state)
Fully implemented using layered architecture:
Router → Service → Repository → Database
Includes sample data loader
Simple unit test for API endpoint
