from db import get_connection

def get_hours_per_consultant(start_date, end_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.consultant_name,
               ROUND(SUM(EXTRACT(EPOCH FROM (t.end_time - t.start_time))/3600
                   - t.lunch_break/60.0)::numeric, 2) AS total_hours
        FROM timeentries t
        JOIN employees e ON t.consultant_id = e.id
        WHERE t.work_date BETWEEN %s AND %s
        GROUP BY e.consultant_name;
    """, (start_date, end_date))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_hours_per_customer(start_date, end_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.customer_name,
               ROUND(SUM(EXTRACT(EPOCH FROM (t.end_time - t.start_time))/3600
                   - t.lunch_break/60.0)::numeric, 2) AS total_hours
        FROM timeentries t
        JOIN customers c ON t.customer_id = c.id
        WHERE t.work_date BETWEEN %s AND %s
        GROUP BY c.customer_name;
    """, (start_date, end_date))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_average_hours_per_consultant(start_date, end_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.consultant_name,
               ROUND(AVG(EXTRACT(EPOCH FROM (t.end_time - t.start_time))/3600
                   - t.lunch_break/60.0)::numeric, 2) AS avg_hours_per_day
        FROM timeentries t
        JOIN employees e ON t.consultant_id = e.id
        WHERE t.work_date BETWEEN %s AND %s
        GROUP BY e.consultant_name;
    """, (start_date, end_date))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


if __name__ == "__main__":
    print(get_hours_per_consultant("2026-08-01", "2026-08-31"))
    print(get_hours_per_customer("2026-08-01", "2026-08-31"))