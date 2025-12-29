from fastapi import FastAPI
from google_play import fetch_google_reviews
from app_store import fetch_apple_reviews
from db import save_review
from nlp import analyze_text
from db import conn

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest/google")
def ingest_google(app_id: str):
    reviews = fetch_google_reviews(app_id)

    success = 0
    failed = 0

    for r in reviews:
        try:
            save_review(app_id, "google", r)
            success += 1
        except Exception as e:
            failed += 1
            print("REVIEW FAILED:", e)

    return {
        "total": len(reviews),
        "inserted": success,
        "failed": failed
    }

@app.post("/ingest/apple")
def ingest_apple(app_name: str, app_id: str):
    reviews = fetch_apple_reviews(app_name, app_id)
    for r in reviews:
        save_review(app_id, "apple", r)
    return {"inserted": len(reviews)}

@app.post("/process/reviews")
def process_reviews(limit: int = 100):
    cur = conn.cursor()

    cur.execute("""
        SELECT id, app_id, store, review_text
        FROM raw_reviews
        WHERE id NOT IN (
            SELECT raw_review_id FROM processed_reviews
        )
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()
    inserted = 0

    for r in rows:
        lang, label, score = analyze_text(r[3])

        cur.execute("""
            INSERT INTO processed_reviews
            (raw_review_id, app_id, store, language, sentiment_label, sentiment_score)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (r[0], r[1], r[2], lang, label, score))

        inserted += 1

    conn.commit()
    return {"processed": inserted}