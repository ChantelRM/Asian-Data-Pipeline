import pandas as pd
import pandera as pa
import pytest

from src.schemas.contracts import raw_mydramalist_schema, clean_dramas_schema


def test_raw_schema_accepts_valid_row():
    df = pd.DataFrame(
        {
            "title": ["Reply 1988"],
            "country": ["South Korea"],
            "tags": ["Family, Friendship, 1988"],
            "rating": [9.2],
            "episodes": [20],
            "air_date": ["2015-11-06"],
            "network": ["tvN"],
            "scrape_date": ["2024-01-01"],
        }
    )
    validated = raw_mydramalist_schema.validate(df)
    assert len(validated) == 1


def test_raw_schema_rejects_rating_out_of_range():
    df = pd.DataFrame(
        {
            "title": ["Bad Rating Drama"],
            "country": ["Thailand"],
            "tags": ["BL"],
            "rating": [15.0],  # invalid: out of 0-10 range
            "episodes": [12],
            "air_date": ["2023-01-01"],
            "network": ["GMMTV"],
            "scrape_date": ["2024-01-01"],
        }
    )
    with pytest.raises(pa.errors.SchemaErrors):
        raw_mydramalist_schema.validate(df, lazy=True)


def test_raw_schema_allows_null_rating_and_dates():
    # Real MyDramaList scrapes have missing ratings/dates for less popular
    # titles -- schema should allow nulls here, not force fabricated defaults.
    df = pd.DataFrame(
        {
            "title": ["Obscure Drama"],
            "country": [None],
            "tags": [None],
            "rating": [None],
            "episodes": [None],
            "air_date": [None],
            "network": [None],
            "scrape_date": [None],
        }
    )
    validated = raw_mydramalist_schema.validate(df)
    assert pd.isna(validated.loc[0, "rating"])


def test_clean_schema_requires_unique_source_title_key():
    df = pd.DataFrame(
        {
            "source_title_key": ["south korea::reply 1988", "south korea::reply 1988"],
            "title": ["Reply 1988", "Reply 1988"],
            "country": ["South Korea", "South Korea"],
            "tags": [["Family"], ["Family"]],
            "rating": [9.2, 9.2],
            "episode_count": pd.array([20, 20], dtype="Int64"),
            "air_date": [pd.Timestamp("2015-11-06"), pd.Timestamp("2015-11-06")],
            "network": ["tvN", "tvN"],
        }
    )
    with pytest.raises(pa.errors.SchemaErrors):
        clean_dramas_schema.validate(df, lazy=True)
