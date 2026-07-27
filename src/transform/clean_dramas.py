"""
Transform step: this is where the real messiness of the source data
gets handled — deliberately kept separate from extract (read+validate
only) and load (write only).

The function signatures below (_parse_tags, _parse_air_date,
_make_source_title_key, clean_dramas) are already fixed to match
tests/test_transform.py — that test file IS your spec. Read it before
you write anything here. Run `pytest tests/test_transform.py -v`
constantly while you work; it's designed to be a tight TDD loop.

THREE PROBLEMS YOU NEED TO SOLVE (each has a real gotcha worth hitting
yourself rather than being told the answer up front):

1. _parse_tags — multi-value tags arrive as one comma-separated string
   ("Romance, BL, School Life, 2023"). Split them into a clean list.
   The test file has a case about a bare 4-digit token showing up in the
   tag string — think about why that would be there and what a genre
   list should NOT contain.

2. _parse_air_date — dates arrive in multiple formats across scrape
   batches (ISO "YYYY-MM-DD", and ambiguous slash-formats like
   "01/04/2023" where day/month order isn't obvious from the string
   alone). pandas.to_datetime has a `dayfirst` parameter for exactly
   this kind of ambiguity. Worth testing it against BOTH format types
   before you trust it blindly — don't assume one setting is
   correct for every date string you'll see in this dataset.

3. _make_source_title_key — build a stable natural key from title +
   country for idempotent upserts downstream. Handle a missing country
   gracefully. Python gotcha to be aware of: `some_value or "default"`
   is a common fallback pattern, but think carefully about what pandas
   actually puts in a dataframe cell when a CSV field is empty, and
   whether that value is "falsy" in the way you'd expect.

4. clean_dramas — the orchestrating function: read the extract
   snapshot(s), apply the three functions above, left-join TMDb
   enrichment (keep unmatched titles rather than dropping them — think
   about why dropping them would bias any later analysis), dedupe,
   validate against clean_dramas_schema, and write the result to
   data/processed/.

Run the tests as you go — they'll tell you immediately if something's
off, which is a much shorter feedback loop than waiting until load fails
against Postgres.
"""

import logging
import re
from pathlib import Path
from typing import Optional

import pandas as pd

# from src.schemas.contracts import clean_dramas_schema

logger = logging.getLogger(__name__)

MYDRAMALIST_PATH = Path("data/processed/mydramalist_extracted.parquet")
TMDB_PATH = Path("data/processed/tmdb_enrichment.parquet")
OUTPUT_PATH = Path("data/processed/dramas_clean.parquet")


def _make_source_title_key(title: str, country: Optional[str]) -> str:
    """
    Build a stable natural key from title + country, used for
    idempotent upserts downstream. Should normalize case/whitespace and
    handle a missing/null country by falling back to some default
    (see tests/test_transform.py::TestMakeSourceTitleKey for the exact
    expected format).
    """
    # TODO: implement
    raise NotImplementedError


def _parse_tags(raw_tags: Optional[str]) -> list:
    """
    Parse a comma-separated tag string into a clean list of tag strings.
    See tests/test_transform.py::TestParseTags for expected edge cases
    (empty/None input, extra whitespace, trailing commas, and a bare
    year token that shouldn't be treated as a genre tag).
    """
    # TODO: implement
    raise NotImplementedError


def _parse_air_date(raw_date) -> Optional[pd.Timestamp]:
    """
    Parse a single air_date string into a pandas Timestamp, or None if
    it can't be parsed. See tests/test_transform.py::TestParseAirDate
    for the exact formats this needs to handle correctly, including
    both an ISO-format case and an ambiguous slash-format case — make
    sure your approach gets BOTH right, not just one.
    """
    # TODO: implement
    raise NotImplementedError


def clean_dramas(
    mydramalist_path: Path = MYDRAMALIST_PATH,
    tmdb_path: Path = TMDB_PATH,
    output_path: Path = OUTPUT_PATH,
) -> Path:
    """
    Orchestrate the full transform: load the extract snapshot(s), clean
    tags/dates, build the natural key, left-join TMDb enrichment, dedupe,
    validate, and write the cleaned dataframe to data/processed/.
    """
    # TODO: implement
    raise NotImplementedError("clean_dramas not yet implemented")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    clean_dramas()
