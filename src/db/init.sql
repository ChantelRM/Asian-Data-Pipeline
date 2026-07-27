-- Star schema for the Asian Drama Analytics Warehouse.
--
-- YOUR TASK: write the CREATE TABLE statements for the tables listed
-- below. This file gets mounted into the warehouse Postgres container
-- and run automatically on first startup (docker-entrypoint-initdb.d),
-- so whatever you write here IS your schema.
--
-- DESIGN CONSTRAINT TO KEEP: tags are multi-valued per drama (a single
-- drama can be "Romance, BL, School, 2023"). Don't put a comma-separated
-- string column on fact_dramas for this — that turns "average rating of
-- BL dramas" into ugly string matching instead of a join. Use a proper
-- bridge/associative table (fact_drama_tag) for the many-to-many
-- instead. This is the textbook way to handle multi-valued dimensions
-- in a star schema, and it's the one design choice in this whole
-- project most likely to get scrutinized in a review — get it right.

CREATE SCHEMA IF NOT EXISTS warehouse;
SET search_path TO warehouse;

-- dim_country
--   country_id (PK), country_name (unique, not null)

-- dim_genre_tag
--   tag_id (PK), tag_name (unique, not null)
--   tag_type -- think about distinguishing a genre tag (Romance,
--   Thriller) from a content flag (BL, GL) from a setting tag (School,
--   Medical). Why might that distinction matter for a query later?

-- dim_network_platform
--   platform_id (PK), platform_name (unique, not null)
--   platform_type -- e.g. broadcast_tv vs streaming vs unknown

-- dim_date
--   date_id (PK), full_date (unique, not null), year, quarter, month, day
--   Think about why you'd want year/quarter/month/day as separate
--   columns rather than just full_date -- what kind of query does this
--   make faster or easier to write?

-- fact_dramas
--   drama_id (PK)
--   source_title_key -- natural key, MUST be unique: this is what your
--   load step upserts on for idempotency. Get this wrong and re-running
--   the DAG will duplicate every drama.
--   title, country_id (FK), network_platform_id (FK), air_date_id (FK)
--   episode_count, rating, popularity, review_sentiment_count
--   tmdb_id, tmdb_poster_path -- from the TMDb enrichment
--   source_system, load_timestamp -- for auditability: which pipeline
--   run loaded/updated this row, and when?

-- fact_drama_tag
--   drama_id (FK), tag_id (FK), composite PK on both
--   This is the bridge table solving the multi-valued tag problem
--   described above.

-- TODO: write the actual CREATE TABLE statements for all six tables.
-- Consider adding indexes on foreign key columns you expect to filter
-- or join on frequently (country_id, air_date_id, tag_id) -- think
-- about which analytical queries you'd actually want to run fast
-- ("do BL dramas rate higher", "Thai output growth by year") and let
-- that guide which indexes are worth adding.
