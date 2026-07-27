"""
Load step: dimensions first (get-or-create), then the fact table
(upsert on the natural key), then the tag bridge table.

IDEMPOTENCY IS THE POINT OF THIS FILE. Airflow WILL re-run tasks — on
manual retry, on backfill, on a flaky network blip during the TMDb call
in an earlier stage. Plain INSERTs here would double your fact rows on
every re-run. Two mechanisms need to make re-runs safe:

  1. Dimension tables (country, tag, network/platform, date) need a
     get-or-create pattern: look up by name first, insert only if not
     found. Think about why this matters for a many-to-many tag bridge
     table specifically — what happens if you insert a duplicate "BL"
     tag row every time you see a BL drama?
  2. fact_dramas needs to upsert on a natural key (source_title_key),
     not blindly insert. Postgres's `INSERT ... ON CONFLICT (...) DO
     UPDATE` is built for exactly this — look it up if you haven't used
     it before, it's a one-statement solve rather than a manual
     SELECT-then-INSERT-or-UPDATE round trip from Python (which is also
     slower AND races under concurrent runs).

THINGS TO DECIDE AND IMPLEMENT:
  1. A connection function reading DB credentials from environment
     variables (see .env.example / docker-compose.yml for the names
     already wired up: WAREHOUSE_DB_HOST, WAREHOUSE_DB_NAME, etc).
  2. get-or-create helpers for dim_country, dim_network_platform,
     dim_date, dim_genre_tag. Note dim_date needs a few derived columns
     (year, quarter, month, day) computed from the date, not just stored
     as a bare date.
  3. The main load_dramas() function: for each cleaned drama row, resolve
     dimension foreign keys, upsert the fact row, then refresh that
     drama's tag bridge rows (think about whether "delete existing bridge
     rows for this drama_id then reinsert" is simpler than trying to diff
     old vs new tags — it usually is, for a re-run-safe many-to-many).
  4. Wrap the whole load in a transaction — commit on success, rollback
     on any failure, so a partial failure never leaves the warehouse in
     a half-loaded state.

This part is genuinely hard to unit-test without a live Postgres, so
budget real time for `docker compose up` + manually inspecting the
warehouse tables (`psql` or a GUI) rather than assuming it works.
"""

import logging
import os
from pathlib import Path
from typing import Optional

import pandas as pd
import psycopg2

logger = logging.getLogger(__name__)

CLEAN_DRAMAS_PATH = Path("data/processed/dramas_clean.parquet")


def _get_connection():
    """Open a psycopg2 connection using env vars for host/db/user/password."""
    # TODO: implement
    raise NotImplementedError


def load_dramas(clean_path: Path = CLEAN_DRAMAS_PATH) -> None:
    """
    Load the cleaned dramas dataframe into the warehouse star schema:
    resolve/create dimension rows, upsert fact_dramas, refresh
    fact_drama_tag bridge rows. Should be safe to run multiple times
    against the same data without creating duplicates.
    """
    # TODO: implement
    raise NotImplementedError("load_dramas not yet implemented")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_dramas()
