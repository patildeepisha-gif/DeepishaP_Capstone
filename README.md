# Mamaearth Regional Operations & Finance Pipeline

This repository contains an end-to-end data pipeline for Mamaearth
regional operations and finance. It loads raw customer, order, and
product data into SQLite, runs analytical SQL reports, performs data
cleaning and exploratory data analysis (EDA), generates visualizations,
and produces an executive narrative using the
Situation--Complication--Resolution (SCR) framework. The narrative
generator also supports a keyless offline fallback.

Run every command below from the repository root. Use the same database
file (`db.sqlite`) throughout so the SQL reports and analysis use the
same data.

## Prerequisites

-   Python 3 installed and available as `python` (or use `python3` on
    macOS/Linux if that is your command).
-   SQLite command-line utility (`sqlite3`).
-   The repository's CSV files and scripts in the structure shown below.
-   For AI-generated narrative only: a Gemini API key. A key is **not**
    required for offline mode.

If the Python scripts require third-party packages, install the
dependencies listed by the project (for example, from `requirements.txt`
if one is provided) before running the pipeline.

## 1. Create and populate the SQLite database, then run the SQL reports

First create the database schema, then insert the seed data, and finally
execute the analytical report queries. Run these commands in this exact
order:

``` bash
sqlite3 db.sqlite < sql/schema.sql
sqlite3 db.sqlite < sql/seed_data.sql
sqlite3 db.sqlite < sql/reports.sql
```

-   `sql/schema.sql` creates the relational tables and their foreign-key
    relationships.
-   `sql/seed_data.sql` inserts the seed records used by the analysis.
-   `sql/reports.sql` executes the analytical SQL queries and prints
    their outputs in the terminal.

Keep the resulting `db.sqlite` file. If you want to rebuild the database
from scratch, remove or rename the existing `db.sqlite` file before
running these commands again. Do not delete it between pipeline stages.

## 2. Run data cleaning and EDA, then generate visualizations

Run the cleaning and exploratory analysis script first:

``` bash
python analysis/clean_and_eda.py
```

This step cleans the input data, performs EDA and IQR-based outlier
checks, reports findings, and exports the verified metrics used by the
narrative generator to:

``` text
narrator/findings.json
```

**Part 2, Task 5 writes `narrator/findings.json`.** Run Task 5 before
generating the narrative. If `findings.json` is missing or outdated,
rerun `analysis/clean_and_eda.py` first so the narrative is based on the
current analysis outputs.

Next, create the charts:

``` bash
python analysis/visualize.py
```

The visualization script generates PNG charts in the `visualizations/`
directory. Run it after the cleaning/EDA step so the charts reflect the
current dataset and analysis.

## 3. Generate the executive narrative (Gemini API or offline)

Run the narrative generator from the repository root:

``` bash
python narrator/generate_narrative.py
```

### Option A --- Use Gemini with an API key

Set your Gemini API key as an environment variable named
`GEMINI_API_KEY`, then run the script. Do not put the key directly into
this README or commit it to source control.

**macOS/Linux (bash or zsh):**

``` bash
export GEMINI_API_KEY="your_gemini_api_key"
python narrator/generate_narrative.py
```

**Windows PowerShell:**

``` powershell
$env:GEMINI_API_KEY = "your_gemini_api_key"
python narrator/generate_narrative.py
```

**Windows Command Prompt (cmd.exe):**

``` bat
set GEMINI_API_KEY=your_gemini_api_key
python narrator/generate_narrative.py
```

The script can then use Gemini to generate the executive narrative from
the verified metrics in `narrator/findings.json`.

### Option B --- Run offline with no API key

If `GEMINI_API_KEY` is not set, run the same command without configuring
a key:

``` bash
python narrator/generate_narrative.py
```

The generator's keyless offline fallback produces a narrative without
calling Gemini. This is useful when an API key is unavailable or network
access is not desired. The offline output is intended to remain
reproducible from the locally generated findings.

The narrative output can be compared with the checked-in sample at
`narrator/sample_output.txt`, if present.

## Reproducing the pipeline from start to finish

From the repository root, execute the following sequence in order:

``` bash
sqlite3 db.sqlite < sql/schema.sql
sqlite3 db.sqlite < sql/seed_data.sql
sqlite3 db.sqlite < sql/reports.sql
python analysis/clean_and_eda.py
python analysis/visualize.py
python narrator/generate_narrative.py
```

For an AI-generated narrative, set `GEMINI_API_KEY` in the current
terminal session before the final command. For a keyless offline
narrative, leave `GEMINI_API_KEY` unset.

To reproduce the figures and metrics in the project brief, use the same
source CSV files and run the complete sequence from the repository root.
The SQL report outputs, `narrator/findings.json`, generated charts in
`visualizations/`, and narrative output are the corresponding artifacts
to inspect. If the CSV files, scripts, or seed data change, rerun the
pipeline from Step 1 so every downstream artifact is regenerated from
the same inputs.

## Repository structure

``` text
.
├── datacustomers.csv
├── dataorders.csv
├── dataproducts.csv
├── db.sqlite                 # Created by the SQL commands above
├── sql/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── reports.sql
├── analysis/
│   ├── clean_and_eda.py
│   └── visualize.py
├── narrator/
│   ├── findings.json         # Written by Part 2, Task 5 / clean_and_eda.py
│   ├── generate_narrative.py
│   └── sample_output.txt
└── visualizations/            # Generated PNG charts
```
