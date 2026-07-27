#!/usr/bin/env bash
# Bulk-creates one GitHub issue per build task, in the same order as the
# README's "Suggested build order". Run this once, from inside the repo,
# after `git remote add origin ...` and `gh auth login`.
#
# Requires: GitHub CLI (https://cli.github.com/) installed and
# authenticated (`gh auth login`), and this script run from inside a
# git repo that already has a GitHub remote.
#
# Usage:
#   chmod +x scripts/create_issues.sh
#   ./scripts/create_issues.sh

set -euo pipefail

echo "Creating labels (safe to ignore 'already exists' errors)..."
gh label create "schema-design" --color "5319E7" --description "DB/pandera schema work" 2>/dev/null || true
gh label create "extract"       --color "0E8A16" --description "Extract stage"           2>/dev/null || true
gh label create "transform"     --color "1D76DB" --description "Transform stage"         2>/dev/null || true
gh label create "load"          --color "D93F0B" --description "Load stage"              2>/dev/null || true
gh label create "orchestration" --color "FBCA04" --description "Airflow DAG"             2>/dev/null || true
gh label create "docs"          --color "C5DEF5" --description "README / writeup"        2>/dev/null || true

echo "Creating issues..."

gh issue create \
  --title "Design star schema DDL (init.sql)" \
  --label "schema-design" \
  --body "Write the CREATE TABLE statements in src/db/init.sql for all six tables (dim_country, dim_genre_tag, dim_network_platform, dim_date, fact_dramas, fact_drama_tag). Column lists are given as comments in the file.

Acceptance criteria:
- All 6 tables defined with appropriate PKs/FKs
- fact_drama_tag correctly models the tag many-to-many (not a delimited string column)
- source_title_key on fact_dramas is UNIQUE (required for idempotent upserts later)
- docker compose up brings up postgres-warehouse with the schema applied cleanly"

gh issue create \
  --title "Define pandera schema contracts (contracts.py)" \
  --label "schema-design" \
  --body "Implement raw_mydramalist_schema, clean_dramas_schema, and tmdb_enrichment_schema in src/schemas/contracts.py.

Acceptance criteria:
- pytest tests/test_schemas.py -v passes
- raw schema allows the nulls real scrape data actually has (missing ratings/dates)
- clean schema enforces uniqueness on the natural key column"

gh issue create \
  --title "Implement tag parsing, date parsing, and key generation (clean_dramas.py helpers)" \
  --label "transform" \
  --body "Implement _parse_tags, _parse_air_date, _make_source_title_key in src/transform/clean_dramas.py.

Acceptance criteria:
- pytest tests/test_transform.py -v passes (all 3 test classes)
- _parse_tags correctly filters out bare year tokens
- _parse_air_date correctly handles both ISO and ambiguous slash-format dates
- _make_source_title_key handles a missing/null country without crashing"

gh issue create \
  --title "Implement extract_mydramalist.py" \
  --label "extract" \
  --body "Read + dedupe + validate + snapshot the Kaggle CSV.

Acceptance criteria:
- Download the real 'Complete 5000 dramas from MyDramaList' CSV and confirm actual column names match (or adjust) the schema from the earlier issue
- Duplicate scrape-date rows are deduped, keeping the most recent
- Raises a clear error if the CSV file is missing, rather than silently producing empty output
- python -m src.extract.extract_mydramalist runs cleanly against the real CSV"

gh issue create \
  --title "Implement extract_tmdb.py" \
  --label "extract" \
  --body "Live TMDb API lookup + enrichment snapshot.

Acceptance criteria:
- Get a free TMDb API key and confirm it's read from TMDB_API_KEY env var, not hardcoded
- Unmatched titles are kept with null enrichment fields, not dropped
- A single failed request doesn't crash the whole run
- Some form of rate-limit delay between requests
- python -m src.extract.extract_tmdb runs cleanly against real data"

gh issue create \
  --title "Implement clean_dramas() orchestrator" \
  --label "transform" \
  --body "Wire the helper functions together: load both extract snapshots, clean tags/dates, left-join TMDb enrichment, dedupe, validate, write output.

Acceptance criteria:
- Unmatched TMDb titles are kept (left join), not dropped
- Output validates against clean_dramas_schema
- python -m src.transform.clean_dramas runs cleanly end to end against real extract output"

gh issue create \
  --title "Implement load_postgres.py" \
  --label "load" \
  --body "Dimension get-or-create + fact upsert + tag bridge refresh.

Acceptance criteria:
- Running load twice with the same input does NOT create duplicate rows (test this manually -- run it, check row counts, run it again, check row counts are unchanged)
- Dimension tables never get duplicate entries for the same name
- Load is wrapped in a transaction (commit on success, rollback on failure)
- Manually verified against a running docker compose Postgres instance, not just 'looks right'"

gh issue create \
  --title "Wire up the Airflow DAG" \
  --label "orchestration" \
  --body "Import the four pipeline functions into dags/drama_warehouse_dag.py, wrap in PythonOperators, set dependency chain.

Acceptance criteria:
- Correct dependency ordering (both extracts must finish before clean_dramas; clean_dramas before load_dramas)
- extract_tmdb has retries configured (network-dependent); extract_mydramalist does not (fails fast on config problems)
- DAG shows up in the Airflow UI and a manually-triggered run completes successfully end to end"

gh issue create \
  --title "End-to-end smoke test + README writeup" \
  --label "docs" \
  --body "Run the full stack for real: docker compose up, trigger the DAG, verify data lands correctly in Postgres.

Acceptance criteria:
- psql query against fact_dramas / fact_drama_tag shows real, correct data
- README's 'Known open questions' section is filled in with your actual decisions (TMDb match/no-match handling, date-ambiguity convention, load-scale limits) and reasoning, not left as questions"

echo "Done. Run 'gh issue list' to confirm."
