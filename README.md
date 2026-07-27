# Asian Drama Analytics Warehouse — Starter Kit

![CI](https://github.com/ChantelRM/Asian-Data-Pipleine/actions/workflows/ci.yml/badge.svg)

A skeleton for a data warehouse combining a batch Kaggle CSV and a live
TMDb API source into a Postgres star schema, orchestrated by Airflow.

**This repo is intentionally unimplemented.** Infra config
(`docker-compose.yml`, `.env.example`, `requirements.txt`) is provided
as-is since that's just wiring, not the learning target. Everything
under `src/` and `dags/` has function signatures, docstrings describing
what each piece needs to do, and `TODO`/`NotImplementedError` markers —
you write the logic. `tests/` is real and complete: treat it as your
spec, and run it constantly as a TDD loop while you build.

## Target architecture (what you're building toward)

```
extract_mydramalist.py --\
                           >--> clean_dramas.py --> load_postgres.py --> Postgres (star schema)
extract_tmdb.py ----------/
```

- **Batch source**: "Complete 5000 dramas from MyDramaList" (Kaggle CSV)
- **Live source**: TMDb's public API
- **Validation**: pandera schema contracts at each stage boundary
- **Warehouse**: Postgres star schema — `fact_dramas` + `fact_drama_tag`
  (bridge table for the many-to-many genre/tag relationship) +
  `dim_country`, `dim_genre_tag`, `dim_network_platform`, `dim_date`
- **Orchestration**: Airflow DAG, one task per pipeline stage
- **Idempotency**: dimension get-or-create + fact upsert on a natural
  key, so re-running the DAG never duplicates rows

## CI and issue tracking

`.github/workflows/ci.yml` runs `pytest tests/test_schemas.py
tests/test_transform.py` on every push and PR — the two test files that
don't need live infra. `load_postgres.py` correctness is verified
manually against a running `docker compose` stack, not in CI.

To get a task board of GitHub Issues matching the build order above:
after pushing this repo to GitHub, install the [GitHub
CLI](https://cli.github.com/), run `gh auth login`, then from the repo
root run:

```bash
chmod +x scripts/create_issues.sh
./scripts/create_issues.sh
```

This creates one labeled issue per build task (schema-design, extract,
transform, load, orchestration, docs), each with acceptance criteria
tied to specific tests. From there you can either work the GitHub
Issues list directly, or turn on a repo Project board (Issues tab →
Projects → new board) and drag issues into To Do / In Progress / Done
columns for a visual Kanban view.

## Suggested build order

1. `src/db/init.sql` — design the actual table DDL from the column
   lists given as comments.
2. `src/schemas/contracts.py` — define the three pandera schemas.
3. `src/transform/clean_dramas.py`'s three small helper functions
   (`_parse_tags`, `_parse_air_date`, `_make_source_title_key`) —
   `pytest tests/test_transform.py -v` as you go, this is designed to
   be a tight loop.
4. `src/extract/extract_mydramalist.py` — once you've got the CSV
   downloaded and looked at its real columns.
5. `src/extract/extract_tmdb.py` — once you have a TMDb API key.
6. `clean_dramas()` (the orchestrating function) — wires 3+4+5 together.
7. `src/load/load_postgres.py` — hardest to unit test; budget real time
   with `docker compose up` and manually inspecting tables.
8. `dags/drama_warehouse_dag.py` — wire the four stages together.

## Setup

1. Download the "Complete 5000 dramas from MyDramaList" Kaggle dataset,
   place the CSV at `data/raw/mydramalist.csv`. Check its actual column
   names before writing your schema — don't assume.
2. Get a free TMDb API key: https://www.themoviedb.org/settings/api
3. `cp .env.example .env` and fill in `TMDB_API_KEY`.
4. `docker compose up -d` once you've written `init.sql` and the DAG.
5. Airflow UI at `http://localhost:8080` (default admin/admin — change
   before this is ever on a shared machine).

## Running stages individually (without Airflow, for local debugging)

```bash
pip install -r requirements.txt
python -m src.extract.extract_mydramalist
python -m src.extract.extract_tmdb
python -m src.transform.clean_dramas
python -m src.load.load_postgres
pytest tests/ -v
```

## Known open questions to resolve yourself, not solve here

- How should TMDb title matching handle titles with no confident match?
  Drop them, or keep them with null enrichment? What does each choice
  do to a later "do BL dramas rate higher" query?
- What's your actual convention for ambiguous `DD/MM/YYYY` vs
  `MM/DD/YYYY` date strings, and where do you document that choice?
- At what data volume would row-by-row loading stop being fine, and
  what would you switch to?

Document whatever you land on in this README once it's real — a
grader (or future you) should be able to read your reasoning, not just
your code.
