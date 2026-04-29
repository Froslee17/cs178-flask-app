import pymysql
import creds

def get_conn():
    return pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
        cursorclass=pymysql.cursors.DictCursor
    )

def execute_query(query, args=()):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, args)

            if query.strip().lower().startswith("select"):
                results = cur.fetchall()
            else:
                conn.commit()
                results = None

            return results
    finally:
        conn.close()
