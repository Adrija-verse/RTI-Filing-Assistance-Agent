"""
list_watsonx_resources.py — lists all projects and available Granite models
Run: python list_watsonx_resources.py
"""
import os, urllib.request, urllib.parse, json
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get("IBM_API_KEY", "").strip()

# ── Get IAM token ────────────────────────────────────────────────────────────
data = urllib.parse.urlencode({
    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
    "apikey": api_key,
}).encode()
req = urllib.request.Request(
    "https://iam.cloud.ibm.com/identity/token", data=data,
    headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST",
)
with urllib.request.urlopen(req, timeout=15) as r:
    token = json.loads(r.read())["access_token"]
print("[OK] IAM token obtained\n")

REGIONS = {
    "eu-de":   "https://eu-de.ml.cloud.ibm.com",
    "us-south": "https://us-south.ml.cloud.ibm.com",
    "jp-tok":   "https://jp-tok.ml.cloud.ibm.com",
    "au-syd":   "https://au-syd.ml.cloud.ibm.com",
}

headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# ── List all projects in each region ─────────────────────────────────────────
print("=" * 60)
print(" YOUR watsonx.ai PROJECTS")
print("=" * 60)
for region, base in REGIONS.items():
    req2 = urllib.request.Request(f"{base}/v2/projects", headers=headers)
    try:
        with urllib.request.urlopen(req2, timeout=10) as r:
            projects = json.loads(r.read()).get("resources", [])
        if projects:
            for p in projects:
                guid = p["metadata"]["guid"]
                name = p["entity"]["name"]
                print(f"  [{region}]  {guid}  \"{name}\"")
        else:
            print(f"  [{region}]  (no projects found)")
    except Exception as e:
        print(f"  [{region}]  Error: {e}")

# ── List available foundation models at eu-de ─────────────────────────────────
print()
print("=" * 60)
print(" AVAILABLE FOUNDATION MODELS (eu-de)")
print("=" * 60)
base_eu = "https://eu-de.ml.cloud.ibm.com"
req3 = urllib.request.Request(
    f"{base_eu}/ml/v1/foundation_model_specs?version=2024-01-01&limit=200",
    headers=headers,
)
try:
    with urllib.request.urlopen(req3, timeout=15) as r:
        models = json.loads(r.read()).get("resources", [])
    granite = [m["model_id"] for m in models if "granite" in m.get("model_id","").lower()]
    print(f"\n  Granite models available ({len(granite)} found):")
    for m in granite:
        print(f"    {m}")
    if not granite:
        print("  (no granite models found — listing all models)")
        for m in models[:20]:
            print(f"    {m['model_id']}")
except Exception as e:
    print(f"  Error listing models: {e}")
