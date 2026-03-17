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

# --- LOGIN SESSION ---
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

# --- SEARCH ---
search = st.text_input("🔍 Search Name or Gender", "")

if target_year in data and data[target_year]:
    members = data[target_year]

    # --- STATS ---
    males = len([i for i in members.values() if i.get('gender') == "Male"])
    females = len([i for i in members.values() if i.get('gender') == "Female"])
    st.write(f"👥 **Stats:** {males} Males | {females} Females")

    st.divider()

    # --- LOOP MEMBERS ---
    for idx, (name, info) in enumerate(members.items()):

        # --- SEARCH FILTER ---
        if search:
            if search.lower() not in name.lower() and search.lower() not in info.get('gender','').lower():
                continue

        gender_icon = "👨" if info.get('gender') == "Male" else "👩"
        total_paid = sum(p['amount'] for p in info.get('payments', []))

        st.write(f"### {gender_icon} {name}")
        st.write(f"📞 {info['phone']} | 💰 Total: GHS {total_paid:.2f}")

        # --- FORM (VERY IMPORTANT) ---
        with st.form(key=f"form_{idx}"):

            col1, col2, col3 = st.columns(3)

            # AMOUNT
            amount = col1.number_input("Enter Amount", min_value=0.0, key=f"amt_{idx}")

            # UPDATE
            new_phone = col2.text_input("Phone", value=info['phone'], key=f"phone_{idx}")
            new_gender = col3.selectbox(
                "Gender",
                ["Male", "Female"],
                index=0 if info.get('gender') == "Male" else 1,
                key=f"gender_{idx}"
            )

            # BUTTONS
            pay_btn = st.form_submit_button("💳 Pay")
            update_btn = st.form_submit_button("Update")
            delete_btn = st.form_submit_button("🗑️ Delete")

            # --- ACTIONS ---
            if pay_btn:
                if amount > 0:
                    info['payments'].append({
                        "amount": amount,
                        "month": target_month,
                        "date": str(datetime.now())
                    })
                    save_data(data)
                    st.success(f"{name} paid GHS {amount}")
                    st.rerun()

            if update_btn:
                info['phone'] = new_phone
                info['gender'] = new_gender
                save_data(data)
                st.success("Updated!")
                st.rerun()

            if delete_btn:
                del data[target_year][name]
                save_data(data)
                st.warning(f"{name} deleted")
                st.rerun()

        st.divider()

else:
    st.warning("No records for this year yet.")
