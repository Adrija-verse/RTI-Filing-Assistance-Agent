"""
diagnose_credentials.py
Run: python diagnose_credentials.py

Checks your .env credentials and tells you exactly what is wrong and how to fix it.
"""

import os
import sys

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

api_key    = os.environ.get("IBM_API_KEY", "").strip()
project_id = os.environ.get("IBM_PROJECT_ID", "").strip()
url        = os.environ.get("IBM_WATSONX_URL", "").strip()
model_id   = os.environ.get("GRANITE_MODEL_ID", "ibm/granite-3-3-8b-instruct").strip()

SEP = "=" * 60

def masked(s):
    if len(s) > 12:
        return s[:6] + "..." + s[-4:]
    return "(too short / empty)"

print(SEP)
print(" RTI Sahayak — IBM Credential Diagnostic")
print(SEP)
print(f"  IBM_API_KEY      : {masked(api_key)}")
print(f"  IBM_PROJECT_ID   : {project_id}")
print(f"  IBM_WATSONX_URL  : {url}")
print(f"  GRANITE_MODEL_ID : {model_id}")
print()

# ── Step 1: Check for placeholder / empty values ─────────────────────────────
issues = []
if not api_key or api_key == "your-ibm-cloud-api-key-here":
    issues.append("IBM_API_KEY is missing or still set to the placeholder value.")
if not project_id or project_id == "your-watsonx-project-id-here":
    issues.append("IBM_PROJECT_ID is missing or still set to the placeholder value.")
if not url:
    issues.append("IBM_WATSONX_URL is not set. Use: https://us-south.ml.cloud.ibm.com")

if issues:
    print("[FAIL] Configuration problems in your .env file:")
    for issue in issues:
        print(f"  - {issue}")
    print()
    print("Fix: Edit your .env file (not .env.example) and update the values,")
    print("     then restart the Flask server.")
    sys.exit(1)

print("[OK] .env values are set. Testing connection to IBM Cloud...")
print()

# ── Step 2: Get IAM bearer token (validates the API key) ─────────────────────
import urllib.request
import urllib.parse
import json

iam_url = "https://iam.cloud.ibm.com/identity/token"
data = urllib.parse.urlencode({
    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
    "apikey": api_key,
}).encode()

try:
    req = urllib.request.Request(
        iam_url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        token_data = json.loads(resp.read())
    token = token_data.get("access_token", "")
    print("[OK] IBM Cloud API key is valid. IAM token obtained.")
except urllib.error.HTTPError as e:
    body = e.read().decode(errors="replace")
    print(f"[FAIL] IBM Cloud API key rejected (HTTP {e.code}).")
    print(f"       Response: {body[:300]}")
    print()
    print("Fix:")
    print("  1. Go to https://cloud.ibm.com")
    print("  2. Manage -> Access (IAM) -> API keys")
    print("  3. Create a new API key, copy it, and update IBM_API_KEY in .env")
    sys.exit(1)
except Exception as e:
    print(f"[FAIL] Could not reach IBM IAM service: {e}")
    print("       Check your internet connection.")
    sys.exit(1)

# ── Step 3: Check the project ID against the configured URL ──────────────────
print(f"[..] Checking Project ID '{project_id}' at {url} ...")

REGIONS = {
    "us-south": "https://us-south.ml.cloud.ibm.com",
    "eu-de":    "https://eu-de.ml.cloud.ibm.com",
    "jp-tok":   "https://jp-tok.ml.cloud.ibm.com",
    "au-syd":   "https://au-syd.ml.cloud.ibm.com",
    "eu-gb":    "https://eu-gb.ml.cloud.ibm.com",
    "ca-tor":   "https://ca-tor.ml.cloud.ibm.com",
}

found_in_region = None

for region_name, region_url in REGIONS.items():
    check_url = f"{region_url}/v2/projects/{project_id}"
    req = urllib.request.Request(
        check_url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            proj_data = json.loads(resp.read())
        proj_name = proj_data.get("entity", {}).get("name", "(unknown)")
        found_in_region = region_name
        print(f"[OK] Project found in region '{region_name}'!")
        print(f"     Project name : {proj_name}")
        print(f"     Project ID   : {project_id}")
        print(f"     Correct URL  : {region_url}")
        print()
        if region_url.rstrip("/") != url.rstrip("/"):
            print("[MISMATCH] Your IBM_WATSONX_URL is wrong!")
            print(f"  Current  : {url}")
            print(f"  Required : {region_url}")
            print()
            print("Fix: Update your .env file:")
            print(f"  IBM_WATSONX_URL={region_url}")
            print("  Then restart the Flask server.")
        else:
            print("[OK] IBM_WATSONX_URL matches the project region.")
            print()
            print("[OK] All credentials look correct!")
            print("     If you still get errors, restart the Flask server so")
            print("     the updated .env is reloaded.")
        break
    except urllib.error.HTTPError as e:
        if e.code == 404:
            continue   # not in this region, try next
        # other error — stop
        body = e.read().decode(errors="replace")
        print(f"[WARN] HTTP {e.code} from {region_name}: {body[:200]}")
        break
    except Exception:
        continue

if found_in_region is None:
    print("[FAIL] Project not found in any IBM Cloud region.")
    print()
    print("The project ID may be wrong or the project may have been deleted.")
    print()
    print("Fix:")
    print("  1. Go to https://cloud.ibm.com and open watsonx.ai")
    print("  2. Open your project -> Manage tab -> General")
    print("  3. Copy the Project ID UUID")
    print("  4. Update IBM_PROJECT_ID in your .env file")
    print("  5. Restart the Flask server")
