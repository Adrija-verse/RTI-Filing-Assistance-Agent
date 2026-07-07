# ⚖️ RTI Sahayak — AI-Powered RTI Filing Assistant

**RTI Sahayak** is a full-stack web application built with **Python Flask** and **IBM watsonx.ai (Granite models)** that helps Indian citizens exercise their Right to Information under the **RTI Act, 2005**. It features a conversational AI chat interface, an application status dashboard, a deadline tracker, and a First Appeal generator — all grounded in retrieved legal text via RAG.

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
        IBM watsonx.ai Granite-3-8b-Instruct
                │
                ▼
        Grounded response (draft / legal info / escalation)
```

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10+
- An **IBM Cloud account** with watsonx.ai enabled
- A **watsonx.ai project** (free Lite tier available)

### 2. Get IBM credentials

1. Log into [IBM Cloud](https://cloud.ibm.com)
2. Navigate to **watsonx.ai** → open your project → copy the **Project ID**
3. Go to **Manage → Access (IAM) → API Keys** → create a new API key
4. Note your regional URL (e.g., `https://us-south.ml.cloud.ibm.com`)

### 3. Configure the environment

```bash
cp .env.example .env
```

Edit `.env`:
```env
IBM_API_KEY=your-ibm-cloud-api-key
IBM_PROJECT_ID=your-watsonx-project-id
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
FLASK_SECRET_KEY=any-random-string
FLASK_DEBUG=false
GRANITE_MODEL_ID=ibm/granite-3-3-8b-instruct
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

> The first run also downloads the `all-MiniLM-L6-v2` sentence-transformer (~80 MB) for local RAG embeddings.

### 5. Run the application

```bash
# Development
python app.py

# Production
gunicorn -w 2 -b 0.0.0.0:8080 app:app
```

Open your browser at **http://localhost:5000** (dev) or **http://localhost:8080** (prod).

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

No code changes needed elsewhere — the system prompt is assembled automatically from this dictionary.

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

## ⚠️ Disclaimer

- RTI Sahayak **does not submit** applications on your behalf.
- It **does not guarantee** government response times.
- It **does not provide** general legal advice — only RTI-related drafting assistance.
- Always **verify** department addresses and PIO contact details before submission.
- For complex or contested cases, **consult a qualified legal professional**.

---

*RTI Sahayak is an independent educational tool and is not affiliated with the Government of India or IBM.*
