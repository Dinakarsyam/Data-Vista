import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import g

def get_db_connection():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
    return g.db

def close_db_connection(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
