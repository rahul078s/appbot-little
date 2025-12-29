-- =========================================================
-- APPBOT CORE SCHEMA MIGRATION
-- =========================================================
-- This migration recreates:
-- 1. raw_reviews
-- 2. processed_reviews
-- with all required indexes
-- =========================================================

BEGIN;

-- =========================
-- 1. RAW REVIEWS TABLE
-- =========================
DROP TABLE IF EXISTS processed_reviews CASCADE;
DROP TABLE IF EXISTS raw_reviews CASCADE;

CREATE TABLE raw_reviews (
    id SERIAL PRIMARY KEY,

    app_id TEXT NOT NULL,
    store TEXT NOT NULL,              -- google | apple

    review_id TEXT NOT NULL UNIQUE,   -- external review id
    rating INTEGER,
    review_text TEXT NOT NULL,

    app_version TEXT,
    review_date TIMESTAMP,

    created_at TIMESTAMP DEFAULT NOW()
);

-- -------------------------
-- Indexes for raw_reviews
-- -------------------------
CREATE INDEX idx_raw_reviews_app_id
    ON raw_reviews (app_id);

CREATE INDEX idx_raw_reviews_store
    ON raw_reviews (store);

CREATE INDEX idx_raw_reviews_app_store
    ON raw_reviews (app_id, store);

CREATE INDEX idx_raw_reviews_created_at
    ON raw_reviews (created_at);

CREATE INDEX idx_raw_reviews_rating
    ON raw_reviews (rating);

-- =========================
-- 2. PROCESSED REVIEWS TABLE
-- =========================
CREATE TABLE processed_reviews (
    id SERIAL PRIMARY KEY,

    raw_review_id INTEGER UNIQUE
        REFERENCES raw_reviews(id)
        ON DELETE CASCADE,

    app_id TEXT NOT NULL,
    store TEXT NOT NULL,

    language TEXT,
    sentiment_label TEXT CHECK (
        sentiment_label IN ('positive', 'neutral', 'negative')
    ),
    sentiment_score FLOAT,

    created_at TIMESTAMP DEFAULT NOW()
);

-- -------------------------
-- Indexes for processed_reviews
-- -------------------------
CREATE INDEX idx_processed_reviews_app_store
    ON processed_reviews (app_id, store);

CREATE INDEX idx_processed_reviews_sentiment
    ON processed_reviews (sentiment_label);

CREATE INDEX idx_processed_reviews_created_at
    ON processed_reviews (created_at);

COMMIT;
