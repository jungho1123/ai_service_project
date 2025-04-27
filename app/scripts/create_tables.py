# app/scripts/create_tables.py
from app.core.database import Base, engine
from app.models.pill import Pill

def init_db():
    print("  Creating tables")
    Base.metadata.create_all(bind=engine)
    print("  Done.")

if __name__ == "__main__":
    init_db()
