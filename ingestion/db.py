import psycopg2

conn = psycopg2.connect(
    dbname="appbot",
    user="appbot",
    password="appbot",
    host="postgres"
)
conn.autocommit = False  # IMPORTANT

def save_review(app_id, store, r):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO raw_reviews
                (app_id, store, review_id, rating, review_text, app_version, review_date)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (review_id) DO NOTHING
            """, (
                app_id,
                store,
                r.get("review_id"),
                r.get("rating"),
                r.get("text"),
                r.get("version"),
                r.get("date")
            ))
        conn.commit()

    except Exception as e:
        conn.rollback()   # 🔑 THIS FIXES THE BUG
        print("DB ERROR:", e)
