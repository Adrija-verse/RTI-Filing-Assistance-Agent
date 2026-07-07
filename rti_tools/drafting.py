"""
rti_tools/drafting.py — RTI application and First Appeal template utilities.
All legal text is grounded in the RTI Act, 2005.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import List, Optional


# ──────────────────────────────────────────────────────────────────────────────
# Deadline helpers
# ──────────────────────────────────────────────────────────────────────────────

def compute_deadline(filing_date: date, life_or_liberty: bool = False) -> date:
    """
    Return the statutory response deadline.
    - Life or liberty matters: 48 hours  (Section 7 proviso).
    - Standard requests:       30 days   (Section 7(1)).
    """
    if life_or_liberty:
        from datetime import datetime, timedelta as td
        dt = datetime.combine(filing_date, datetime.min.time()) + td(hours=48)
        return dt.date()
    return filing_date + timedelta(days=30)


def deadline_status(filing_date: date, life_or_liberty: bool = False) -> dict:
    """
    Return a status dict for dashboard display.
    Keys: deadline (date), days_remaining (int), status (str: on_track|due_soon|overdue)
    """
    deadline = compute_deadline(filing_date, life_or_liberty)
    remaining = (deadline - date.today()).days

    if remaining < 0:
        status = "overdue"
    elif remaining <= 5:
        status = "due_soon"
    else:
        status = "on_track"

    return {
        "deadline": deadline,
        "days_remaining": remaining,
        "status": status,
    }


# ──────────────────────────────────────────────────────────────────────────────
# RTI Application draft
# ──────────────────────────────────────────────────────────────────────────────

def draft_rti_application(
    applicant_name: str,
    applicant_address: str,
    applicant_contact: str,
    department: str,
    pio_address: str,
    information_sought: List[str],
    filing_date: Optional[date] = None,
    bpl: bool = False,
    life_or_liberty: bool = False,
    preferred_language: str = "English",
    is_state_dept: bool = False,
    expedited_note: Optional[str] = None,
) -> str:
    """Return a fully formatted RTI application under Section 6(1).

    Args:
        is_state_dept:  Set True when the department is a State Government body.
                        Appends a caveat that the fee may vary by state RTI rules.
        expedited_note: If the user wants a faster response, pass that as a
                        plain-language request here.  It is printed as a separate
                        polite line and NEVER overrides the statutory deadline.
    """
    if filing_date is None:
        filing_date = date.today()

    deadline = compute_deadline(filing_date, life_or_liberty)

    # Statutory timeline — fixed by law; never shortened.
    if life_or_liberty:
        timeline_note = "48 hours (this matter concerns life or liberty — Section 7 proviso)"
    else:
        timeline_note = "30 days (Section 7(1) of the RTI Act, 2005)"

    # Fee — Rs. 10/- is the prescribed Central fee (Rule 3, RTI Fee Rules 2005).
    # BPL applicants are fully exempt (Rule 5).  First Appeals carry no fee.
    if bpl:
        fee_note = (
            "I am a Below Poverty Line (BPL) applicant. I am attaching a copy of my BPL "
            "certificate/card. No fee is therefore payable as per Rule 5 of the Right to "
            "Information (Regulation of Fee and Cost) Rules, 2005."
        )
    else:
        fee_note = (
            "I am enclosing the prescribed application fee of Rs. 10/- (Rupees Ten only) "
            "by [IPO / Demand Draft / Banker's Cheque / online payment — please choose one] "
            "as required under Rule 3 of the Right to Information "
            "(Regulation of Fee and Cost) Rules, 2005."
        )
        if is_state_dept:
            fee_note += (
                "\nNote: The fee for State Government RTI applications may vary slightly "
                "by state. Please verify the applicable fee under your State RTI Rules "
                "before submission."
            )

    numbered_questions = "\n".join(
        f"  {i + 1}. {q}" for i, q in enumerate(information_sought)
    )

    # Build optional expedited request line (separate from the statutory deadline).
    expedited_line = ""
    if expedited_note:
        expedited_line = (
            f"\nURGENT REQUEST (without prejudice to statutory deadline):\n"
            f"{expedited_note}\n"
        )

    return f"""APPLICATION UNDER THE RIGHT TO INFORMATION ACT, 2005
(Section 6 — Request for Information)
{'=' * 60}

To,
The Public Information Officer (PIO),
{department},
{pio_address}

Date: {filing_date.strftime('%d %B %Y')}

Subject: Request for information under the Right to Information Act, 2005.

Sir / Madam,

