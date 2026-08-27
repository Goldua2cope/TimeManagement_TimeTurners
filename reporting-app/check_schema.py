from db import get_connection

conn = get_connection()
cur = conn.cursor()
tables = ['employees', 'customers', 'timeentries', 'total_hours']
for t in tables:
    print(f"--- {t} ---")
    cur.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = %s
        ORDER BY ordinal_position;
    """, (t,))
    for row in cur.fetchall():
        print(row)
cur.close()
conn.close()