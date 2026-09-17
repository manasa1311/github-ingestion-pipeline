# GitHub API Data Ingestion Pipeline

A Python data pipeline that fetches repository data from the GitHub REST API for multiple users and persists it to JSON, CSV, and PostgreSQL — with proper pagination, authentication, error handling, logging, and config-driven batch processing.

## What it does

1. Authenticates with the GitHub API using a personal access token
2. Fetches all public repositories for a configurable list of usernames, handling pagination automatically
3. Processes users in a batch — one failed username doesn't stop the whole run
4. Saves results to:
   - `<username>_repos.json` — full raw data per user
   - `<username>_repos.csv` — flattened key fields per user
   - PostgreSQL (`repos` table) — queryable, persistent storage
5. Logs every step (successes, failures, timeouts, batch summary) to `pipeline.log`

## Tech stack

- Python 3.10
- `requests` — HTTP calls to the GitHub API
- `psycopg2` — PostgreSQL driver
- `python-dotenv` — environment variable management
- PostgreSQL — persistent storage
- Built-in `json`, `csv`, `logging` modules

## Project structure

```
github-ingestion-pipeline/
├── main.py            # Orchestrates the pipeline: config -> fetch -> save
├── github_client.py   # GitHubClient class: auth, requests, pagination
├── storage.py          # Save results to JSON and CSV
├── database.py         # PostgreSQL connection, table setup, inserts
├── config.py           # Loads config.json
├── config.json          # Non-secret settings (usernames, per_page)
├── requirements.txt     # Python dependencies
└── .gitignore
```

## Setup

**1. Clone and enter the project**
```bash
git clone https://github.com/manasa1311/github-ingestion-pipeline.git
cd github-ingestion-pipeline
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create a `.env` file** in the project root:
```
GITHUB_TOKEN=your_github_personal_access_token
DB_NAME=github_pipeline
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

**5. Create the PostgreSQL database** (one-time):
```sql
CREATE DATABASE github_pipeline;
```

**6. Configure which users to fetch**, in `config.json`:
```json
{
    "usernames": ["torvalds", "gvanrossum"],
    "per_page": 5
}
```

## Usage

```bash
python main.py
```

Output includes per-user JSON/CSV files, rows inserted into the `repos` table, and a full run log in `pipeline.log`.

## Design notes

- **Pagination**: GitHub returns results in pages; the client loops until an empty page signals the end, rather than assuming a fixed count.
- **Error isolation**: each API call is wrapped in specific exception handling (`Timeout`, `ConnectionError`, `HTTPError`), so a single bad username or network blip doesn't crash the whole batch — it's logged and the run continues.
- **Secrets vs. config**: `.env` holds credentials (never committed); `config.json` holds non-secret run settings (safe to commit, easy to change without touching code).
- **Parameterized SQL**: all database inserts use placeholders (`%s`), not string formatting, to prevent SQL injection.

## Possible extensions

- Retry logic with exponential backoff for transient failures
- Incremental/delta fetching instead of full re-fetch each run
- Dockerize for easier deployment
- Schedule via cron / Task Scheduler for automatic periodic runs
