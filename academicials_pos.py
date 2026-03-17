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

# --- PAGE CONFIG ---
st.set_page_config(page_title="Academicians 2017", layout="wide")

# Custom Header
st.markdown('<div style="background-color:#1E3A8A;color:white;padding:15px;text-align:center;border-radius:10px;font-weight:bold;font-size:24px;">✨ ACADEMICIANS 2017 OFFICIAL LEDGER ✨</div>', unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = True

data = load_data()

# --- SIDEBAR ---
st.sidebar.header("📥 Data Management")
target_year = st.sidebar.selectbox("Select Year", [str(y) for y in range(2024, 2031)])
target_month = st.sidebar.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

st.sidebar.divider()

with st.sidebar.expander("➕ Register New Member"):
    new_name = st.text_input("Full Name")
    new_phone = st.text_input("Phone Number")
    new_gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    if st.button("Save to Database", use_container_width=True):
        if target_year not in data: 
            data[target_year] = {}
        if new_name:
            data[target_year][new_name] = {"phone": new_phone, "gender": new_gender, "payments": []}
            save_data(data)
            st.success(f"Added {new_name}!")
            st.rerun()

# --- MAIN INTERFACE ---
st.title(f"📊 {target_month} {target_year} Ledger")

if target_year in data and data[target_year]:
    # --- SEARCH BAR ---
    search_query = st.text_input("🔍 Search by Name, Phone, or Gender", placeholder="Type here to filter...")
    
    members = data[target_year]
    
    # Filtered List Logic
    filtered_members = {
        name: info for name, info in members.items() 
        if search_query.lower() in name.lower() 
        or search_query.lower() in info.get('phone', '').lower()
        or search_query.lower() in info.get('gender', '').lower()
    }

    # Stats Row
    m_count = len([n for n, i in filtered_members.items() if i.get('gender') == "Male"])
    f_count = len([n for n, i in filtered_members.items() if i.get('gender') == "Female"])
    st.info(f"Showing {len(filtered_members)} results: 👨 {m_count} Males | 👩 {f_count} Females")

    st.divider()

    # Table Header
    h1, h2, h3, h4 = st.columns([2, 1.5, 1.5, 1])
    h1.subheader("Member Info")
    h2.subheader("Payment")
    h3.subheader("Edit Details")
    h4.subheader("Remove")

    for name, info in filtered_members.items():
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1])
            
            # 1. Member Info Display
            icon = "👨" if info.get('gender') == "Male" else "👩"
            total_paid = sum(p['amount'] for p in info['payments'] if p['month'] == target_month)
            col1.markdown(f"**{icon} {name}** \n📞 {info['phone']}")
            
            # 2. Payment Section
            with col2:
                amt = st.number_input(f"Amt (GHS)", min_value=0.0, step=1.0, key=f"pay_in_{name}")
                if st.button(f"Pay for {name}", key=f"btn_pay_{name}"):
                    if amt > 0:
                        info['payments'].append({
                            "amount": amt, 
                            "month": target_month, 
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                        save_data(data)
                        st.toast(f"Success: {name} paid GHS {amt}")
                        st.rerun()
                st.caption(f"Total this month: **GHS {total_paid:.2f}**")

            # 3. Update/Edit Section
            with col3:
                with st.popover("⚙️ Edit Member"):
                    edit_phone = st.text_input("New Phone", value=info['phone'], key=f"ed_ph_{name}")
                    edit_gen = st.selectbox("New Gender", ["Male", "Female"], index=0 if info['gender']=="Male" else 1, key=f"ed_gn_{name}")
                    if st.button("Save Changes", key=f"sav_ed_{name}"):
                        info['phone'] = edit_phone
                        info['gender'] = edit_gen
                        save_data(data)
                        st.rerun()

            # 4. Delete Section
            with col4:
                if st.button("🗑️ Delete", key=f"del_{name}", help="Remove member from system"):
                    del data[target_year][name]
                    save_data(data)
                    st.rerun()
            
            st.divider()
else:
    st.warning(f"No records found for {target_year}. Start by adding a member in the sidebar!")
