import psycopg2
from sentence_splitter import smart_split

conn = psycopg2.connect(
    dbname="appbot",
    user="appbot",
    password="appbot",
    host="localhost",
    port=5432
)

cur = conn.cursor()

cur.execute("""
    SELECT
        rr.id,
        rr.app_id,
        pr.sentiment_label,
        pr.sentiment_score,
        rr.review_text
    FROM raw_reviews rr
    JOIN processed_reviews pr ON pr.raw_review_id = rr.id
    WHERE rr.id NOT IN (
        SELECT DISTINCT raw_review_id FROM review_sentences
    )
""")

rows = cur.fetchall()

inserted = 0

for raw_id, app_id, label, score, text in rows:
    sentences = smart_split(text)

    for s in sentences:
        cur.execute("""
            INSERT INTO review_sentences
            (raw_review_id, app_id, sentiment_label, sentiment_score, sentence)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (raw_id, app_id, label, score, s))
        inserted += 1

conn.commit()
cur.close()
conn.close()

print(f"Inserted {inserted} sentences")
