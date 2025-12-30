from google_play_scraper import reviews, Sort

STORE = "google"

def fetch_google_reviews(app_id: str, count: int = 1000, country="in"):
    result, _ = reviews(
        app_id,
        lang="en",
        country=country,
        sort=Sort.NEWEST,
        count=count
    )

    data = []
    for r in result:
        # Defensive extraction
        review_id = r.get("reviewId")
        text = r.get("content")

        if not review_id or not text:
            continue  # skip invalid rows safely

        data.append({
            "app_id": app_id,
            "store": STORE,
            "review_id": review_id,
            "rating": r.get("score"),
            "text": text.strip(),
            "version": r.get("appVersion"),
            "date": r.get("at")
        })

    return data
