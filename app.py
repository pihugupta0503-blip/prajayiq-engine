import streamlit as st
import pandas as pd
import json
import re
from google import genai
from google.genai import types

# Page setup
st.set_page_config(
    page_title="PrajayIQ - Outreach Intelligence Engine",
    page_icon="⚡",
    layout="wide"
)

# Custom styling for consulting-grade appearance
st.markdown("""
<style>
    .main-header { font-size: 28px; font-weight: 700; color: #1E293B; margin-bottom: 5px; }
    .sub-header { font-size: 15px; color: #64748B; margin-bottom: 25px; }
    .metric-card { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 15px; margin-bottom: 10px; }
    .lint-success { color: #16A34A; font-weight: 600; }
    .lint-fail { color: #DC2626; font-weight: 600; }
    .preview-box { background-color: #0F172A; color: #F8FAFC; padding: 20px; border-radius: 12px; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">⚡ PrajayIQ: Precision B2B Outreach & Intelligence Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Bespoke C-Suite ICP Synthesis & 4-Format Copywriting Matrix (PrajayLeads Standard)</div>', unsafe_allow_html=True)

# Sidebar: API Key Configuration
with st.sidebar:
    st.header("🔑 Model Configuration")
    gemini_api_key = st.text_input("Enter Gemini API Key", type="password", help="Needed to run dynamic analysis")
    st.markdown("---")
    st.markdown("### Client Presets")
    preset_choice = st.selectbox(
        "Load Preset Case Study:",
        ["Revell Horsey ($10B+ Financial Advisor)", "Dr. Kerry Mitchell Brown (Forbes Author & CEO)", "Tanvi Mittal (Organizational Facilitator)", "Custom Client"]
    )

# Presets initialization
presets = {
    "Revell Horsey ($10B+ Financial Advisor)": {
        "client_name": "Revell Horsey",
        "profile": "Advisor to CEOs scaling growth-stage businesses. 35+ years across Investment Banking (Bank of America, Credit Suisse), SaaS leadership, and multi-location pet service operations. $10B+ in growth capital formation. Dartmouth College graduate.",
        "notes": "Target owners and operators of multi-location pet services, veterinary networks, and pet boarding businesses across the US. Emphasize unit-level economics, capital structure, and scale bottlenecks. Tone must be peer-to-peer and Wall-Street grade.",
        "sample_prospect": "Robert Appleby, President & Owner at K9 Resorts Luxury Pet Hotel (376 employees, luxury pet franchise operations across US)."
    },
    "Dr. Kerry Mitchell Brown (Forbes Author & CEO)": {
        "client_name": "Dr. Kerry Mitchell Brown",
        "profile": "CEO, kmb Consultancy. Organizational Transformation for Complex Institutions. PhD in Leadership. Author of upcoming Forbes book 'Revolutionary Leadership'. Chicago, Illinois.",
        "notes": "Outreach targets enterprise Chief People Officers, Diversity & Culture VPs, and Executive Directors of Organizational Development in companies with 500+ employees. Tone: Thought leader, scholarly yet pragmatic, human-centered.",
        "sample_prospect": "Joseph Lanzo, SHRM-SCP, Head of Human Resources and Talent Strategy (Greater Philadelphia, Enterprise HR Leader)."
    },
    "Tanvi Mittal (Organizational Facilitator)": {
        "client_name": "Tanvi Mittal",
        "profile": "Facilitator & Executive Coach at Tanvi Mittal Coaching. Helping senior corporate leadership teams thrive through restructuring, uncertainty, and culture shifts. Philadelphia, PA.",
        "notes": "Target CPOs, VP People and Culture, and change management executives. Strictly non-salesy, peer-to-peer inquiry. Emphasize trust-building in newly merged or restructured teams.",
        "sample_prospect": "Cheryl Bucci, VP People Operations & Organizational Development."
    },
    "Custom Client": {
        "client_name": "",
        "profile": "",
        "notes": "",
        "sample_prospect": ""
    }
}

active_data = presets[preset_choice]

# Step 1 & 2: Client Profile and Discovery
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Client Profile & Positioning")
    c_name = st.text_input("Client Name", value=active_data["client_name"])
    c_profile = st.text_area("Client LinkedIn Profile Summary / Experience", value=active_data["profile"], height=130)

with col2:
    st.subheader("2. Strategic Onboarding & Discovery Notes")
    c_notes = st.text_area("Founder / Strategy Meeting Intake Notes", value=active_data["notes"], height=185)

# Trigger ICP Generation
if st.button("Generate Ideal Customer Profile (ICP) & Sales Navigator Strings", type="primary"):
    if not gemini_api_key:
        st.warning("Please enter your Gemini API Key in the left sidebar to run the analysis.")
    else:
        try:
            client = genai.Client(api_key=gemini_api_key)
            prompt = f"""
            Act as an elite B2B LinkedIn Outreach Strategist for an agency servicing high-ticket advisory clients.
            Analyze this client and the strategy meeting notes:
            Client: {c_name}
            Profile: {c_profile}
            Intake Notes: {c_notes}

            Return a structured JSON with:
            1. "primary_icp": Exact target job titles, company size, and industries.
            2. "disqualifications": Profiles to strictly exclude.
            3. "sales_nav_boolean": Exact LinkedIn Sales Navigator search string using OR, AND, and quotes.
            4. "value_pillar": The single core peer-to-peer hook.
            """
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            st.session_state['icp_result'] = json.loads(response.text)
        except Exception as e:
            st.error(f"Error calling model: {e}")

# Display ICP Results
if 'icp_result' in st.session_state:
    icp = st.session_state['icp_result']
    st.markdown("---")
    st.subheader("🎯 Synthesized Target Persona & Sales Navigator Architecture")
    c_a, c_b = st.columns(2)
    with c_a:
        st.markdown(f"**Primary ICP Focus:**\n{icp.get('primary_icp', '')}")
        st.markdown(f"**Disqualification Criteria:**\n{icp.get('disqualifications', '')}")
    with c_b:
        st.markdown(f"**Core Value Hook:**\n{icp.get('value_pillar', '')}")
        st.code(icp.get('sales_nav_boolean', ''), language="text")

st.markdown("---")

# Step 3: Prospect Ingestion and 4-Format Copywriting Matrix
st.subheader("3. Prospect Context & The 4-Format Copywriting Matrix")

p_col1, p_col2 = st.columns([1, 1])

with p_col1:
    prospect_input = st.text_area(
        "Paste Prospect's Profile Info / Specific Accomplishment / Career Trajectory:",
        value=active_data["sample_prospect"],
        height=140
    )
    format_choice = st.radio(
        "Select Copywriting Matrix Formula:",
        [
            "Format 1: Career Arc Anchor (Inflection Point / Past-to-Present Transition)",
            "Format 2: Peer-to-Peer Identity (Direct C-Level Vocabulary, No Subservience)",
            "Format 3: Pattern Interrupt (Contrarian Market / Unit Economics Truth)",
            "Format 4: The YOU-Factor (Explicit Quote / Podcast / Recent Milestone)"
        ]
    )

with p_col2:
    st.markdown("**Agency Locked Formatting Rules Enforced:**")
    st.markdown("""
    - Strict maximum character length: Under 220 characters
    - Punctuation restriction: Zero hyphens (`-`), en-dashes (`–`), or em-dashes (`—`)
    - Opening: Immediate YOU-factor anchor (No 'Hope you are well' or 'I came across your profile')
    - Tone: Executive peer dialogue, zero sales pitches or calendar booking links
    """)

# Generate Message via Gemini
if st.button("Synthesize Personalized Outreach Note", type="secondary"):
    if not gemini_api_key:
        st.warning("Please enter your Gemini API Key in the sidebar.")
    else:
        try:
            client = genai.Client(api_key=gemini_api_key)
            gen_prompt = f"""
            You are drafting an executive LinkedIn outreach connection note for client: {c_name}
            Client Context: {c_profile}
            Prospect Context: {prospect_input}
            Chosen Strategy: {format_choice}

            RULES (NON-NEGOTIABLE):
            1. Total character count must be under 220 characters.
            2. Do NOT use ANY hyphens (-), en-dashes (–), or em-dashes (—).
            3. Do NOT use sales buzzwords like 'synergy', 'hop on a call', 'help you scale'.
            4. Open immediately by referencing the prospect's distinct path (the YOU-Factor).
            5. Output ONLY the raw message text.
            """
            resp = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=gen_prompt
            )
            st.session_state['generated_note'] = resp.text.strip()
        except Exception as e:
            st.error(f"Generation error: {e}")

# Pre-Flight Linting Engine & Simulation
if 'generated_note' in st.session_state:
    st.markdown("---")
    st.subheader("4. Pre-Flight Linting Protocol & Mobile Preview")
    
    note_text = st.text_area("Active Draft (Editable):", value=st.session_state['generated_note'], height=90)
    
    # Linting Checks
    char_len = len(note_text)
    has_dash = bool(re.search(r'[-–—]', note_text))
    has_jargon = bool(re.search(r'\b(quick call|synergy|hop on|free demo|pitch)\b', note_text, re.IGNORECASE))
    has_you_factor = not note_text.lower().startswith(('hi my name is', 'hope this finds you', 'i came across', 'i wanted to reach'))
    
    l_col1, l_col2 = st.columns([1, 1])
    
    with l_col1:
        st.markdown("**Automated Audit Checklist:**")
        st.markdown(f"- Character Count (< 220): {'<span class=\"lint-success\">PASS (' + str(char_len) + ')</span>' if char_len <= 220 else '<span class=\"lint-fail\">FAIL (' + str(char_len) + ')</span>'}", unsafe_allow_html=True)
        st.markdown(f"- Zero Hyphens/Dashes Rule: {'<span class=\"lint-success\">PASS (None found)</span>' if not has_dash else '<span class=\"lint-fail\">FAIL (Dashes detected)</span>'}", unsafe_allow_html=True)
        st.markdown(f"- Non-Salesy Lexicon: {'<span class=\"lint-success\">PASS (Clean)</span>' if not has_jargon else '<span class=\"lint-fail\">FAIL (Sales jargon found)</span>'}", unsafe_allow_html=True)
        st.markdown(f"- Opening 'YOU-Factor' Verification: {'<span class=\"lint-success\">PASS (Authentic opener)</span>' if has_you_factor else '<span class=\"lint-fail\">FAIL (Generic opener)</span>'}", unsafe_allow_html=True)
        
        if st.button("Auto-Lint & Clean Text"):
            cleaned = re.sub(r'[-–—]', ' ', note_text)
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            st.session_state['generated_note'] = cleaned
            st.rerun()

    with l_col2:
        st.markdown("**Sales Navigator Mobile View Simulation:**")
        st.markdown(f"""
        <div class="preview-box">
            <div style="font-size: 11px; color: #94A3B8; margin-bottom: 8px;">LinkedIn Sales Navigator • InMail / Connection Request</div>
            <div style="font-size: 13px; line-height: 1.4;">{note_text}</div>
            <div style="margin-top: 15px; font-size: 10px; color: #64748B;">Delivered via PrajayLeads Verified Protocol</div>
        </div>
        """, unsafe_allow_html=True)

# Step 5: Master Campaign Tracker Data
st.markdown("---")
st.subheader("5. Audited Master Prospect Tracker (Annexure E Alignment)")

sample_tracker_data = pd.DataFrame([
    {"Prospect Name": "Robert Appleby", "Company": "K9 Resorts Luxury Pet Hotel", "Title": "President/Owner", "Formula": "Career Arc Anchor", "Status": "Connected", "Conversion": "Strategy Call Booked"},
    {"Prospect Name": "Garret Tadlock", "Company": "Smart Tech Partnerships", "Title": "Chief Revenue Officer", "Formula": "Peer-to-Peer Identity", "Status": "Connected", "Conversion": "Phone Call Scheduled"},
    {"Prospect Name": "Joseph Lanzo", "Company": "Enterprise HR Advisory", "Title": "Head of HR", "Formula": "Pattern Interrupt", "Status": "Connected", "Conversion": "Webinar Seat Confirmed"},
    {"Prospect Name": "Cheryl Bucci", "Company": "Growth Stage Health", "Title": "VP People Operations", "Formula": "YOU-Factor Anchor", "Status": "In Review", "Conversion": "Pending Follow-up"}
])

st.dataframe(sample_tracker_data, use_container_width=True)
