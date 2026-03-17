# -*- coding: utf-8 -*-
""
#Created on Mon Mar 16 18:31:12 2026
#@author: felix
# Student Monthly Dues System
import streamlit as st
import json
import os
from datetime import datetime

# --- DATABASE FUNCTIONS ---
def load_data():
    if not os.path.exists('members_data.json'):
        # Start with a clean list of years including 2017
        years = [str(y) for y in range(2017, 2031)]
        with open('members_data.json', 'w') as f: 
            json.dump({"years": years, "data": {}}, f)
    with open('members_data.json', 'r') as f: return json.load(f)

def save_data(data):
    with open('members_data.json', 'w') as f: json.dump(data, f, indent=4)

# --- LOGIN LOGIC ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login(pin):
    if pin == "2017":
        st.session_state.logged_in = True
        st.rerun()
    else:
        st.error("❌ Wrong PIN")

def logout():
    st.session_state.logged_in = False
    st.rerun()

# --- PAGE CONFIG ---
st.set_page_config(page_title="Academicians 2017", layout="wide")

# Header Marquee
st.markdown('<div style="background-color:#1E3A8A;color:white;padding:15px;text-align:center;border-radius:10px;font-weight:bold;">✨ ACADEMICIANS 2017 OFFICIAL LEDGER ✨</div>', unsafe_allow_html=True)

# Check Login
if not st.session_state.logged_in:
    st.subheader("🔒 Secure Access")
    user_pin = st.text_input("Enter PIN to Access Ledger", type="password")
    if st.button("Login"):
        login(user_pin)
    st.stop()

db = load_data()
data = db["data"]

# --- SIDEBAR ---
st.sidebar.header("🚪 Session")
if st.sidebar.button("Logout of System"):
    logout()

st.sidebar.divider()
st.sidebar.header("📥 Data Entry")
target_year = st.sidebar.selectbox("Year", db["years"])
target_month = st.sidebar.selectbox("Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

with st.sidebar.expander("➕ Add New Member"):
    new_name = st.text_input("Full Name")
    new_phone = st.text_input("Phone")
    new_gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    if st.button("Save Member"):
        if target_year not in data: data[target_year] = {}
        if new_name:
            data[target_year][new_name] = {"phone": new_phone, "gender": new_gender, "payments": []}
            save_data(db)
            st.success("Member Saved!")
            st.rerun()

# --- MAIN INTERFACE ---
st.title(f"📊 Ledger: {target_month} {target_year}")

if target_year in data and data[target_year]:
    search = st.text_input("🔍 Search Name or Gender")
    members = data[target_year]
    
    # Stats Summary
    males = len([n for n, i in members.items() if i.get('gender') == "Male"])
    females = len([n for n, i in members.items() if i.get('gender') == "Female"])
    st.write(f"👥 **Stats:** {males} Males | {females} Females")

    # Table Header
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    col1.write("**Member Detail**")
    col2.write("**Total Paid**")
    col3.write("**Add Payment**")
    col4.write("**Manage**")
    st.divider()

    for name in list(members.keys()):
        info = members[name]
        if search.lower() in name.lower() or search.lower() in info.get('gender', '').lower():
            paid = sum(p['amount'] for p in info['payments'])
            gender_icon = "👨" if info.get('gender') == "Male" else "👩"
            
            c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
            c1.write(f"{gender_icon} **{name}**\n({info['phone']})")
            c2.write(f"GHS {paid:.2f}")
            
            # IMPROVED PAYMENT BOX
            with c3.popover("💸 Pay"):
                amt = st.number_input("Amount (GHS)", min_value=1.0, value=50.0, step=10.0, key=f"amt_{name}")
                if st.button("Confirm Payment", key=f"pay_btn_{name}"):
                    info['payments'].append({"amount": amt, "month": target_month, "date": str(datetime.now())})
                    save_data(db)
                    st.balloons()
                    st.rerun()

            # MANAGE POP-OVER
            with c4.popover("⚙️"):
                st.write("Edit Info")
                new_p = st.text_input("Phone", value=info['phone'], key=f"edit_p_{name}")
                new_g = st.selectbox("Gender", ["Male", "Female"], index=0 if info.get('gender')=="Male" else 1, key=f"edit_g_{name}")
                if st.button("Update", key=f"up_{name}"):
                    info['phone'] = new_p
                    info['gender'] = new_g
                    save_data(db)
                    st.rerun()
                if st.button("🗑️ Delete", key=f"del_{name}"):
                    del data[target_year][name]
                    save_data(db)
                    st.rerun()

    # WhatsApp Report
    st.divider()
    if st.button("📱 Generate WhatsApp Report"):
        report = f"*ACADEMICIANS 2017 - {target_month} {target_year}*\n"
        for n, i in members.items():
            p = sum(pm['amount'] for pm in i['payments'])
            report += f"• {n}: GHS {p}\n"
        st.text_area("Copy this:", value=report)
else:
    st.info(f"No members found for {target_year} yet.")
