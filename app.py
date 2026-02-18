

import streamlit as st
import requests
import io
import base64

# --- HELPER: IMAGE TO BASE64 ---
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# --- CONFIG & THEME ---
st.set_page_config(page_title="EA Architect", page_icon="🏛️", layout="centered")

# Attempt to load the background image
bin_str = get_base64_of_bin_file('BACKGROUND.png')
bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
        color: #E0E0E0;
    }}
    /* Dark overlay to ensure text is readable over the custom image */
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(11, 14, 20, 0.85); 
        z-index: -1;
    }}
""" if bin_str else ".stApp { background-color: #0B0E14; color: #E0E0E0; }"

st.markdown(bg_css + """
    h1, h2, h3 { color: #00FFA3 !important; font-family: 'Courier New', Courier, monospace; }
    
    .slogan { 
        color: #FFFFFF; 
        font-family: 'Courier New', Courier, monospace; 
        font-size: 1.1em; 
        margin-top: -20px; 
        margin-bottom: 30px; 
        letter-spacing: 2px;
        opacity: 0.9;
    }
    
    h3 { opacity: 0.7; } 
    .stProgress > div > div > div > div { background-color: #00FFA3; }
    .stButton>button {
        width: 100%; border-radius: 4px; border: 1px solid #00FFA3;
        background-color: transparent; color: #00FFA3; font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #00FFA3; border-color: #FFFFFF; color: #0B0E14; }
    .summary-box { background-color: #161B22; padding: 25px; border-radius: 12px; border-left: 5px solid #00FFA3; margin-bottom: 20px; }
    .price-tag { font-size: 28px; color: #00FFA3; font-weight: bold; text-align: center; padding: 15px; border: 2px dashed #00FFA3; border-radius: 8px; margin: 20px 0; }
    .counter-text { font-size: 0.85em; margin-top: -5px; margin-bottom: 10px; text-align: right; }
    .success-card { background-color: #161B22; padding: 40px; border-radius: 15px; text-align: center; border: 1px solid #00FFA3; }
    </style>
    """, unsafe_allow_html=True)

# --- TELEGRAM SETTINGS ---
try:
    TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    TELEGRAM_CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]
except:
    TELEGRAM_BOT_TOKEN = ""
    TELEGRAM_CHAT_ID = ""
    
def send_telegram_message(message, files=None):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        st.error("Missing Token or Chat ID in the code settings.")
        return False
    base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
    try:
        text_payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
        text_response = requests.post(f"{base_url}/sendMessage", json=text_payload, timeout=10)
        if files:
            for file_label, file_data in files.items():
                if file_data:
                    requests.post(f"{base_url}/sendPhoto", data={"chat_id": TELEGRAM_CHAT_ID, "caption": f"Visual for {file_label}"}, files={"photo": file_data}, timeout=15)
        return True
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return False

# --- SESSION STATE ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'data' not in st.session_state: st.session_state.data = {}
if 'submitted' not in st.session_state: st.session_state.submitted = False

# --- HEADER WITH LOGO ---
col_logo, col_title = st.columns([1, 4])
with col_logo:
    try:
        st.image("LOGO.png", width=80)
    except:
        st.write("🏛️") # Fallback icon
with col_title:
    st.title("EA ARCHITECT")

# --- STEP 1: INTAKE ---
if st.session_state.step == 1:
    st.markdown('<p class="slogan">STRATEGY TO BOT</p>', unsafe_allow_html=True)
    st.write("### Step 1: Trading Bot Setup")
    st.progress(0.25)
    st.error("⚠️ **Development Environment:** MetaTrader 5 (MT5) Only.")
    with st.form("page1"):
        bot_name = st.text_input("What is the name of the bot you'd like to create?", 
                                 value=st.session_state.data.get('bot_name', ''),
                                 placeholder="e.g. Alpha Bot, Gold Hunter, ScalpMaster Pro")
        
        exp = st.select_slider("Trading experience?", options=["Beginner", "Intermediate", "Professional"],
                               value=st.session_state.data.get('experience', 'Beginner'))
        
        prog = st.radio("Programming knowledge?", ["None", "Basic", "Coder"], 
                        index=["None", "Basic", "Coder"].index(st.session_state.data.get('coding', 'None')))
        
        source = st.radio("Discovery source?", ["Social Media", "Friend", "Search", "Other"], 
                          index=["Social Media", "Friend", "Search", "Other"].index(st.session_state.data.get('referral', 'Social Media')),
                          horizontal=True)
        
        if st.form_submit_button("Start Architecture →"):
            if bot_name:
                st.session_state.data.update({'bot_name': bot_name, 'experience': exp, 'coding': prog, 'referral': source})
                st.session_state.step = 2
                st.rerun()
            else: st.warning("Please provide a name for your bot to continue.")

# --- STEP 2: STRATEGY ---
elif st.session_state.step == 2:
    st.write(f"### Step 2: Architecture for {st.session_state.data.get('bot_name', 'your EA')}")
    st.progress(0.50)
    with st.form("page2"):
        st.subheader("Logic Definition")
        entry = st.text_area("Entry Logic (Include Timeframes)", 
                             value=st.session_state.data.get('entry', ''),
                             max_chars=250, height=150, placeholder="Define your buy/sell rules here...")
        
        color_e = "#00FFA3" if len(entry) < 225 else "#FF4B4B"
        st.markdown(f'<p class="counter-text" style="color: {color_e}"> 250 characters</p>', unsafe_allow_html=True)
        
        entry_img = st.file_uploader("Optional: Upload Entry Visual (Screenshot/Chart)", type=['png', 'jpg', 'jpeg'], key="entry_u")
        st.divider()
        
        exit_r = st.text_area("Exit Logic (Close Conditions)", 
                              value=st.session_state.data.get('exit', ''),
                              max_chars=120, height=100, placeholder="Define when to close trades...")
        
        color_x = "#00FFA3" if len(exit_r) < 100 else "#FF4B4B"
        st.markdown(f'<p class="counter-text" style="color: {color_x}"> 120 characters</p>', unsafe_allow_html=True)
        
        exit_img = st.file_uploader("Optional: Upload Exit Visual (Screenshot/Chart)", type=['png', 'jpg', 'jpeg'], key="exit_u")
        st.divider()
        
        assets = st.text_input("Target Assets", 
                               value=st.session_state.data.get('assets', ''),
                               max_chars=50, placeholder="e.g. XAUUSD, EURUSD, BTC")
        
        col1, col2 = st.columns(2)
        if col1.form_submit_button("← Back"):
            st.session_state.step = 1
            st.rerun()
        if col2.form_submit_button("Next: Risk Management →"):
            if entry and exit_r and assets:
                st.session_state.data.update({'entry': entry, 'exit': exit_r, 'assets': assets, 'entry_img': entry_img, 'exit_img': exit_img})
                st.session_state.step = 3
                st.rerun()
            else: st.warning("Please fill the logic fields to continue.")

# --- STEP 3: RISK & CAPITAL ---
elif st.session_state.step == 3:
    st.write("### Step 3: Risk & Capital Settings")
    st.progress(0.75)
    with st.form("page3"):
        capital = st.number_input("Initial Trading Capital ($)", min_value=10, 
                                  value=st.session_state.data.get('capital', 1000), step=100)
        
        st.subheader("Account-Based Risk (%)")
        c_r1, c_r2 = st.columns(2)
        sl_pct = c_r1.number_input("Stop Loss (% of Account)", min_value=0.1, max_value=100.0, 
                                   value=st.session_state.data.get('sl_pct', 1.0))
        tp_pct = c_r2.number_input("Take Profit (% of Account)", min_value=0.1, max_value=100.0, 
                                   value=st.session_state.data.get('tp_pct', 2.0))
        
        st.subheader("Automation & Advanced Modules")
        selected_features = st.multiselect(
            "Select the modules to integrate into your EA:",
            options=[
                "Trailing Stop", "Break-even Logic", "News Filter (API)",
                "Trading Session Timer", "Spread Filter", "On-Screen Dashboard",
                "Daily Loss Limit", "Daily Target Profit Limit",
                "MQL5 Alerts (Trade Open/Close)", "Magic Number Manager"
            ],
            default=st.session_state.data.get('features', ["Trailing Stop", "Break-even Logic"])
        )
        
        risk_notes = st.text_area("Specific Risk Rules", 
                                  value=st.session_state.data.get('risk_notes', ''),
                                  max_chars=50, placeholder="e.g. No trading on Fridays, Max 3 trades per day.")
        
        color_rn = "#00FFA3" if len(risk_notes) < 30 else "#FF4B4B"
        st.markdown(f'<p class="counter-text" style="color: {color_rn}"> 50 characters</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        if col1.form_submit_button("← Back"):
            st.session_state.step = 2
            st.rerun()
        if col2.form_submit_button("Review Quote →"):
            st.session_state.data.update({'capital': capital, 'sl_pct': sl_pct, 'tp_pct': tp_pct, 'features': selected_features, 'risk_notes': risk_notes})
            st.session_state.step = 4
            st.rerun()

# --- STEP 4: REVIEW & PRICING ---
elif st.session_state.step == 4:
    st.write("### Step 4: Final Review & Quote")
    st.progress(1.0)
    
    total_chars = len(st.session_state.data.get('entry', '')) + len(st.session_state.data.get('exit', ''))
    if total_chars > 300:
        complexity_label, complexity_fee = "🔴 Complex Strategy", 35.0
    elif total_chars > 150:
        complexity_label, complexity_fee = "🟡 Medium Level Strategy", 25.0
    else:
        complexity_label, complexity_fee = "🟢 Easy Strategy", 15.0

    base_fee = 59.0
    feature_fee = len(st.session_state.data.get('features', [])) * 5.0
    raw_subtotal = base_fee + feature_fee + complexity_fee
    subtotal = min(raw_subtotal, 200.0)
    paypal_fee = subtotal * 0.05 
    total_quote = subtotal + paypal_fee

    st.markdown(f"""
    <div class="summary-box">
        <h4>📋 Logic Architect Report: {st.session_state.data.get('bot_name', 'Unnamed Bot')}</h4>
        <b>Assets:</b> {st.session_state.data.get('assets', 'Not specified')}<br>
        <b>Complexity Level:</b> {complexity_label}<br>
        <b>Risk Config:</b> SL {st.session_state.data.get('sl_pct', 0)}% / TP {st.session_state.data.get('tp_pct', 0)}%<br>
        <b>Selected Modules:</b> {", ".join(st.session_state.data.get('features', [])) if st.session_state.data.get('features') else "None"}<br>
        <b>Visuals Provided:</b> {"Entry ✅" if st.session_state.data.get('entry_img') else "Entry ❌"}, {"Exit ✅" if st.session_state.data.get('exit_img') else "Exit ❌"}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="price-tag">Estimated Fee: ${total_quote:.2f} USD</div>', unsafe_allow_html=True)
    
    with st.form("final"):
        contact = st.text_input("Telegram Handle / Email", value=st.session_state.data.get('contact', ''), placeholder="@username")
        st.write("⚠️ *Review your logic above. Fees are based on complexity and modules selected.*")
        col1, col2 = st.columns(2)
        if col1.form_submit_button("← Edit"):
            st.session_state.step = 3
            st.rerun()
        
        # Disable button if already submitted to prevent spam
        submit_btn = col2.form_submit_button("🚀 Submit to Architect", disabled=st.session_state.submitted)
        
        if submit_btn:
            if contact:
                st.session_state.submitted = True
                st.session_state.data['contact'] = contact
                d = st.session_state.data
                
                # --- TELEGRAM REPORT GENERATION ---
                features_list = ", ".join(d.get('features', [])) if d.get('features') else "None"
                
                report = (
                    f"<b>🏛️ NEW EA ORDER</b>\n\n"
                    f"<b>🤖 Bot:</b> {d.get('bot_name')}\n"
                    f"<b>👤 Client:</b> {contact}\n"
                    f"<b>💰 Complexity:</b> {complexity_label}\n"
                    f"<b>🏦 Capital:</b> ${d.get('capital'):,.2f}\n"
                    f"<b>🛠️ Assets:</b> {d.get('assets')}\n"
                    f"<b>📏 Risk:</b> SL {d.get('sl_pct')}% | TP {d.get('tp_pct')}%\n\n"
                    f"<b>🧩 Modules:</b>\n{features_list}\n\n"
                    f"<b>🧠 Profile:</b> Exp: {d.get('experience')} | Code: {d.get('coding')}\n\n"
                    f"<b>📝 Entry Logic:</b>\n{d.get('entry')}\n\n"
                    f"<b>🚪 Exit Logic:</b>\n{d.get('exit')}\n\n"
                    f"<b>⚠️ Specific Risk Rules:</b>\n{d.get('risk_notes') if d.get('risk_notes') else 'None'}\n\n"
                    f"<b>💵 Quote:</b> ${total_quote:.2f}"
                )
                
                telegram_files = {}
                if d.get('entry_img'): telegram_files['Entry'] = d['entry_img'].getvalue()
                if d.get('exit_img'): telegram_files['Exit'] = d['exit_img'].getvalue()
                
                if send_telegram_message(report, files=telegram_files if telegram_files else None):
                    st.session_state.step = 5
                    st.rerun()
            else: st.error("Please provide contact info.")

# --- STEP 5: SUCCESS PAGE ---
elif st.session_state.step == 5:
    # Only show balloons once when reaching this step
    if st.session_state.submitted:
        st.balloons()
        st.session_state.submitted = False # Reset flag so balloons don't re-trigger on simple page refreshes

    st.markdown(f"""
    <div class="success-card">
        <h2 style="margin-top:0;">✅ Architecture Submitted!</h2>
        <p style="font-size:1.2em;">Excellent, <b>{st.session_state.data.get('bot_name')}</b> is now in the queue.</p>
        <hr style="border-color: #00FFA3; opacity: 0.3;">
        <p>Your strategy details and visuals have been sent to the developers.</p>
        <p><b>What happens next?</b></p>
        <ul style="text-align: left; display: inline-block;">
            <li>The developers will review your logic complexity.</li>
            <li>You will receive a message at <b>{st.session_state.data.get('contact')}</b>.</li>
            <li>Once the quote is confirmed, development begins.</li>
        </ul>
        <br><br>
        <p style="opacity:0.6; font-style:italic;">You can close this page now.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start New Project"):
        st.session_state.step = 1
        st.session_state.data = {}
        st.session_state.submitted = False # Explicitly reset flag for new project
        st.rerun()


st.caption("MT5 EA Architect System © 2026")