I, {applicant_name}, a citizen of India residing at {applicant_address}, \
hereby request the following information under Section 6(1) of the Right to \
Information Act, 2005. My contact details are: {applicant_contact}.

INFORMATION SOUGHT:
{numbered_questions}

STATUTORY TIMELINE:
Under {timeline_note}, you are required to provide the information or \
communicate a decision within the statutory deadline: {deadline.strftime('%d %B %Y')}.
{expedited_line}
FEE:
{fee_note}

PREFERRED LANGUAGE OF RESPONSE: {preferred_language}

I request that the information be provided in the form of certified copies / \
printouts / inspection of records (please delete as appropriate).

Kindly acknowledge receipt of this application.

Yours sincerely,

{applicant_name}
{applicant_address}
{applicant_contact}
Date: {filing_date.strftime('%d %B %Y')}

{'=' * 60}
NOTE: If no response is received by {deadline.strftime('%d %B %Y')}, you may \
file a First Appeal under Section 19(1) of the RTI Act, 2005.
No fee is required for filing a First Appeal.
Always verify the PIO's current name and address before submission.
{'=' * 60}""".strip()


# ──────────────────────────────────────────────────────────────────────────────
# First Appeal draft
# ──────────────────────────────────────────────────────────────────────────────

def draft_first_appeal(
    applicant_name: str,
    applicant_address: str,
    applicant_contact: str,
    department: str,
    original_application_date: date,
    original_application_subject: str,
    pio_address: str = "[PIO address — as on original application]",
    appellate_officer_address: str = "[First Appellate Authority — officer senior in rank to PIO]",
    reason_for_appeal: str = "No response received within the statutory period",
) -> str:
    """Return a formatted First Appeal under Section 19(1) of the RTI Act, 2005."""
    today = date.today()
    original_deadline = original_application_date + timedelta(days=30)
    days_overdue = max(0, (today - original_deadline).days)
    first_appeal_window = original_deadline + timedelta(days=30)

    return f"""FIRST APPEAL UNDER SECTION 19(1) OF THE RIGHT TO INFORMATION ACT, 2005
{'=' * 60}

To,
The First Appellate Authority (FAA),
{department},
{appellate_officer_address}

Date: {today.strftime('%d %B %Y')}

Subject: First Appeal under Section 19(1) of the RTI Act, 2005 — against \
deemed refusal / non-response by the PIO of {department}.

Sir / Madam,

I, {applicant_name}, a citizen of India residing at {applicant_address}, \
submit this First Appeal under Section 19(1) of the Right to Information \
Act, 2005, on the following grounds:

FACTS:
1. I filed an RTI application under Section 6(1) of the RTI Act, 2005 with \
the PIO of {department} on {original_application_date.strftime('%d %B %Y')}, \
seeking the following information:
   "{original_application_subject}"

2. The statutory deadline for a response under Section 7(1) was \
{original_deadline.strftime('%d %B %Y')} (30 days from the date of application).

3. As of today ({today.strftime('%d %B %Y')}), I have received no response, \
decision, or communication from the PIO. The deadline has been exceeded by \
{days_overdue} day(s).

4. Under Section 7(2) of the RTI Act, 2005, failure to give a decision within \
the prescribed period is deemed to be a refusal.

GROUNDS OF APPEAL:
{reason_for_appeal}.

RELIEF SOUGHT:
(a) Direct the PIO to forthwith provide the information requested in my original \
application dated {original_application_date.strftime('%d %B %Y')}.
(b) Note that under Section 7(6) of the RTI Act, 2005, the information shall now \
be provided free of charge since the PIO has failed to comply with the statutory \
time limit.
(c) Initiate penalty proceedings against the PIO under Section 20(1) of the RTI \
Act, 2005, imposing a penalty of Rs 250 per day for the period of default.

I am attaching a copy of the original RTI application for reference.

Yours sincerely,

{applicant_name}
{applicant_address}
{applicant_contact}
Date: {today.strftime('%d %B %Y')}

Enclosures:
1. Copy of original RTI application dated \
{original_application_date.strftime('%d %B %Y')}.
2. Proof of submission (postal receipt / acknowledgement, if available).

{'=' * 60}
NOTE:
• This First Appeal should be filed by \
{first_appeal_window.strftime('%d %B %Y')} (within 30 days of the original deadline).
• If filing after that date, include a condonation-of-delay request \
(Section 19(1) proviso).
• If the First Appeal is also not decided within 30 days, you may file a \
Second Appeal with CIC/SIC under Section 19(3) within 90 days.
• Verify the Appellate Authority's name and address from the department's website.
{'=' * 60}""".strip()
