# dbt-analytics-portfolio1
# dbt Analytics Engineering Portfolio

## Overview
This project demonstrates an end-to-end analytics engineering workflow for a SaaS business, including data modeling, transformation, churn analysis, and executive dashboards.

## Architecture
Raw CSV data is loaded into DuckDB, transformed using dbt Core, analyzed via Python, and surfaced through BI dashboards.

## Key Features
- dbt Core models with tests and snapshots
- SaaS GTM metrics (ARR, churn, revenue)
- Churn propensity modeling
- Executive dashboards

## Tools
- DuckDB
- dbt Core
- Python (pandas, scikit-learn)
- Evidence.dev
- GitHub Pages

## How to Run
1. Generate data: `python scripts/generate_data.py`
2. Load data: `python scripts/load_data.py`
3. Run dbt: `dbt run && dbt test && dbt snapshot`
4. Launch notebooks: `jupyter notebook`
