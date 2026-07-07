"""
RTI Act, 2005 — Structured knowledge chunks for RAG retrieval.
Source: The Right to Information Act, 2005 (Act No. 22 of 2005), Government of India.
Each chunk has: id, title, text, tags.
"""

RTI_ACT_CHUNKS = [
    {
        "id": "sec2_definitions",
        "title": "Section 2 – Definitions",
        "text": (
            "Section 2(f) – 'Information' means any material in any form, including records, "
            "documents, memos, e-mails, opinions, advices, press releases, circulars, orders, "
            "log books, contracts, reports, papers, samples, models, data material held in any "
            "electronic form and information relating to any private body which can be accessed "
            "by a public authority under any other law for the time being in force.\n\n"
            "Section 2(h) – 'Public authority' means any authority or body or institution of "
            "self-government established or constituted by or under the Constitution; or by any "
            "other law made by Parliament; or by any other law made by State Legislature; or by "
            "notification issued or order made by the appropriate Government.\n\n"
            "Section 2(j) – 'Right to information' means the right to information accessible "
            "under this Act which is held by or under the control of any public authority and "
            "includes the right to inspect work, documents, records; take notes, extracts, or "
            "certified copies of documents or records; take certified samples of material; and "
            "obtain information in the form of diskettes, floppies, tapes, video cassettes or "
            "in any other electronic mode or through printouts."
        ),
        "tags": ["definitions", "information", "public authority", "right to information"],
    },
    {
        "id": "sec3_right",
        "title": "Section 3 – Right to Information",
        "text": "Section 3 – Subject to the provisions of this Act, all citizens shall have the right to information.",
        "tags": ["citizen right", "applicability"],
    },
    {
        "id": "sec4_proactive",
        "title": "Section 4 – Obligations of Public Authorities",
        "text": (
            "Section 4(1)(b) – Every public authority shall publish within 120 days: "
            "(i) particulars of its organisation, functions and duties; (ii) powers and duties "
            "of its officers and employees; (iii) procedure followed in decision-making; "
            "(iv) norms set for the discharge of its functions; (v) rules, regulations, "
            "instructions, manuals and records held by or under its control; (vi) statement of "
            "categories of documents that are held by it or under its control; "
            "(ix) directory of officers and employees; (x) monthly remuneration received by "
            "each officer and employee; (xi) budget allocated; (xii) manner of execution of "
            "subsidy programmes; (xvi) names, designations and other particulars of the "
            "Public Information Officers."
        ),
        "tags": ["proactive disclosure", "public authority obligations", "PIO directory"],
    },
    {
        "id": "sec5_pio",
        "title": "Section 5 – Designation of Public Information Officers",
        "text": (
            "Section 5(1) – Every public authority shall designate as many officers as the "
            "Central Public Information Officers or State Public Information Officers in all "
            "administrative units or offices under it as may be necessary to provide information "
            "to persons requesting for the information under this Act.\n\n"
            "Section 5(2) – Every public authority shall designate an officer at each "
            "sub-divisional level as a Central Assistant Public Information Officer or a State "
            "Assistant Public Information Officer to receive the applications for information "
            "or appeals under this Act for forwarding the same forthwith to the CPIO/SPIO.\n\n"
            "Section 5(4) – The CPIO or SPIO may seek the assistance of any other officer as "
            "considered necessary for the proper discharge of duties."
        ),
        "tags": ["PIO", "CPIO", "SPIO", "designation", "APIO"],
    },
    {
        "id": "sec6_application",
        "title": "Section 6 – Request for Information",
        "text": (
            "Section 6(1) – A person who desires to obtain any information under this Act shall "
            "make a request in writing or through electronic means in English or Hindi or in the "
            "official language of the area in which the application is being made, accompanying "
            "such fee as may be prescribed, to the Central Public Information Officer or State "
            "Public Information Officer of the concerned public authority.\n\n"
            "Section 6(2) – An applicant making request for information shall not be required to "
            "give any reason for requesting the information or any other personal details except "
            "those that may be necessary for contacting him.\n\n"
            "Section 6(3) – Where an application is made to a public authority requesting for "
            "information which is held by another public authority, it shall be the duty of the "
            "public authority to whom such application is made, to transfer the application or "
            "such part of it as may be appropriate to that other public authority and inform the "
            "applicant immediately. The transfer shall be done within 5 days."
        ),
        "tags": ["application", "request", "fee", "transfer", "Section 6"],
    },
    {
        "id": "sec7_timelines",
        "title": "Section 7 – Disposal of Request",
        "text": (
            "Section 7(1) – The CPIO or SPIO shall, as expeditiously as possible, and in any "
            "case within 30 days of the receipt of the request, either provide the information "
            "on payment of such fee as may be prescribed or reject the request for any of the "
            "reasons specified in sections 8 and 9.\n\n"
            "Proviso to Section 7(1) – Where the information sought for concerns the life or "
            "liberty of a person, the same shall be provided within 48 hours of the receipt "
            "of the request.\n\n"
            "Section 7(2) – If the CPIO or SPIO fails to give decision on the request for "
            "information within the period specified under sub-section (1), he or she shall be "
            "deemed to have refused the request.\n\n"
            "Section 7(6) – The person making request for information shall be provided the "
            "information free of charge where a public authority fails to comply with the time "
            "limits specified under sub-section (1).\n\n"
            "Section 7(9) – An information shall be provided in the form in which it is sought "
            "unless it would disproportionately divert the resources of the public authority "
            "or would be detrimental to the safety or preservation of the record in question."
        ),
        "tags": ["timeline", "30 days", "48 hours", "life or liberty", "deadline", "disposal", "Section 7"],
    },
    {
        "id": "sec8_exemptions",
        "title": "Section 8 – Exemption from Disclosure",
        "text": (
            "Section 8(1) – There shall be no obligation to give any citizen: (a) information "
            "prejudicially affecting sovereignty and integrity of India, security, strategic, "
            "scientific or economic interests of the State; (b) information expressly forbidden "
            "by court of law; (c) information whose disclosure would cause breach of privilege "
            "of Parliament or the State Legislature; (d) commercial confidence, trade secrets "
            "or intellectual property harming competitive position of a third party; "
            "(e) information in fiduciary relationship; (f) information received in confidence "
            "from foreign government; (g) information endangering life or physical safety of "
            "any person or identifying source of information for law enforcement; "
            "(h) information impeding investigation or prosecution of offenders; "
            "(i) cabinet papers including deliberations of Council of Ministers; "
            "(j) personal information whose disclosure has no relationship to any public "
            "activity or interest, or would cause unwarranted invasion of privacy.\n\n"
            "Section 8(3) – Information relating to any occurrence or event which has taken "
            "place twenty years before the date on which any request is made shall be provided."
        ),
        "tags": ["exemptions", "denial", "privacy", "security", "Section 8"],
    },
    {
        "id": "sec19_appeal",
        "title": "Section 19 – Appeal",
        "text": (
            "Section 19(1) – Any person who does not receive a decision within the time "
            "specified in sub-section (1) of section 7, or is aggrieved by a decision of the "
            "CPIO or SPIO, may within 30 days from the expiry of such period or from the "
            "receipt of such a decision prefer an appeal to such officer who is senior in rank "
            "to the CPIO or SPIO in each public authority. This officer is designated the "
            "First Appellate Authority (FAA). The FAA is NOT the CPIO or SPIO — the FAA is a "
            "different, more senior officer in the same public authority. The FAA may admit "
            "the appeal after the expiry of the period of 30 days if satisfied that the "
            "appellant was prevented by sufficient cause from filing the appeal in time.\n\n"
            "IMPORTANT — correct terminology: The recipient of a First Appeal under "
            "Section 19(1) must always be addressed as 'The First Appellate Authority (FAA)'. "
            "Never address a First Appeal to the CPIO, SPIO, or PIO — the appeal is filed "
            "against the PIO's non-response, so it must go to the FAA who is senior to the PIO.\n\n"
            "Section 19(3) – A second appeal against the decision under sub-section (1) shall "
            "lie within 90 days from the date on which the decision should have been made or "
            "was actually received, with the Central Information Commission (CIC) for Central "
            "Government authorities, or the State Information Commission (SIC) for State "
            "Government authorities.\n\n"
            "Section 19(5) – In any appeal proceedings, the burden of proving that a denial "
            "of a request was justified shall be on the CPIO or SPIO who denied the request.\n\n"
            "Section 19(8) – The CIC or SIC in its decision may require the public authority "
            "to compensate the complainant for any loss; impose penalties; or reject the complaint."
        ),
        "tags": [
            "appeal", "first appeal", "second appeal", "Section 19", "CIC", "SIC",
            "First Appellate Authority", "FAA", "appellate officer", "not SPIO", "not PIO",
        ],
    },
    {
        "id": "sec20_penalty",
        "title": "Section 20 – Penalties",
        "text": (
            "Section 20(1) – Where the CIC or SIC is of the opinion that the CPIO or SPIO "
            "has without any reasonable cause refused to receive an application for information "
            "or has not furnished information within the time specified under section 7(1) or "
            "maliciously denied the request or knowingly given incorrect, incomplete or "
            "misleading information or destroyed information which was the subject of the "
            "request or obstructed in any manner in furnishing the information, it shall impose "
            "a penalty of Rs 250 (two hundred and fifty) rupees each day till the application "
            "is received or information is furnished, so however, that the total amount of such "
            "penalty shall not exceed Rs 25,000 (twenty-five thousand) rupees."
        ),
        "tags": ["penalty", "fine", "Rs 250 per day", "Section 20", "CIC"],
    },
    {
        "id": "fee_rules_central",
        "title": "RTI Fee Rules – Central Government",
        "text": (
            "Right to Information (Regulation of Fee and Cost) Rules, 2005:\n"
            "Rule 3 – Application fee: Rs. 10/- (Rupees Ten only) for a request under "
            "Section 6(1). This is the only correct fee for Central Government applications. "
            "Never state a different amount.\n"
            "Rule 4 – Additional fee for providing information: Rs. 2/- per page (A4/A3 size); "
            "actual charge for larger size paper; actual cost for samples or models; "
            "Rs. 50/- per diskette or floppy; free of charge for the first hour of inspection "
            "of records, Rs. 5/- for each subsequent hour.\n"
            "Rule 5 – BPL (Below Poverty Line) applicants: NO fee is charged for the "
            "application. The applicant must furnish proof of BPL status (BPL card/certificate).\n"
            "First Appeals (Section 19(1)): NO fee is required. A First Appeal is free of charge.\n"
            "Second Appeals to CIC/SIC (Section 19(3)): NO fee is required.\n"
            "Payment modes for application fee: Demand Draft, Banker's Cheque, Indian Postal "
            "Order (IPO) payable to the Accounts Officer of the concerned public authority; "
            "cash against proper receipt; online payment via the RTI Online Portal "
            "(https://rtionline.gov.in)."
        ),
        "tags": [
            "fee", "Rs. 10", "Rs 10", "application fee", "BPL", "cost", "payment",
            "first appeal fee", "no fee", "appeal fee exemption",
        ],
    },
    {
        "id": "fee_rules_state",
        "title": "RTI Fee Rules – State Government",
        "text": (
            "State RTI Fee Rules:\n"
            "For State Government public authorities, the application fee is governed by "
            "each state's own RTI Rules (made under Section 27 of the RTI Act, 2005). "
            "Most states prescribe Rs. 10/- as the application fee, matching the Central rules. "
            "However, some states may prescribe a different amount (commonly between Rs. 5/- "
            "and Rs. 50/-).\n"
            "When drafting an RTI application for a State Government department, always:\n"
            "1. State Rs. 10/- as the fee (the most common state fee).\n"
            "2. Add a note: 'The fee may vary slightly by state; please verify the applicable "
            "   fee under [State] Right to Information Rules before submission.'\n"
            "BPL exemption applies equally in all states — no fee for BPL applicants.\n"
            "First Appeals and Second Appeals to SIC: NO fee required in all states.\n"
            "Examples of known state fees (verify before use):\n"
            "  • Maharashtra: Rs. 10/- (Maharashtra RTI Rules, 2005)\n"
            "  • Karnataka: Rs. 10/- (Karnataka RTI Rules, 2005)\n"
            "  • Uttar Pradesh: Rs. 10/-\n"
            "  • Tamil Nadu: Rs. 10/-\n"
            "  • West Bengal: Rs. 10/-\n"
            "Always direct applicants to verify with the concerned state's RTI portal or "
            "the department's public notice board."
        ),
        "tags": [
            "fee", "state fee", "state RTI rules", "Rs. 10", "state government",
            "BPL", "first appeal fee", "no fee", "state appeal",
        ],
    },
    {
        "id": "online_filing",
        "title": "Online RTI Filing – RTI Online Portal",
        "text": (
            "The Government of India has established the RTI Online Portal "
            "(https://rtionline.gov.in) for filing RTI applications and first appeals with "
            "Central Government ministries and departments electronically.\n"
            "Steps: (1) Register on the portal. (2) Select the Ministry/Department. "
            "(3) Fill in the application form. (4) Pay Rs 10 online via net banking/UPI. "
            "(5) BPL applicants upload BPL card for fee waiver. (6) An RTI registration number "
            "is generated — keep this for tracking.\n"
            "Note: The portal covers only Central Government public authorities. For state "
            "government departments, use the respective state RTI portal or submit a physical "
            "application to the concerned SPIO."
        ),
        "tags": ["online filing", "rtionline.gov.in", "portal", "central government", "e-RTI"],
    },
    {
        "id": "common_issues_mapping",
        "title": "Common Citizen Issues – Department Mapping",
        "text": (
            "Pension (government employees, family pension): Ministry of Pension & Pensioners' "
            "Welfare (Central); State Finance/Treasury Department (State employees).\n"
            "Provident Fund (EPF/PF): Employees' Provident Fund Organisation (EPFO).\n"
            "Income Tax refund, PAN, tax assessment: Income Tax Department / CBDT.\n"
            "Passport: Ministry of External Affairs / Regional Passport Office.\n"
            "Railways (train tickets, refunds, reservation): Ministry of Railways / Zonal Railway.\n"
            "Ration card, food security, PDS: Department of Food & Public Distribution (Central); "
            "State Food & Civil Supplies Department (State).\n"
            "Land records, property documents: State Revenue Department / District Collector.\n"
            "Birth / death certificate: Municipal Corporation / Gram Panchayat / State Registrar.\n"
            "Police complaints / FIR status: State Police (Home Department).\n"
            "Bank account / loan (public sector bank): Concerned PSB; RBI for regulatory issues.\n"
            "Scholarship: Ministry of Education (Central) or State Education Department.\n"
            "Employment / job card (MGNREGS): Ministry of Rural Development / District Programme Coordinator.\n"
            "AADHAAR / UID: UIDAI (Unique Identification Authority of India).\n"
            "Driving licence / vehicle registration: State Transport Department / RTO.\n"
            "Electricity / water (utility): State Electricity Board / State Water Board.\n"
            "Gram Panchayat / local body works: State Panchayati Raj Department / District Collector.\n"
            "PMAY (housing scheme): Ministry of Housing & Urban Affairs (Urban); "
            "Ministry of Rural Development (Rural).\n"
            "COVID-19 vaccination certificate: Ministry of Health & Family Welfare / NHM."
        ),
        "tags": [
            "department mapping", "pension", "EPFO", "income tax", "passport", "railway",
            "ration card", "land records", "police", "scholarship", "MGNREGS", "AADHAAR",
            "driving licence", "electricity", "PMAY", "vaccination",
        ],
    },
    {
        "id": "pio_directory_central",
        "title": "PIO Directory – Key Central Government Ministries",
        "text": (
            "Central Government CPIOs — verify current details at https://rtionline.gov.in.\n\n"
            "1. Ministry of Finance (Economic Affairs, Revenue, Expenditure, Financial Services): "
            "CPIO, North Block, New Delhi – 110001.\n"
            "2. Ministry of Home Affairs: CPIO, North Block, New Delhi – 110001.\n"
            "3. Ministry of External Affairs: CPIO, South Block, New Delhi – 110011.\n"
            "4. Ministry of Railways (Railway Board): CPIO, Rail Bhavan, Raisina Road, "
            "New Delhi – 110001.\n"
            "5. EPFO: CPIO, Bhavishya Nidhi Bhawan, 14 Bhikaiji Cama Place, New Delhi – 110066.\n"
            "6. Ministry of Labour and Employment: CPIO, Shram Shakti Bhawan, Rafi Marg, "
            "New Delhi – 110001.\n"
            "7. Ministry of Health and Family Welfare: CPIO, Nirman Bhawan, New Delhi – 110011.\n"
            "8. Ministry of Education: CPIO, Shastri Bhawan, New Delhi – 110001.\n"
            "9. CBDT (Income Tax): CPIO, North Block, New Delhi – 110001.\n"
            "10. Ministry of Pension & Pensioners' Welfare: CPIO, Lok Nayak Bhawan, "
            "Khan Market, New Delhi – 110003.\n"
            "11. Ministry of Rural Development: CPIO, Krishi Bhawan, New Delhi – 110001.\n"
            "12. Ministry of Housing & Urban Affairs: CPIO, Nirman Bhawan, New Delhi – 110011.\n"
            "13. Ministry of Road Transport and Highways: CPIO, Parivahan Bhawan, New Delhi – 110001.\n"
            "14. UIDAI (AADHAAR): CPIO, Bangla Sahib Road, Behind Kali Mandir, Gole Market, "
            "New Delhi – 110001.\n"
            "IMPORTANT: Always verify the current CPIO name and address from the official "
            "ministry website or the RTI Online Portal before submitting an application."
        ),
        "tags": [
            "PIO", "CPIO", "ministry", "central government", "Railways", "EPFO", "pension",
            "income tax", "health", "education", "directory", "UIDAI",
        ],
    },
]
