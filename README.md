# DBapp (Streamlit + Delta)

## Quick Start

1. Create Delta tables in Databricks SQL:

```
USE CATALOG ashraf;
USE SCHEMA default;

@scripts/002_create_delta_tables.sql
```

2. Seed fake data (Databricks job or notebook):

```
python scripts/003_seed_delta_tables.py
```

3. Run locally:

```
pip install -r streamlit_app/requirements.txt
DB_CATALOG=ashraf DB_SCHEMA=default streamlit run streamlit_app/app.py
```

## Environment Variables

- `DB_CATALOG`: Databricks catalog name (default: `main`)
- `DB_SCHEMA`: Databricks schema name (default: `default`)

## App Structure

- `streamlit_app/app.py`: main dashboard
- `streamlit_app/pages/`: supporting pages (map, export, users, help)
- `streamlit_app/data_access.py`: Delta table access + fallbacks
- `scripts/`: Delta DDL and seed data
