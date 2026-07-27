"""
Pandera schema contracts.

WHY THIS FILE EXISTS: this is the single place that defines "what does
valid data look like" at each stage boundary of the pipeline. Get this
right and pandera will fail loudly and specifically when bad data shows
up (e.g. "column 'rating' has value -3.2 which violates check
in_range(0,10) at row 4821") instead of the failure surfacing three steps
later as a cryptic KeyError somewhere in load.

YOUR TASK: define three DataFrameSchema objects below. Import
`pandera as pa` and use `pa.DataFrameSchema`, `pa.Column`, `pa.Check`.

--------------------------------------------------------------------
1. raw_mydramalist_schema
--------------------------------------------------------------------
Validates the data immediately after reading the Kaggle CSV, BEFORE any
cleaning. Think about what columns the source actually has (check the
real CSV once you've downloaded it — don't guess) and how permissive
this needs to be. Questions to answer for yourself:
  - Which columns can be null? (hint: real scrape data has missing
    ratings, missing air dates, missing cast info for less popular titles)
  - Should "tags" be validated as a single raw string here, or already
    parsed into a list? (hint: think about which stage's job that is —
    extract's job is read + validate structure, not clean.)
  - What's a sane range check for "rating"? For "episodes"?
  - Should this schema be `strict=True` or allow extra/unexpected
    columns from the source without failing? What's the tradeoff?

--------------------------------------------------------------------
2. clean_dramas_schema
--------------------------------------------------------------------
Validates data AFTER transform/cleaning, right before it's safe to load.
This is arguably the more important contract — if data passes this,
it should be safe to write to Postgres without surprises. Think about:
  - What should be the key column, and should it be unique? (this
    matters a lot for your idempotent-upsert strategy downstream)
  - What type should "tags" be after cleaning (still a raw string,
    or something else)?
  - What type should "air_date" be after cleaning?

--------------------------------------------------------------------
3. tmdb_enrichment_schema
--------------------------------------------------------------------
Validates the TMDb API response data, one row per matched (or unmatched)
title. Think about:
  - What should happen to rows where TMDb had no match at all?
    Should tmdb_id be nullable?
  - What field holds watch-provider names, and what type is it?
--------------------------------------------------------------------

Once you've written these, run:
    pytest tests/test_schemas.py -v
That test file is your spec — it tells you exactly what column names
and behaviors are expected. Read the assertions before you write the
schema, not after.
"""

import pandera as pa
from pandera import Column, Check, DataFrameSchema

# TODO: define raw_mydramalist_schema
raw_mydramalist_schema = None

# TODO: define clean_dramas_schema
clean_dramas_schema = None

# TODO: define tmdb_enrichment_schema
tmdb_enrichment_schema = None
