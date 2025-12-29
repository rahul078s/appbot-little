from google_play_scraper import reviews, Sort

def fetch_google_reviews(app_id, count=100):
    result, _ = reviews(
        app_id,
        lang="en",
        country="us",
        sort=Sort.NEWEST,
        count=count
    )

    data = []
    for r in result:
        data.append({
            "review_id": r["reviewId"],
            "rating": r["score"],
            "text": r["content"],
            "version": r.get("appVersion"),
            "date": r["at"]
        })
    return data