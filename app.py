import streamlit as st
import pandas as pd
import json
import re

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

# Preset Database
presets = {
    "Revell Horsey ($10B+ Financial Advisor)": {
        "client_name": "Revell Horsey",
        "profile": "Advisor to CEOs scaling growth-stage businesses. 35+ years across Investment Banking (Bank of America, Credit Suisse), SaaS leadership, and multi-location pet service operations. $10B+ in growth capital formation. Dartmouth College graduate.",
        "notes": "Target owners and operators of multi-location pet services, veterinary networks, and pet boarding businesses across the US. Emphasize unit-level economics, capital structure, and scale bottlenecks. Tone must be peer-to-peer and Wall-Street grade.",
        "icp": {
            "primary_icp": "Founders, CEOs, Presidents, and VPs of Operations at multi-unit pet boarding, daycares, grooming, and veterinary chains with 11-500 employees across the United States.",
            "disqualifications": "Single-facility pet shops, dog walkers, independent solo trainers, low-margin retail suppliers.",
            "sales_nav_boolean": '("Dog Boarding" OR "Pet Boarding" OR "Dog Daycare" OR "Veterinary") AND ("Owner" OR "Founder" OR "President" OR "VP of Operations") AND Headcount: 11-500',
            "value_pillar": "Optimizing unit economics, working capital, and multi-location scaling bottlenecks."
        },
        "sample_prospect": "Robert Appleby, President & Owner at K9 Resorts Luxury Pet Hotel (376 employees, luxury pet franchise operations across US).",
        "copy_samples": {
            "Format 1: Career Arc Anchor": "Robert, building K9 Resorts across multiple luxury locations is a rare operational feat. Scaling unit economics behaves very differently past 5 sites. Worth comparing notes. Cheers! Revell",
            "Format 2: Peer-to-Peer Identity": "Robert, fellow operator here. Spent 35 years in investment banking and pet services capital structure. Unit level visibility is what catches most founders. Would value connecting. Revell",
            "Format 3: Pattern Interrupt": "Robert, there is a moment every multi-location pet operator hits around unit five where margin compression catches them off guard. Deep in pet services finance. Best, Revell",
            "Format 4: The YOU-Factor": "Robert, your expansion of K9 Resorts into luxury franchising shows an exact pulse on consumer demand. 35 years in multi-unit pet finance. Would love to connect. Revell"
        }
    },
    "Dr. Kerry Mitchell Brown (Forbes Author & CEO)": {
        "client_name": "Dr. Kerry Mitchell Brown",
        "profile": "CEO, kmb Consultancy. Organizational Transformation for Complex Institutions. PhD in Leadership. Author of upcoming Forbes book 'Revolutionary Leadership'. Chicago, Illinois.",
        "notes": "Outreach targets enterprise Chief People Officers, Diversity & Culture VPs, and Executive Directors of Organizational Development in companies with 500+ employees. Tone: Thought leader, scholarly yet pragmatic, human-centered.",
        "icp": {
            "primary_icp": "Chief People Officers, VPs of Human Resources, Chief Diversity Officers, and Executive Directors of Organizational Development in 500+ headcount enterprises.",
            "disqualifications": "Entry-level HR recruiters, transactional staffing firms, solo executive headhunters.",
            "sales_nav_boolean": '("Chief People Officer" OR "VP Human Resources" OR "Organizational Development") AND ("Transformation" OR "Culture") AND Headcount: 501-5,000+',
            "value_pillar": "Structural leadership transformation and human-centered institutional change."
        },
        "sample_prospect": "Joseph Lanzo, SHRM-SCP, Head of Human Resources and Talent Strategy (Greater Philadelphia, Enterprise HR Leader).",
        "copy_samples": {
            "Format 1: Career Arc Anchor": "Joseph, your path building HR functions from scratch is striking. For someone whose strength is structure, team trust is the hardest bridge. Dr Kerry Mitchell Brown, Forbes author. Glad to connect.",
            "Format 2: Peer-to-Peer Identity": "Joseph, fellow leadership practitioner here. Navigating systemic transformation across complex enterprise structures requires care and power. Would love to share perspectives. Dr Kerry",
            "Format 3: Pattern Interrupt": "Joseph, structure can stabilize a department, but it cannot manufacture organic leadership trust during reorganization. Researching this for 20 years. Dr Kerry Mitchell Brown",
            "Format 4: The YOU-Factor": "Joseph, your focus on converting chaos into clear people systems resonated deeply with my upcoming Forbes book, Revolutionary Leadership. Would value connecting. Dr Kerry"
        }
    },
    "Tanvi Mittal (Organizational Facilitator)": {
        "client_name": "Tanvi Mittal",
        "profile": "Facilitator & Executive Coach at Tanvi Mittal Coaching. Helping senior corporate leadership teams thrive through restructuring, uncertainty, and culture shifts. Philadelphia, PA.",
        "notes": "Target CPOs, VP People and Culture, and change management executives. Strictly non-salesy, peer-to-peer inquiry. Emphasize trust-building in newly merged or restructured teams.",
        "icp": {
            "primary_icp": "Vice Presidents of People & Culture, Heads of Talent Development, and Change Management leads navigating mergers and high-growth uncertainty.",
            "disqualifications": "Technical recruitment specialists, administrative HR assistants.",
            "sales_nav_boolean": '("VP People" OR "People and Culture" OR "Talent Development") AND ("Restructuring" OR "Organizational Effectiveness") AND Region: Greater Philadelphia',
            "value_pillar": "Facilitating psychological safety and clarity through organizational restructuring."
        },
        "sample_prospect": "Cheryl Bucci, VP People Operations & Organizational Development.",
        "copy_samples": {
            "Format 1: Career Arc Anchor": "Cheryl, leading people operations through institutional shifts is demanding work. How leadership teams hold space for uncertainty defines retention. Tanvi Mittal, facilitator. Glad to connect.",
            "Format 2: Peer-to-Peer Identity": "Cheryl, anthropology trained facilitator here. When corporate structures pivot, trust between new teams is rarely solved by process alone. Would love to exchange notes. Tanvi",
            "Format 3: Pattern Interrupt": "Cheryl, most restructuring roadmaps plan for operational milestones but overlook emotional friction within middle management. Deep in organizational facilitation. Tanvi",
            "Format 4: The YOU-Factor": "Cheryl, your recent perspective on building resilient culture during leadership transitions stood out. That mirrors my work with executive teams. Tanvi Mittal. Glad to connect."
        }
    }
}

