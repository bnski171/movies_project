from sqlalchemy import create_engine

DATABASE_URL = "postgresql://user:1111@localhost:5432/movies"

engine = create_engine(DATABASE_URL)
try:
    connection = engine.connect()
    print("Connection successful!")
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")
