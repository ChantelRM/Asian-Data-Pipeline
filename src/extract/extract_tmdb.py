"""
Extract step for the live-API source: TMDb.

This is the piece that demonstrates a live-fetch pattern distinct from
the static Kaggle file. Get a free key at
https://www.themoviedb.org/settings/api and read their docs for:
  - GET /search/tv  (search by title)
  - GET /tv/{id}/watch/providers  (streaming availability by region)

THINGS TO DECIDE AND IMPLEMENT:
  1. For each title from the extracted MyDramaList data, search TMDb's
     /search/tv endpoint and take a result (top match, or something
     smarter if you want to handle ambiguous titles better).
     Known limitation to be aware of, not necessarily solve: exact/fuzzy
     title-text search will miss some titles (alternate romanizations,
     subtitles). Decide how much effort that's worth for a two-week
     project, and document whatever you decide in your README rather
     than silently hoping it's fine.
  2. Decide what to do with titles that get NO match — should they be
     dropped, or kept with null enrichment fields? (Think about what
     dropping them would do to any later "do BL dramas rate higher"
     query — silent survivorship bias is a real risk here.)
  3. Rate limiting: don't hammer the API in a tight loop with zero
     delay. Think about what happens if a request fails mid-run (a
     timeout, a 429) — should the whole extract blow up, or should a
     handful of failed lookups just fall back to null gracefully?
  4. Fetch watch-provider data for matched titles too (region: pick one,
     e.g. "ZA" or "US" — TMDb's response is keyed by region).
  5. Validate the assembled dataframe against tmdb_enrichment_schema
     and write it as a snapshot to data/processed/.

Get your API key into the environment as TMDB_API_KEY (see .env.example)
— never hardcode it in this file.
"""

import logging
import os
import time
from pathlib import Path

import requests
import pandas as pd

# from src.schemas.contracts import tmdb_enrichment_schema

logger = logging.getLogger(__name__)

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

INPUT_PATH = Path("data/processed/mydramalist_extracted.parquet")
OUTPUT_PATH = Path("data/processed/tmdb_enrichment.parquet")


def extract_tmdb(input_path: Path = INPUT_PATH, output_path: Path = OUTPUT_PATH) -> Path:
    """
    For each title in the MyDramaList extract, look it up on TMDb and
    write an enrichment snapshot (poster path, popularity, watch
    providers) to data/processed/.
    """
    if not TMDB_API_KEY:
        raise EnvironmentError(
            "TMDB_API_KEY is not set. Get a free key at "
            "https://www.themoviedb.org/settings/api and set it in .env"
        )

    # TODO: implement
    raise NotImplementedError("extract_tmdb not yet implemented")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    extract_tmdb()
