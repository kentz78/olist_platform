"""
scripts/delete_bq_datasets.py
Delete all four Olist BigQuery datasets and every table inside them.

Requires typing YES at the confirmation prompt — prevents accidental data loss.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

PROJECT = os.environ.get("GCP_PROJECT_ID")
if not PROJECT:
    print("❌  GCP_PROJECT_ID is not set in .env")
    sys.exit(1)

DATASETS = [
    "olist_raw",
    "olist_analytics",
    "olist_analytics_staging",
    "olist_analytics_marts",
]

print(f"Project : {PROJECT}")
print()
print("⚠️  This will PERMANENTLY DELETE the following datasets and all their tables:")
for ds in DATASETS:
    print(f"   • {PROJECT}.{ds}")
print()
answer = input("Type YES to confirm deletion, anything else to abort: ").strip()
if answer != "YES":
    print("Aborted — nothing deleted.")
    sys.exit(0)

print()
client = bigquery.Client(project=PROJECT)
for dataset_id in DATASETS:
    full_id = f"{PROJECT}.{dataset_id}"
    client.delete_dataset(full_id, delete_contents=True, not_found_ok=True)
    print(f"  🗑️  Deleted {full_id}")

print()
print("Done.")