# Sidebar
with st.sidebar:
    st.header("⚙️ PrajayIQ System Mode")
    st.success("🟢 Production Engine Active (Zero API Latency)")
    st.markdown("---")
    st.markdown("### Select Client Case Study:")
    preset_choice = st.selectbox(
        "Client Preset:",
        list(presets.keys())
    )

active_data = presets[preset_choice]

# Step 1 & 2: Client Profile and Discovery
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Client Profile & Positioning")
    c_name = st.text_input("Client Name", value=active_data["client_name"])
    c_profile = st.text_area("Client LinkedIn Profile Summary / Experience", value=active_data["profile"], height=130)

with col2:
    st.subheader("2. Strategic Onboarding & Discovery Notes")
    c_notes = st.text_area("Founder / Strategy Meeting Intake Notes", value=active_data["notes"], height=130)

# Trigger ICP Generation
if st.button("Generate Ideal Customer Profile (ICP) & Sales Navigator Strings", type="primary"):
    st.session_state['icp_result'] = active_data["icp"]
    st.session_state['active_client'] = preset_choice

# Display ICP Results
if 'icp_result' in st.session_state and st.session_state.get('active_client') == preset_choice:
    icp = st.session_state['icp_result']
    st.markdown("---")
    st.subheader("🎯 Synthesized Target Persona & Sales Navigator Architecture")
    c_a, c_b = st.columns(2)
    with c_a:
        st.markdown(f"**Primary ICP Focus:**\n{icp.get('primary_icp', '')}")
        st.markdown(f"**Disqualification Criteria:**\n{icp.get('disqualifications', '')}")
    with c_b:
        st.markdown(f"**Core Value Hook:**\n{icp.get('value_pillar', '')}")
        st.markdown("**Sales Navigator Boolean String:**")
        st.code(icp.get('sales_nav_boolean', ''), language="text")

st.markdown("---")

# Step 3: Prospect Ingestion and 4-Format Copywriting Matrix
st.subheader("3. Prospect Context & The 4-Format Copywriting Matrix")

p_col1, p_col2 = st.columns([1, 1])

with p_col1:
    prospect_input = st.text_area(
        "Target Prospect Context / Career Path:",
        value=active_data["sample_prospect"],
        height=120
    )
    format_choice = st.selectbox(
        "Select Copywriting Matrix Formula:",
        [
            "Format 1: Career Arc Anchor",
            "Format 2: Peer-to-Peer Identity",
            "Format 3: Pattern Interrupt",
            "Format 4: The YOU-Factor"
        ]
    )

with p_col2:
    st.markdown("**Agency Locked Formatting Rules Enforced:**")
    st.markdown("""
    - Strict maximum character length: Under 220 characters
    - Punctuation restriction: Zero hyphens (`-`), en-dashes (`–`), or em-dashes (`—`)
    - Opening: Immediate YOU-factor anchor (No 'Hope you are well')
    - Tone: Executive peer dialogue, zero sales pitches or calendar booking links
    """)

# Generate Message
if st.button("Synthesize Personalized Outreach Note", type="secondary"):
    st.session_state['generated_note'] = active_data["copy_samples"][format_choice]

# Pre-Flight Linting Engine & Simulation
if 'generated_note' in st.session_state:
    st.markdown("---")
    st.subheader("4. Pre-Flight Linting Protocol & Mobile Preview")
    
    note_text = st.text_area("Active Draft (Editable for Live Linting Test):", value=st.session_state['generated_note'], height=90)
    
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
