# ⚖️ RTI Sahayak — AI-Powered RTI Filing Assistant

**RTI Sahayak** is a full-stack web application built with **Python Flask** and **IBM watsonx.ai (Granite models)** that helps Indian citizens exercise their Right to Information under the **RTI Act, 2005**. It features a conversational AI chat interface, an application status dashboard, a deadline tracker, and a First Appeal generator — all grounded in retrieved legal text via RAG.

> Built as part of the **IBM SkillsBuild for University Engagements** internship program, **AICTE 2026**.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#️-architecture)
- [Fork & Clone](#-fork--clone)
- [Quick Start](#-quick-start)
- [Customising the Agent](#-customising-the-agent-agent_instructions)
- [API Reference](#-api-reference)
- [Deployment on IBM Cloud](#️-deployment-on-ibm-cloud-lite-tier)
- [Knowledge Base](#-knowledge-base)
- [Troubleshooting](#-troubleshooting)
- [Disclaimer](#️-disclaimer)

---

## ✨ Features

| Feature | Description |
|---|---|
| 💬 **AI Chat (RAG)** | Describe your issue in plain language; Granite AI identifies the department, drafts RTI applications, and answers legal questions — grounded in the RTI Act knowledge base |
| 📊 **Status Dashboard** | Table view of all applications with colour-coded status: 🟢 On Track · 🟡 Due Soon · 🔴 Overdue |
| 🗓️ **Deadline Tracker** | Calculates the 30-day (standard) or 48-hour (life/liberty) statutory deadline from your filing date |
| 📣 **First Appeal Generator** | Auto-drafts a Section 19(1) First Appeal for overdue applications, with one click |
| 🔧 **AGENT_INSTRUCTIONS** | Single block in `agent/rti_agent.py` to customise tone, drafting rules, escalation timing, and knowledge sources |
| 🗃️ **SQLite Persistence** | All drafted applications saved to a local SQLite database for tracking |

---

## 🏗️ Architecture

```
RTI Sahayak/
├── app.py                          # Flask app + all routes (pages + REST API)
├── requirements.txt
├── .env.example                    # Copy → .env and fill in IBM credentials
│
├── agent/
│   └── rti_agent.py                # AGENT_INSTRUCTIONS block + watsonx.ai client + RTISahayakAgent
│
├── knowledge_base/
│   └── rti_act_provisions.py       # RTI Act 2005 text chunks + PIO directory + fee rules + dept mapping
│
├── rti_tools/
│   ├── rag.py                      # FAISS + sentence-transformers RAG retrieval (local, no API cost)
│   ├── drafting.py                 # Application & First Appeal template utilities
│   └── database.py                 # SQLite schema + CRUD helpers
│
├── templates/
│   ├── index.html                  # Chat UI (Bootstrap dark, sidebar, typing indicator)
│   ├── dashboard.html              # Application status dashboard (colour-coded table)
│   └── application_detail.html    # Single application view + First Appeal panel
│
└── instance/
    └── rti_sahayak.db              # SQLite database (auto-created on first run)
```

**RAG → Granite pipeline:**
```
User message
    │
    ▼
FAISS similarity search (sentence-transformers, local)
    │
    └─► Top-5 RTI Act chunks → injected into Granite system prompt
                │
                ▼
        IBM watsonx.ai Granite model
                │
                ▼
        Grounded response (draft / legal info / escalation)
```

---

## 🍴 Fork & Clone

### Option A — Fork it (recommended if you plan to modify or contribute)

1. Open the repository: **https://github.com/Adrija-verse/RTI-Filing-Assistance-Agent**
2. Click the **Fork** button in the top-right corner of the page — this creates your own copy under your GitHub account.
3. Clone **your fork** (not the original) to your machine:

   ```bash
   git clone https://github.com/<your-username>/RTI-Filing-Assistance-Agent.git
   cd RTI-Filing-Assistance-Agent
   ```

4. *(Optional)* Add the original repo as an `upstream` remote, so you can pull future updates from it:

   ```bash
   git remote add upstream https://github.com/Adrija-verse/RTI-Filing-Assistance-Agent.git
   git remote -v   # confirm both origin (yours) and upstream (original) are set
   ```

   To pull future updates from the original repo into your fork:
   ```bash
   git fetch upstream
   git merge upstream/main
   ```

### Option B — Just clone it (if you only want to run it locally, not contribute back)

```bash
git clone https://github.com/Adrija-verse/RTI-Filing-Assistance-Agent.git
cd RTI-Filing-Assistance-Agent
```

### Option C — Download as ZIP (no Git required)

1. Go to **https://github.com/Adrija-verse/RTI-Filing-Assistance-Agent**
2. Click **Code → Download ZIP**
3. Extract the ZIP and open a terminal inside the extracted folder

---

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.10+**
- **Git** (for cloning; not required if you downloaded the ZIP)
- An **IBM Cloud account** with watsonx.ai enabled
- A **watsonx.ai project** (free Lite tier available)

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Activate it:
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows (PowerShell/CMD)
```

You should see `(venv)` appear at the start of your terminal prompt once activated.

### 3. Get IBM credentials

1. Log into [IBM Cloud](https://cloud.ibm.com)
2. Navigate to **watsonx.ai** → open your project → copy the **Project ID**
3. Go to **Manage → Access (IAM) → API Keys** → create a new API key and copy it
4. Note your regional URL (e.g., `https://us-south.ml.cloud.ibm.com` or `https://eu-de.ml.cloud.ibm.com`)
5. *(Optional)* Run `python list_watsonx_resources.py` after setting up your `.env` (next step) to see which Granite models are available in your region.

### 4. Configure the environment

Copy the example file and fill in your real credentials:

```bash
cp .env.example .env
```

Edit `.env` with a text editor:

```env
# IBM watsonx.ai credentials
IBM_API_KEY=your-ibm-cloud-api-key-here
IBM_PROJECT_ID=your-watsonx-project-id-here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Flask settings
FLASK_SECRET_KEY=change-this-to-a-random-secret
FLASK_DEBUG=false

# Granite model available in your region
GRANITE_MODEL_ID=ibm/granite-3-3-8b-instruct
```

> ⚠️ **Never commit your `.env` file.** It's already listed in `.gitignore` — double check with `git status` before your first commit that it doesn't appear as a tracked file.

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

> The first run also downloads the `all-MiniLM-L6-v2` sentence-transformer model (~80 MB) for local RAG embeddings — this happens automatically and only once.

### 6. Verify your setup (optional but recommended)

```bash
python diagnose_credentials.py
```

This checks that your `.env` values are correctly formatted and that IBM Cloud accepts your API key before you try running the full app.

### 7. Run the application

```bash
# Development mode
python app.py

# Production mode (using Gunicorn)
gunicorn -w 2 -b 0.0.0.0:8080 app:app
```

Open your browser at:
- **http://localhost:5000** (development mode)
- **http://localhost:8080** (production/Gunicorn mode)

You should see the RTI Sahayak chat interface load, with the sidebar showing quick actions, deadline tracker, and links to the dashboard.

---

## 🔧 Customising the Agent (AGENT_INSTRUCTIONS)

Open [`agent/rti_agent.py`](agent/rti_agent.py) and edit the `AGENT_INSTRUCTIONS` dictionary at the top of the file:

```python
AGENT_INSTRUCTIONS = {
    "name": "RTI Sahayak",
    "persona": "...",          # Who the agent is
    "tone": "...",             # Communication style
    "drafting_rules": "...",   # Legal drafting constraints
    "clarification_policy": "...",  # When/how to ask for missing info
    "department_policy": "...",     # How to identify departments
    "escalation_rules": "...",      # Deadline → appeal timing logic
    "knowledge_sources": "...",     # What knowledge sources to cite
    "out_of_scope": "...",          # How to handle non-RTI queries
}
```

No code changes needed elsewhere — the system prompt is assembled automatically from this dictionary. After editing, just restart the Flask server for changes to take effect.

---

## 🌐 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Chat UI |
| `GET` | `/dashboard` | Application dashboard |
| `GET` | `/application/<id>` | Application detail + First Appeal panel |
| `POST` | `/api/chat` | `{ message }` → `{ reply }` |
| `POST` | `/api/chat/reset` | Clear conversation history |
| `POST` | `/api/deadline` | `{ filing_date, life_or_liberty }` → deadline info |
| `POST` | `/api/draft/application` | Draft + save RTI application |
| `POST` | `/api/draft/appeal` | Draft First Appeal under Section 19 |
| `GET` | `/api/applications` | All applications (JSON) |

---

## ☁️ Deployment on IBM Cloud (Lite tier)

### Option A — IBM Code Engine (recommended)

```bash
# 1. Build container
docker build -t rti-sahayak .

# 2. Push to IBM Container Registry
ibmcloud cr push us.icr.io/<namespace>/rti-sahayak:latest

# 3. Deploy to Code Engine
ibmcloud ce application create \
  --name rti-sahayak \
  --image us.icr.io/<namespace>/rti-sahayak:latest \
  --port 8080 \
  --env IBM_API_KEY=xxx \
  --env IBM_PROJECT_ID=xxx \
  --env IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com \
  --env FLASK_SECRET_KEY=xxx \
  --env GRANITE_MODEL_ID=ibm/granite-3-3-8b-instruct
```

### Option B — IBM Cloud Foundry

```bash
# manifest.yml already provided
ibmcloud cf push rti-sahayak
```

### Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]
```

---

## 📚 Knowledge Base

The RTI Act knowledge base is in [`knowledge_base/rti_act_provisions.py`](knowledge_base/rti_act_provisions.py). It contains structured chunks covering:

- Sections 2, 3, 4, 5, 6, 7, 8, 19, 20 of the RTI Act, 2005
- Right to Information (Regulation of Fee and Cost) Rules, 2005
- PIO Directory — 14 key Central Government ministries
- Common citizen issue → department mapping (pension, EPFO, passport, railway, AADHAAR, etc.)

To **add more provisions or PIO entries**, append new dict entries to `RTI_ACT_CHUNKS`. The FAISS index is rebuilt in-memory on each server start.

---

## 🛠️ Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `ModuleNotFoundError` on startup | Dependencies not installed, or venv not activated | Run `pip install -r requirements.txt` inside your activated virtual environment |
| App starts but chat returns errors | Missing or incorrect `.env` values | Run `python diagnose_credentials.py` to check your IBM credentials |
| `401` / `403` error from watsonx.ai | Invalid or expired API key | Regenerate your API key in IBM Cloud → Manage → Access (IAM) → API Keys |
| Model not found error | `GRANITE_MODEL_ID` not available in your region | Run `python list_watsonx_resources.py` to see valid model IDs for your `IBM_WATSONX_URL` region |
| Slow first response | Sentence-transformer model downloading (~80 MB) | Normal on first run only — subsequent runs are fast |
| Port already in use | Another process using port 5000/8080 | Run on a different port: `python app.py --port 5050` (or stop the conflicting process) |

---

## ⚠️ Disclaimer

- RTI Sahayak **does not submit** applications on your behalf.
- It **does not guarantee** government response times.
- It **does not provide** general legal advice — only RTI-related drafting assistance.
- Always **verify** department addresses and PIO contact details before submission.
- For complex or contested cases, **consult a qualified legal professional**.

---

*RTI Sahayak is an independent educational tool and is not affiliated with the Government of India or IBM.*
