"""
agent/rti_agent.py — RTI Sahayak agent powered by IBM watsonx.ai Granite models.

AGENT_INSTRUCTIONS
==================
Customize the agent's behavior by editing the constants in this block.
These settings control tone, legal drafting rules, escalation timing,
knowledge sources, and clarification policy.
"""

from __future__ import annotations

import os
from datetime import date
from typing import List, Dict

# ══════════════════════════════════════════════════════════════════════════════
#  AGENT_INSTRUCTIONS — Edit this section to customize the agent
# ══════════════════════════════════════════════════════════════════════════════

AGENT_INSTRUCTIONS = {
    # ── Identity ────────────────────────────────────────────────────────────
    "name": "RTI Sahayak",
    "persona": (
        "You are RTI Sahayak, a knowledgeable and helpful assistant that guides "
        "Indian citizens in exercising their Right to Information under the "
        "RTI Act, 2005. You speak in clear, simple, jargon-free language because "
        "users may have limited familiarity with legal or bureaucratic processes."
    ),

    # ── Tone & Language ──────────────────────────────────────────────────────
    "tone": (
        "Be warm, respectful, and encouraging. Avoid bureaucratic jargon. "
        "Use short sentences and active voice. When users seem frustrated or "
        "confused, acknowledge their concern before providing guidance."
    ),

    # ── Legal Drafting Rules ─────────────────────────────────────────────────
    "drafting_rules": (
        "1. Use ONLY information retrieved from the knowledge base — never invent "
        "   legal provisions, section numbers, fee amounts, or department addresses.\n"
        "2. Write 'information sought' as specific, numbered questions so the request "
        "   cannot be rejected as vague under Section 7(9).\n"
        "3. Always include: applicant details, PIO address, fee note, today's date, "
        "   statutory deadline (30 days standard / 48 hours for life or liberty).\n"
        "4. Remind users to verify the PIO's current address before submission.\n"
        "5. Do not guarantee government response times.\n"
        "6. Do not provide general legal advice beyond RTI matters.\n"
        "7. Do not submit applications on the user's behalf.\n"
        "\n"
        "FEE RULES (strictly enforced):\n"
        "8. The prescribed RTI application fee is ALWAYS Rs. 10/- (Rupees Ten only) "
        "   for Central Government departments (Rule 3, RTI Fee & Cost Rules, 2005). "
        "   Never state a different amount.\n"
        "9. If the department is a State Government body, state Rs. 10/- as the fee "
        "   AND add a note: 'Fee may vary slightly by state; verify with [State] RTI "
        "   Rules before submission.'\n"
        "10. If the applicant indicates BPL (Below Poverty Line) status, state that "
        "    NO fee is required and the applicant must attach their BPL certificate "
        "    (Rule 5, RTI Fee & Cost Rules, 2005).\n"
        "11. First Appeals under Section 19(1) carry NO fee. Always state this.\n"
        "\n"
        "DEADLINE RULES (strictly enforced):\n"
        "12. The statutory response deadline is ALWAYS 30 days from the date of "
        "    receipt of the application (Section 7(1), RTI Act, 2005). Never shorten "
        "    this, regardless of what the user requests.\n"
        "13. For matters concerning life or liberty, the deadline is ALWAYS 48 hours "
        "    from receipt (Section 7(1) proviso). No other timeline applies.\n"
        "14. If the user requests an expedited or faster response, add it as a "
        "    SEPARATE polite request line (e.g., 'URGENT REQUEST (without prejudice "
        "    to statutory deadline): I request an early response given the urgency '). "
        "    This line must NEVER replace or modify the stated statutory deadline."
    ),

    # ── Clarification Policy ────────────────────────────────────────────────
    "clarification_policy": (
        "If any of the following required fields are missing, ask the user for "
        "them BEFORE drafting: applicant name, applicant address, applicant "
        "contact (phone or email), filing date (for deadline tracking), and "
        "reference number (for first appeals). Ask for one or two fields at a "
        "time — do not bombard the user with a long list of questions at once."
    ),

    # ── Department / PIO Identification ─────────────────────────────────────
    "department_policy": (
        "Identify the most relevant government department and PIO from the "
        "retrieved knowledge base. If the department cannot be confidently "
        "identified (e.g., ambiguous jurisdiction), ask ONE clarifying question "
        "(e.g., 'Is this a Central Government or State Government matter?') "
        "rather than guessing."
    ),

    # ── Escalation / First Appeal Timing ────────────────────────────────────
    "escalation_rules": (
        "Standard deadline: 30 days from filing date (Section 7(1)).\n"
        "Life or liberty: 48 hours from filing (Section 7(1) proviso).\n"
        "If the user reports no response after the deadline, immediately offer "
        "to draft a First Appeal under Section 19(1).\n"
        "CRITICAL — appellate authority terminology: A First Appeal under "
        "Section 19(1) is ALWAYS addressed to the First Appellate Authority (FAA) "
        "— an officer senior in rank to the PIO/CPIO/SPIO in the same public "
        "authority. NEVER address or refer to the recipient of a First Appeal as "
        "SPIO, CPIO, or PIO. The correct designation is 'First Appellate "
        "Authority (FAA)' or 'The First Appellate Authority'.\n"
        "Mention that: (a) information is now free under Section 7(6); "
        "(b) penalty of Rs 250/day applies under Section 20(1).\n"
        "First Appeal window: 30 days after the original deadline lapses.\n"
        "Second Appeal: to CIC (Central) or SIC (State) within 90 days "
        "under Section 19(3)."
    ),

    # ── Knowledge Sources ────────────────────────────────────────────────────
    "knowledge_sources": (
        "Primary: RTI Act, 2005 provisions retrieved from the local knowledge base.\n"
        "Secondary: Right to Information (Regulation of Fee and Cost) Rules, 2005.\n"
        "PIO Directory: Central Government ministries (verify at rtionline.gov.in).\n"
        "Department Mapping: Common citizen issues mapped to relevant departments."
    ),

    # ── Scope Limits ─────────────────────────────────────────────────────────
    "out_of_scope": (
        "If a request falls outside RTI scope (e.g., filing a consumer complaint, "
        "legal advice on property disputes), politely redirect the user and suggest "
        "consulting a qualified legal professional or the appropriate authority."
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
#  System prompt builder (assembled from AGENT_INSTRUCTIONS)
# ══════════════════════════════════════════════════════════════════════════════

def build_system_prompt(context: str, today_str: str) -> str:
    ai = AGENT_INSTRUCTIONS
    return f"""{ai['persona']}

TONE: {ai['tone']}

LEGAL DRAFTING RULES:
{ai['drafting_rules']}

CLARIFICATION POLICY:
{ai['clarification_policy']}

DEPARTMENT / PIO IDENTIFICATION:
{ai['department_policy']}

ESCALATION & APPEAL TIMING:
{ai['escalation_rules']}

KNOWLEDGE SOURCES:
{ai['knowledge_sources']}

OUT-OF-SCOPE POLICY:
{ai['out_of_scope']}

Today's date: {today_str}

RETRIEVED CONTEXT FROM RTI ACT & PIO DIRECTORY:
{context}

Instructions: Answer the user's query using ONLY the information in the retrieved context above.
If the context does not contain what you need, state so clearly and ask a targeted clarifying question.
Never fabricate legal provisions, addresses, or department names.
"""


# ══════════════════════════════════════════════════════════════════════════════
#  Error translation helper
# ══════════════════════════════════════════════════════════════════════════════

def _friendly_error(exc: Exception, project_id: str, url: str) -> str:
    """
    Translate raw IBM API exceptions into clear, actionable messages.
    Inspects the exception text for known IBM error codes.
    """
    msg = str(exc).lower()

    # Project / space not found (WSCPA0000E, 404 on project lookup)
    if "wscpa0000e" in msg or ("not found" in msg and "project" in msg) or "missing" in msg:
        return (
            f"[ERROR] IBM watsonx.ai Project Not Found\n\n"
            f"Project ID '{project_id}' could not be found.\n\n"
            f"How to fix this:\n"
            f"1. Go to https://cloud.ibm.com and open watsonx.ai.\n"
            f"2. Open the project you want to use.\n"
            f"3. Click 'Manage' tab, then 'General' and copy the Project ID.\n"
            f"4. Paste it as IBM_PROJECT_ID in your .env file.\n\n"
            f"Also check that your IBM_WATSONX_URL matches the region where "
            f"your project lives (e.g. us-south, eu-de, jp-tok).\n"
            f"Current URL: {url}"
        )

    # Authentication / API key errors
    if any(k in msg for k in ("401", "unauthorized", "invalid api key", "authentication")):
        return (
            "[ERROR] IBM Cloud Authentication Failed\n\n"
            "Your IBM_API_KEY is invalid or expired.\n\n"
            "How to fix this:\n"
            "1. Go to https://cloud.ibm.com\n"
            "2. Navigate to Manage -> Access (IAM) -> API keys.\n"
            "3. Create a new API key and copy it.\n"
            "4. Replace IBM_API_KEY in your .env file with the new key."
        )

    # Wrong region URL
    if any(k in msg for k in ("connection", "timeout", "nodename nor servname")):
        return (
            f"[ERROR] Cannot reach IBM watsonx.ai\n\n"
            f"Could not connect to: {url}\n\n"
            "How to fix this:\n"
            "- Check your IBM_WATSONX_URL in .env -- it must match your region.\n"
            "- Valid URLs:\n"
            "    https://us-south.ml.cloud.ibm.com\n"
            "    https://eu-de.ml.cloud.ibm.com\n"
            "    https://jp-tok.ml.cloud.ibm.com\n"
            "- Check your internet connection."
        )

    # Model not found / not enabled
    if any(k in msg for k in ("model", "404", "not found")) and "project" not in msg:
        return (
            "[ERROR] Granite Model Not Available\n\n"
            "The requested model is not available in your watsonx.ai instance.\n\n"
            "How to fix this:\n"
            "- Verify GRANITE_MODEL_ID in your .env file.\n"
            "- Recommended value: ibm/granite-3-3-8b-instruct\n"
            "- Check that the model is enabled in your watsonx.ai region."
        )

    # Fallback — return the original message with context
    return (
        f"[ERROR] IBM watsonx.ai Error\n\n{exc}\n\n"
        f"Check your .env file:\n"
        f"  IBM_API_KEY      -- your IBM Cloud API key\n"
        f"  IBM_PROJECT_ID   -- your watsonx.ai Project ID\n"
        f"                      (project -> Manage -> General)\n"
        f"  IBM_WATSONX_URL  -- must match the region of your project\n"
        f"  GRANITE_MODEL_ID -- e.g. ibm/granite-3-3-8b-instruct"
    )


# ══════════════════════════════════════════════════════════════════════════════
#  watsonx.ai client wrapper
# ══════════════════════════════════════════════════════════════════════════════

class WatsonxClient:
    """Thin wrapper around IBM watsonx.ai ModelInference."""

    def __init__(self):
        from ibm_watsonx_ai import Credentials
        from ibm_watsonx_ai.foundation_models import ModelInference

        api_key = os.environ.get("IBM_API_KEY", "").strip()
        project_id = os.environ.get("IBM_PROJECT_ID", "").strip()
        url = os.environ.get("IBM_WATSONX_URL", "https://eu-de.ml.cloud.ibm.com").strip()
        model_id = os.environ.get("GRANITE_MODEL_ID", "ibm/granite-4-h-small").strip()

        # ── Validate credentials before making any API call ──────────────────
        if not api_key or api_key == "your-ibm-cloud-api-key-here":
            raise EnvironmentError(
                "IBM_API_KEY is not set. Open your .env file and add your IBM Cloud API key."
            )
        if not project_id or project_id == "your-watsonx-project-id-here":
            raise EnvironmentError(
                "IBM_PROJECT_ID is not set. Open your .env file and add your watsonx.ai Project ID."
            )

        self._project_id = project_id
        self._url = url

        try:
            credentials = Credentials(url=url, api_key=api_key)
            self._model = ModelInference(
                model_id=model_id,
                credentials=credentials,
                project_id=project_id,
                params={
                    "max_new_tokens": 2048,
                    "temperature": 0.2,
                    "repetition_penalty": 1.1,
                },
            )
        except Exception as exc:
            raise EnvironmentError(_friendly_error(exc, project_id, url)) from exc

    def generate(self, system_prompt: str, user_message: str, history: List[Dict]) -> str:
        """
        Build a chat-style prompt and call Granite via watsonx.ai.
        Returns the generated text string.
        """
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        try:
            response = self._model.chat(messages=messages)
            return response["choices"][0]["message"]["content"].strip()
        except Exception as exc:
            raise RuntimeError(_friendly_error(exc, self._project_id, self._url)) from exc


# ══════════════════════════════════════════════════════════════════════════════
#  RTISahayakAgent — high-level agent class
# ══════════════════════════════════════════════════════════════════════════════

class RTISahayakAgent:
    """
    Conversational RTI agent with RAG retrieval and watsonx.ai Granite backend.
    Maintains per-session conversation history.
    """

    def __init__(self):
        self._client = WatsonxClient()
        self.history: List[Dict] = []

    def chat(self, user_message: str) -> str:
        """
        Send a user message and return the agent's response.
        Retrieves relevant RTI Act provisions first, then calls Granite.
        """
        from rti_tools.rag import retrieve, format_context

        chunks = retrieve(user_message, k=5)
        context = format_context(chunks)
        today_str = date.today().strftime("%d %B %Y")
        system_prompt = build_system_prompt(context, today_str)

        reply = self._client.generate(system_prompt, user_message, self.history)

        # Append to history (keep last 10 turns to manage token budget)
        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": reply})
        if len(self.history) > 20:
            self.history = self.history[-20:]

        return reply

    def reset(self) -> None:
        """Clear the conversation history."""
        self.history = []
