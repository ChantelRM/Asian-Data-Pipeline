import pandas as pd
import pytest

from src.transform.clean_dramas import _parse_tags, _parse_air_date, _make_source_title_key


class TestParseTags:
    def test_splits_and_strips_comma_separated_tags(self):
        assert _parse_tags("Romance, BL, School Life") == ["Romance", "BL", "School Life"]

    def test_filters_out_bare_year_tokens(self):
        # Real MyDramaList tag strings mix genuine tags with a trailing
        # year, e.g. "Romance, BL, 2023" -- the year is not a genre.
        assert _parse_tags("Romance, BL, 2023") == ["Romance", "BL"]

    def test_handles_none_and_empty_string(self):
        assert _parse_tags(None) == []
        assert _parse_tags("") == []
        assert _parse_tags("   ") == []

    def test_handles_extra_whitespace_and_trailing_commas(self):
        assert _parse_tags("Romance,  , BL,") == ["Romance", "BL"]


class TestParseAirDate:
    def test_parses_iso_format(self):
        result = _parse_air_date("2023-04-01")
        assert result == pd.Timestamp("2023-04-01")

    def test_parses_us_slash_format_dayfirst_convention(self):
        # 01/04/2023 is ambiguous (day/month vs month/day). We document
        # and test the dayfirst convention explicitly here, rather than
        # letting it silently vary based on pandas defaults.
        result = _parse_air_date("01/04/2023")
        assert result == pd.Timestamp("2023-04-01")

    def test_returns_none_for_garbage_input(self):
        assert _parse_air_date("not a date") is None

    def test_returns_none_for_null_input(self):
        assert _parse_air_date(None) is None
        assert _parse_air_date("") is None


class TestMakeSourceTitleKey:
    def test_normalizes_case_and_whitespace(self):
        key1 = _make_source_title_key("Reply 1988", "South Korea")
        key2 = _make_source_title_key("  reply 1988  ", "south korea")
        assert key1 == key2

    def test_handles_missing_country(self):
        key = _make_source_title_key("Some Drama", None)
        assert key == "unknown::some drama"
