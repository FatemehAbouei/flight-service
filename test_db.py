from app.db.database import fetchone

row = fetchone("SELECT 1 as test")
print(row)
