# dbCode.py
# Author: Alex Froslee
# Helper functions for database connection and queries

import pymysql
from creds import *

def get_conn():
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db,
        cursorclass=pymysql.cursors.DictCursor
    )

def execute_query(query, args=()):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, args)
            return cur.fetchall()
    finally:
        conn.close()
