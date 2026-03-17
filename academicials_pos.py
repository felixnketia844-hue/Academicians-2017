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
        with open('members_data.json', 'w') as f:
            json.dump({}, f)
    with open('members_data.json', 'r') as f:
        return json.load(f)

def save_data(data):
    with open('members_data.json', 'w') as f:
        json.dump(data, f, indent=4)

# --- SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- LOGIN / LOGOUT ---
def login():
    st.session_state.logged_in = True
    st.experimental_rerun()

def logout():
    st.session_state.logged_in = False
    st.experimental_rerun()

# --- PAGE CONFIG ---
st.set_page_config(page_title="Academicians 2017", layout="wide")

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🔒 Login")
    if st.button("Login", key="login_btn"):
        login()
    st.stop()

# --- MARQUEE HEADER ---
st.markdown("""
<style>
@keyframes scroll-left {
  0% { transform: translateX(100%); }
  100% { transform: translateX(-100%); }
}
.marquee {
  overflow: hidden;
  white-space: nowrap;
  box-sizing: border-box;
  background-color:#1E3A8A;
  border-radius:10px;
  padding: 15px;
  color:white;
  font-weight:bold;
  font-size:22px;
}
.marquee span {
  display: inline-block;
  padding-left: 100%;
  animation: scroll-left 15s linear infinite;
}
.submarquee {
  overflow: hidden;
  white-space: nowrap;
  box-sizing: border-box;
  font-size:16px;
  color:#f0f0f0;
  margin-top:5px;
}
.submarquee span {
  display:inline-block;
  padding-left:100%;
  animation: scroll-left 20s linear infinite;
}
</style>

<div class="marquee"><span>✨ ACADEMICIANS 2017 OFFICIAL LEDGER ✨</span></div>
<div class="submarquee"><span>Manage members | Track payments | Update or Delete | Safe & secure ledger</span></div>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
data = load_data()

# --- SIDEBAR ---
st.sidebar.header("🚪 Session")
if st.sidebar.button("Logout", key="logout_btn"):
    logout()

st.sidebar.divider()
st.sidebar.header("📥 Data Entry")
target_year = st.sidebar.selectbox("Year", [str(y) for y in range(2024, 2031)], key="year_select")
target_month = st.sidebar.selectbox(
    "Month",
    ["January","February","March","April","May","June",
     "July","August","September","October","November","December"], key="month_select"
)

# --- ADD NEW MEMBER ---
with st.sidebar.expander("➕ Add New Member"):
    new_name = st.text_input("Full Name", key="new_name")
    new_phone = st.text_input("Phone", key="new_phone")
    new_gender = st.radio("Gender", ["Male", "Female"], horizontal=True, key="new_gender")
    if st.button("Save Member", key="save_member_btn"):
        if target_year not in data:
            data[target_year] = {}
        if new_name.strip():
            data[target_year][new_name] = {"phone": new_phone, "gender": new_gender, "payments": []}
            save_data(data)
            st.success("Member Saved!")
            st.experimental_rerun()
        else:
            st.error("Name is required!")

# --- MAIN LEDGER ---
st.title(f"📊 Ledger: {target_month} {target_year}")

if target_year in data and data[target_year]:
    search = st.text_input("🔍 Search Name or Gender", key="search_input").strip().lower()
    members = data[target_year]

    # Stats
    males = len([n for n,i in members.items() if i.get('gender')=="Male"])
    females = len([n for n,i in members.items() if i.get('gender')=="Female"])
    st.write(f"👥 **Stats:** {males} Males | {females} Females")

    # Table header
    col1, col2, col3, col4 = st.columns([2,1,1,1])
    col1.write("**Member Detail**")
    col2.write("**Total Paid**")
    col3.write("**Action**")
    col4.write("**Manage**")
    st.divider()

    for idx, name in enumerate(list(members.keys())):
        info = members[name]
        gender_icon = "👨" if info.get('gender')=="Male" else "👩"

        # Search filter
        if not search or search in name.lower() or search in info.get('gender','').lower():
            paid = sum(p['amount'] for p in info['payments'])
            c1, c2, c3, c4 = st.columns([2,1,1,1])
            c1.write(f"{gender_icon} **{name}**\n({info['phone']})")
            c2.write(f"GHS {paid:.2f}")

            # --- CUSTOM PAYMENT ---
            amount_key = f"amt_{idx}"
            amount = c3.number_input("Amount", min_value=0.0, key=amount_key)
            pay_key = f"pay_{idx}"
            if c3.button("💳 Pay", key=pay_key):
                if amount > 0:
                    info['payments'].append({"amount": amount, "month": target_month, "date": str(datetime.now())})
                    save_data(data)
                    st.success("Payment added!")
                    st.experimental_rerun()

            # --- UPDATE / DELETE ---
            new_p_key = f"edit_p_{idx}"
            new_g_key = f"edit_g_{idx}"
            new_p = st.text_input("Phone", value=info['phone'], key=new_p_key)
            new_g = st.selectbox("Gender", ["Male","Female"], index=0 if info.get('gender')=="Male" else 1, key=new_g_key)
            if st.button("Update Member", key=f"up_{idx}"):
                info['phone'] = new_p
                info['gender'] = new_g
                save_data(data)
                st.success("Updated!")
                st.experimental_rerun()

            confirm_key = f"confirm_{idx}"
            if st.checkbox("Confirm Delete", key=confirm_key):
                if st.button("🗑️ Delete Member", key=f"del_{idx}"):
                    del data[target_year][name]
                    save_data(data)
                    st.warning("Deleted!")
                    st.experimental_rerun()
else:
    st.warning("No records for this year yet.")
