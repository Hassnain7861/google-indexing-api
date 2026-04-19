#!/usr/bin/env python3
"""
Google Indexing API — Bulk URL Submitter
Quota: 200 requests/day per project (default)
Docs: https://developers.google.com/search/apis/indexing-api/v3/quickstart
"""

import json
import time
import sys
from pathlib import Path

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    sys.exit("Missing deps. Run: pip install google-auth google-auth-httplib2 google-api-python-client")

# ── Config ────────────────────────────────────────────────────────────────────
SERVICE_ACCOUNT_FILE = r"d:\Water heater repair\turing-handler-493615-j4-5da6285b02f2.json"
SCOPES               = ["https://www.googleapis.com/auth/indexing"]
BATCH_DELAY_SECONDS  = 1          # pause between requests (be polite to quota)
TYPE                 = "URL_UPDATED"  # or "URL_DELETED"
# ─────────────────────────────────────────────────────────────────────────────


def load_urls(source: str) -> list[str]:
    """Load URLs from a .txt or .json file, or a plain list."""
    p = Path(source)
    if not p.exists():
        sys.exit(f"File not found: {source}")

    if p.suffix == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
        # accept {"urls": [...]} or bare list
        return data["urls"] if isinstance(data, dict) else data
    else:
        return [u.strip() for u in p.read_text(encoding="utf-8").splitlines() if u.strip()]


def build_service(key_file: str):
    creds = service_account.Credentials.from_service_account_file(
        key_file, scopes=SCOPES
    )
    return build("indexing", "v3", credentials=creds, cache_discovery=False)


def submit_url(service, url: str, notification_type: str) -> dict:
    body = {"url": url, "type": notification_type}
    return service.urlNotifications().publish(body=body).execute()


def run(urls_file: str):
    urls = load_urls(urls_file)
    print(f"Loaded {len(urls)} URLs from {urls_file}\n")

    service = build_service(SERVICE_ACCOUNT_FILE)

    results = {"success": [], "error": []}

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}", end=" ... ", flush=True)
        try:
            resp = submit_url(service, url, TYPE)
            notify_time = resp.get("urlNotificationMetadata", {}).get(
                "latestUpdate", {}).get("notifyTime", "")
            print(f"OK  ({notify_time})")
            results["success"].append(url)
        except HttpError as e:
            msg = json.loads(e.content).get("error", {}).get("message", str(e))
            print(f"FAIL  {e.status_code} — {msg}")
            results["error"].append({"url": url, "error": msg})
        except Exception as e:
            print(f"FAIL  {e}")
            results["error"].append({"url": url, "error": str(e)})

        if i < len(urls):
            time.sleep(BATCH_DELAY_SECONDS)

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'-'*50}")
    print(f"Done.  Success: {len(results['success'])}  |  Failed: {len(results['error'])}")

    report_path = Path("indexing_report.json")
    report_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Report saved -> {report_path}")

    if results["error"]:
        failed_path = Path("failed_urls.txt")
        failed_path.write_text(
            "\n".join(e["url"] for e in results["error"]), encoding="utf-8"
        )
        print(f"Failed URLs  -> {failed_path}  (re-run against this file to retry)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python bulk_index.py urls.txt")
    run(sys.argv[1])
