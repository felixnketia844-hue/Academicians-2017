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

# --- LOGIN/LOGOUT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = True

def logout():
    st.session_state.logged_in = False
    st.rerun()

# --- PAGE CONFIG ---
st.set_page_config(page_title="Academicians 2017", layout="wide")

st.markdown(
    '<div style="background-color:#1E3A8A;color:white;padding:15px;text-align:center;border-radius:10px;font-weight:bold;">✨ ACADEMICIANS 2017 OFFICIAL LEDGER ✨</div>',
    unsafe_allow_html=True
)

if not st.session_state.logged_in:
    st.info("You have logged out.")
    if st.button("Log Back In"):
        st.session_state.logged_in = True
        st.rerun()
    st.stop()

data = load_data()

# --- SIDEBAR ---
st.sidebar.header("🚪 Session")
if st.sidebar.button("Logout of System"):
    logout()

st.sidebar.divider()
st.sidebar.header("📥 Data Entry")

target_year = st.sidebar.selectbox("Year", [str(y) for y in range(2024, 2031)])
target_month = st.sidebar.selectbox(
    "Month",
    ["January","February","March","April","May","June",
     "July","August","September","October","November","December"]
)

# --- ADD MEMBER ---
with st.sidebar.expander("➕ Add New Member"):
    new_name = st.text_input("Full Name")
    new_phone = st.text_input("Phone")
    new_gender = st.radio("Gender", ["Male", "Female"], horizontal=True)

    if st.button("Save Member"):
        if target_year not in data:
            data[target_year] = {}

        if new_name.strip() != "":
            data[target_year][new_name] = {
                "phone": new_phone,
                "gender": new_gender,
                "payments": []
            }
            save_data(data)
            st.success("Member Saved!")
            st.rerun()

# --- MAIN ---
st.title(f"📊 Ledger: {target_month} {target_year}")

# --- SEARCH BAR (FIXED) ---
search = st.text_input("🔍 Search Name or Gender", "")

if target_year in data and data[target_year]:
    members = data[target_year]

    # --- STATS ---
    males = len([i for i in members.values() if i.get('gender') == "Male"])
    females = len([i for i in members.values() if i.get('gender') == "Female"])
    st.write(f"👥 **Stats:** {males} Males | {females} Females")

    st.divider()

    for idx, (name, info) in enumerate(members.items()):

        # --- SEARCH FILTER FIX ---
        if search:
            if search.lower() not in name.lower() and search.lower() not in info.get('gender','').lower():
                continue

        gender_icon = "👨" if info.get('gender') == "Male" else "👩"

        # --- TOTAL AMOUNT ---
        total_paid = sum(p['amount'] for p in info.get('payments', []))

        c1, c2, c3, c4 = st.columns([2,1,1,1])

        # MEMBER INFO
        c1.write(f"{gender_icon} **{name}**\n({info['phone']})")

        # TOTAL
        c2.write(f"GHS {total_paid:.2f}")

        # --- ADD AMOUNT (FIXED) ---
        amount = c3.number_input("Amount", min_value=0.0, key=f"amt_{idx}")

        if c3.button("💳 Pay", key=f"pay_{idx}"):
            if amount > 0:
                info['payments'].append({
                    "amount": amount,
                    "month": target_month,
                    "date": str(datetime.now())
                })
                save_data(data)
                st.success(f"{name} paid GHS {amount}")
                st.rerun()

        # --- UPDATE ---
        new_phone = c4.text_input("Phone", value=info['phone'], key=f"phone_{idx}")
        new_gender = c4.selectbox(
            "Gender",
            ["Male", "Female"],
            index=0 if info.get('gender')=="Male" else 1,
            key=f"gender_{idx}"
        )

        if c4.button("Update", key=f"update_{idx}"):
            info['phone'] = new_phone
            info['gender'] = new_gender
            save_data(data)
            st.success("Updated!")
            st.rerun()

        # --- DELETE (FIXED) ---
        if c4.button("🗑️ Delete", key=f"delete_{idx}"):
            del data[target_year][name]
            save_data(data)
            st.warning(f"{name} deleted")
            st.rerun()

        st.divider()

else:
    st.warning("No records for this year yet.")
