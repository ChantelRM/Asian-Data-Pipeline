"""
Extract step for the batch/file source: MyDramaList Kaggle dataset.

DESIGN CONSTRAINT TO KEEP: this function should NOT clean data. Read,
validate structurally against `raw_mydramalist_schema`, write a snapshot
to data/processed/. Keeping extract "dumb" means you can re-run
transform logic against a fixed extract snapshot without re-touching the
source CSV — useful once you're iterating on cleaning bugs and don't
want extract-time surprises mixed in with transform-time bugs while you
debug.

THINGS TO DECIDE AND IMPLEMENT:
  1. Read the CSV with pandas.
  2. The Kaggle scrape almost certainly has duplicate rows for the same
     title across different scrape dates. Decide how to dedupe (hint:
     if there's a scrape_date column, keep the most recent one per
     title+country) — do this BEFORE validation, not after.
  3. Validate against raw_mydramalist_schema (see src/schemas/contracts.py)
     — you'll need to build that schema first.
  4. Write the validated dataframe somewhere in data/processed/ as a
     snapshot for the next stage to read. Think about file format:
     CSV vs parquet — what does each preserve or lose about dtypes?
  5. Log how many rows you read, how many survived dedup, and where you
     wrote the output. If a row count check would help you catch
     silent data loss later, consider it.

Consider what should happen if the CSV file doesn't exist at the
expected path — silently producing an empty dataframe is a bad failure
mode; think about what error message would actually help future-you
debug this at 11pm.
"""

import logging
import os
from pathlib import Path

import pandas as pd

# from src.schemas.contracts import raw_mydramalist_schema

logger = logging.getLogger(__name__)

RAW_CSV_PATH = Path(
    os.environ.get("MYDRAMALIST_CSV_PATH", "data/raw/mydramalist.csv")
)
OUTPUT_PATH = Path("data/processed/mydramalist_extracted.parquet")


def extract_mydramalist(csv_path: Path = RAW_CSV_PATH, output_path: Path = OUTPUT_PATH) -> Path:
    """
    Read, dedupe, validate, and snapshot the MyDramaList CSV.

    Returns the path the validated snapshot was written to.
    """
    # TODO: implement
    raise NotImplementedError("extract_mydramalist not yet implemented")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    extract_mydramalist()
