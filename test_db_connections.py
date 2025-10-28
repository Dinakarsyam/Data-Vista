import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

print(f"DB_USER: {DB_USER}")
print(f"DB_PASSWORD: {DB_PASSWORD}")
print(f"DB_HOST: {DB_HOST}")
print(f"DB_NAME: {DB_NAME}")

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    print("One or more environment variables are missing.")
else:
    DB_PASSWORD_ENCODED = quote_plus(DB_PASSWORD)
    DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD_ENCODED}@{DB_HOST}/{DB_NAME}'

    engine = create_engine(DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def test_connection():
        try:
            db = SessionLocal()
            db.execute("SELECT 1")
            print("Database connection successful!")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
        finally:
            db.close()

    if __name__ == "__main__":
        test_connection()
