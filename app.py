"""
app.py — Flask application for RTI Sahayak.
IBM watsonx.ai + Granite + RAG-based RTI assistant.

Run:
    python app.py                  (development)
    gunicorn -w 2 -b 0.0.0.0:8080 app:app  (production)
"""

from __future__ import annotations

import os
import json
import uuid
from datetime import date, datetime
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
    flash,
)
from flask_cors import CORS
from dotenv import load_dotenv

# ── Load environment variables ─────────────────────────────────────────────
load_dotenv()

# ── Flask app setup ────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "rti-sahayak-dev-secret")
CORS(app)

# ── Database init ──────────────────────────────────────────────────────────
from rti_tools.database import init_db, save_application, get_all_applications, get_application, delete_application
init_db()

# ── Per-session agent instances ────────────────────────────────────────────
_agents: dict[str, object] = {}

def get_agent(session_id: str):
    """Return (or lazily create) a per-session RTISahayakAgent."""
    if session_id not in _agents:
        from agent.rti_agent import RTISahayakAgent
        _agents[session_id] = RTISahayakAgent()
    return _agents[session_id]


# ══════════════════════════════════════════════════════════════════════════════
#  Page routes
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    """Landing page — chat interface."""
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    """Application status dashboard."""
    applications = get_all_applications()
    return render_template("dashboard.html", applications=applications)


@app.route("/application/<int:app_id>")
def application_detail(app_id: int):
    """Detail view for a single application."""
    app_record = get_application(app_id)
    if app_record is None:
        flash("Application not found.", "error")
        return redirect(url_for("dashboard"))
    return render_template("application_detail.html", app=app_record)


@app.route("/application/<int:app_id>/delete", methods=["POST"])
def delete_app(app_id: int):
    """Delete an application."""
    delete_application(app_id)
    flash("Application deleted.", "info")
    return redirect(url_for("dashboard"))


# ══════════════════════════════════════════════════════════════════════════════
#  API routes
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """
    POST /api/chat
    Body: { "message": "user text" }
    Returns: { "reply": "agent response" }
    """
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "message is required"}), 400

    session_id = session.get("session_id", str(uuid.uuid4()))
    session["session_id"] = session_id

    try:
        agent = get_agent(session_id)
        reply = agent.chat(user_message)
        return jsonify({"reply": reply})
    except EnvironmentError as exc:
        return jsonify({"error": str(exc), "config_required": True}), 503
    except Exception as exc:
        return jsonify({"error": f"Agent error: {exc}"}), 500


@app.route("/api/chat/reset", methods=["POST"])
def api_chat_reset():
    """Clear the current session's conversation history."""
    session_id = session.get("session_id")
    if session_id and session_id in _agents:
        _agents[session_id].reset()
    return jsonify({"status": "ok"})


@app.route("/api/deadline", methods=["POST"])
def api_deadline():
    """
    POST /api/deadline
    Body: { "filing_date": "YYYY-MM-DD", "life_or_liberty": false }
    Returns deadline info dict.
    """
    data = request.get_json(silent=True) or {}
    try:
        filing_date = datetime.strptime(data["filing_date"], "%Y-%m-%d").date()
    except (KeyError, ValueError):
        return jsonify({"error": "filing_date (YYYY-MM-DD) is required"}), 400

    lol = bool(data.get("life_or_liberty", False))

    from rti_tools.drafting import deadline_status
    info = deadline_status(filing_date, lol)
    info["deadline"] = info["deadline"].isoformat()
    info["filing_date"] = filing_date.isoformat()
    return jsonify(info)


@app.route("/api/draft/application", methods=["POST"])
def api_draft_application():
    """
    POST /api/draft/application
    Body: { applicant_name, applicant_address, applicant_contact,
            department, pio_address, information_sought (list),
            filing_date (opt), bpl (opt), life_or_liberty (opt) }
    Returns: { draft, deadline_info, saved_id }
    """
    data = request.get_json(silent=True) or {}

    required = ["applicant_name", "applicant_address", "applicant_contact",
                 "department", "pio_address", "information_sought"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    from rti_tools.drafting import draft_rti_application, deadline_status

    filing_date = date.today()
    if data.get("filing_date"):
        try:
            filing_date = datetime.strptime(data["filing_date"], "%Y-%m-%d").date()
        except ValueError:
            pass

    lol = bool(data.get("life_or_liberty", False))
    info = data.get("information_sought", [])
    if isinstance(info, str):
        info = [info]

    draft = draft_rti_application(
        applicant_name=data["applicant_name"],
        applicant_address=data["applicant_address"],
        applicant_contact=data["applicant_contact"],
        department=data["department"],
        pio_address=data["pio_address"],
        information_sought=info,
        filing_date=filing_date,
        bpl=bool(data.get("bpl", False)),
        life_or_liberty=lol,
    )

    dl_info = deadline_status(filing_date, lol)
    dl_info["deadline"] = dl_info["deadline"].isoformat()

    # Persist to DB
    subject = "; ".join(info[:2]) if info else "RTI Application"
    saved_id = save_application({
        "subject": subject[:200],
        "department": data["department"],
        "pio_address": data["pio_address"],
        "date_filed": filing_date.isoformat(),
        "deadline": dl_info["deadline"],
        "life_liberty": lol,
        "applicant_name": data["applicant_name"],
        "applicant_address": data["applicant_address"],
        "applicant_contact": data["applicant_contact"],
        "draft_text": draft,
    })

    return jsonify({
        "draft": draft,
        "deadline_info": dl_info,
        "saved_id": saved_id,
    })


@app.route("/api/draft/appeal", methods=["POST"])
def api_draft_appeal():
    """
    POST /api/draft/appeal
    Body: { applicant_name, applicant_address, applicant_contact,
            department, original_application_date (YYYY-MM-DD),
            original_application_subject, pio_address (opt),
            appellate_officer_address (opt), reason_for_appeal (opt) }
    Returns: { draft }
    """
    data = request.get_json(silent=True) or {}

    required = ["applicant_name", "applicant_address", "applicant_contact",
                 "department", "original_application_date", "original_application_subject"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        orig_date = datetime.strptime(data["original_application_date"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "original_application_date must be YYYY-MM-DD"}), 400

    from rti_tools.drafting import draft_first_appeal

    draft = draft_first_appeal(
        applicant_name=data["applicant_name"],
        applicant_address=data["applicant_address"],
        applicant_contact=data["applicant_contact"],
        department=data["department"],
        original_application_date=orig_date,
        original_application_subject=data["original_application_subject"],
        pio_address=data.get("pio_address", "[PIO address — as on original application]"),
        appellate_officer_address=data.get(
            "appellate_officer_address",
            "[First Appellate Authority — officer senior in rank to PIO]"
        ),
        reason_for_appeal=data.get(
            "reason_for_appeal",
            "No response received within the statutory 30-day period under Section 7(1) "
            "of the RTI Act, 2005, constituting a deemed refusal under Section 7(2)."
        ),
    )

    return jsonify({"draft": draft})


@app.route("/api/applications", methods=["GET"])
def api_applications():
    """GET /api/applications — Return all tracked applications as JSON."""
    return jsonify(get_all_applications())


# ══════════════════════════════════════════════════════════════════════════════
#  Entry point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug)
