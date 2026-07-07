"""
create_watsonx_project.py
=========================
Creates a new watsonx.ai project under your IBM Cloud account and
prints the Project ID to paste into your .env file.

Run:  python create_watsonx_project.py
"""

import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("IBM_API_KEY", "").strip()
URL     = os.environ.get("IBM_WATSONX_URL", "https://eu-de.ml.cloud.ibm.com").strip()

if not API_KEY or API_KEY == "your-ibm-cloud-api-key-here":
    print("[ERROR] IBM_API_KEY is not set in your .env file.")
    raise SystemExit(1)

# ── Step 1: Get IAM bearer token ─────────────────────────────────────────────
print("[1/3] Obtaining IAM token...")
data = urllib.parse.urlencode({
    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
    "apikey": API_KEY,
}).encode()
req = urllib.request.Request(
    "https://iam.cloud.ibm.com/identity/token",
    data=data,
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=15) as r:
    token = json.loads(r.read())["access_token"]
print("    IAM token obtained.\n")

# ── Step 2: Look up the IBM Cloud account GUID ───────────────────────────────
print("[2/3] Looking up IBM Cloud account ID...")
req2 = urllib.request.Request(
    "https://accounts.cloud.ibm.com/v1/accounts",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
)
with urllib.request.urlopen(req2, timeout=15) as r:
    accounts = json.loads(r.read())

if not accounts.get("resources"):
    print("[ERROR] No IBM Cloud accounts found for this API key.")
    raise SystemExit(1)

account_guid = accounts["resources"][0]["metadata"]["guid"]
print(f"    Account GUID: {account_guid}\n")

# ── Step 3: Create a new watsonx.ai project ───────────────────────────────────
print("[3/3] Creating watsonx.ai project 'RTI-Sahayak'...")
project_body = json.dumps({
    "name": "RTI-Sahayak",
    "description": "RTI Sahayak — AI-powered RTI Filing Assistant",
    "generator": "rti-sahayak-setup",
    "type": "wx",
    "compute": [{"name": "default_spark", "crn": ""}],
    "storage": {"type": "bmcos_object_storage"},
}).encode()

create_req = urllib.request.Request(
    f"{URL}/v2/projects",
    data=project_body,
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    },
    method="POST",
)
try:
    with urllib.request.urlopen(create_req, timeout=20) as r:
        project = json.loads(r.read())

    new_id   = project["metadata"]["guid"]
    new_name = project["entity"]["name"]

    print(f"    Project created: \"{new_name}\"")
    print(f"    Project ID     : {new_id}")
    print()
    print("=" * 60)
    print(" ACTION REQUIRED — update your .env file:")
    print("=" * 60)
    print(f"  IBM_PROJECT_ID={new_id}")
    print(f"  IBM_WATSONX_URL={URL}")
    print(f"  GRANITE_MODEL_ID=ibm/granite-4-h-small")
    print()
    print("Then restart the Flask server:  python app.py")

except urllib.error.HTTPError as e:
    body = e.read().decode(errors="replace")
    print(f"[ERROR] Could not create project (HTTP {e.code}): {body[:400]}")
    print()
    print("You may need to create the project manually:")
    print("  1. Go to https://cloud.ibm.com -> watsonx.ai")
    print("  2. Click 'New project' -> 'Create an empty project'")
    print("  3. Manage tab -> General -> copy the Project ID")
    print("  4. Add it as IBM_PROJECT_ID in your .env file")
