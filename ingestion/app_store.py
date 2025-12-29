from app_store_scraper import AppStore

def fetch_apple_reviews(app_name, app_id, count=1000):
    app = AppStore(
        country="in",   # 🔑 CHANGE THIS (try 'in' first)
        app_name=app_name,
        app_id=app_id
    )
    app.review(how_many=count)

    data = []
    for r in app.reviews:
        data.append({
            "review_id": r.get("id"),
            "rating": r.get("rating"),
            "text": r.get("review"),
            "version": r.get("version"),
            "date": r.get("date")
        })
    return data

