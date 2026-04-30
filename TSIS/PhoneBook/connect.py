import psycopg2
from config import *

def connect():
    return psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )