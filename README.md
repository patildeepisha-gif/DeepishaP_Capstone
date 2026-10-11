# Mamaearth Regional Operations & Finance Pipeline

This repository contains an end-to-end data pipeline, exploratory data analysis suite, SQLite relational store, and a GenAI-powered executive narrative generator (following the Situation–Complication–Resolution framework) equipped with a fully keyless offline fallback.

---

## Repository Structure

```text
├── datacustomers.csv          # Raw customer demographic data
├── dataorders.csv             # Raw order transactional data
├── dataproducts.csv           # Raw product catalog data
├── sql/
│   ├── schema.sql             # Relational table schemas with foreign keys
│   ├── seed_data.sql          # Seed data insertion statements
│   └── reports.sql            # Analytical SQL queries & expected outputs
├── analysis/
│   ├── clean_and_eda.py       # Data cleaning, EDA, IQR outliers, & findings exporter
│   └── visualize.py           # Matplotlib visualization generator
├── narrator/
│   ├── findings.json          # Automatically exported verified metrics
│   ├── generate_narrative.py  # GenAI SCR narrator with keyless offline fallback
│   └── sample_output.txt      # Saved sample narrative output for validation
└── visualizations/            # Generated PNG charts

# 1. Create database schema
sqlite3 db.sqlite < sql/schema.sql

# 2. Insert seed data
sqlite3 db.sqlite < sql/seed_data.sql

# 3. Execute analytical report queries
sqlite3 db.sqlite < sql/reports.sql

# Run data cleaning, EDA, and export narrator/findings.json
python analysis/clean_and_eda.py

# Generate and save analysis visualizations to visualizations/
python analysis/visualize.py

python narrator/generate_narrative.py

export GEMINI_API_KEY="your_free_api_key_here"
python narrator/generate_narrative.py
