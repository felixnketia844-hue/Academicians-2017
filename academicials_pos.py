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
        with open('members_data.json', 'w') as f: json.dump({}, f)
    with open('members_data.json', 'r') as f: 
        try:
            return json.load(f)
        except:
            return {}

def save_data(data):
    with open('members_data.json', 'w') as f: json.dump(data, f, indent=4)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Academicians 2017", layout="wide")
st.markdown('<h1 style="text-align:center; color:#1E3A8A;">✨ ACADEMICIANS 2017 LEDGER ✨</h1>', unsafe_allow_html=True)

data = load_data()

# --- SIDEBAR ---
st.sidebar.header("Settings")
target_year = st.sidebar.selectbox("Year", [str(y) for y in range(2024, 2031)])
target_month = st.sidebar.selectbox("Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

with st.sidebar.expander("➕ Add New Member"):
    new_name = st.text_input("Full Name")
    new_phone = st.text_input("Phone")
    new_gender = st.selectbox("Gender", ["Male", "Female"])
    if st.button("Save New Member"):
        if target_year not in data: data[target_year] = {}
        if new_name:
            data[target_year][new_name] = {"phone": new_phone, "gender": new_gender, "payments": []}
            save_data(data)
            st.rerun()

# --- MAIN INTERFACE ---
if target_year in data and data[target_year]:
    # 1. THE SEARCH BAR
    search = st.text_input("🔍 Search by Name or Gender", placeholder="Type name here...")
    
    st.divider()
    
    # 2. THE LIST
    members = data[target_year]
    for name in list(members.keys()):
        info = members[name]
        
        # Search Filter Logic
        if search.lower() in name.lower() or search.lower() in info.get('gender','').lower():
            
            # Create 4 columns for: Info, Payment, Update, Delete
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            
            # COLUMN 1: Basic Info
            with col1:
                st.markdown(f"**{name}**")
                st.caption(f"{info.get('gender')} | {info.get('phone')}")
            
            # COLUMN 2: Amount Paid & Payment Input
            with col2:
                total_paid = sum(p['amount'] for p in info['payments'] if p['month'] == target_month)
                amt = st.number_input(f"GHS Amount", min_value=0.0, key=f"pay_{name}")
                if st.button(f"Confirm Payment", key=f"btn_{name}"):
                    if amt > 0:
                        info['payments'].append({"amount": amt, "month": target_month, "date": str(datetime.now())})
                        save_data(data)
                        st.success(f"Paid {amt}")
                        st.rerun()
                st.write(f"Total Paid: **GHS {total_paid}**")

            # COLUMN 3: Update Details
            with col3:
                new_p = st.text_input("Edit Phone", value=info['phone'], key=f"p_{name}")
                if st.button("Update Info", key=f"upd_{name}"):
                    info['phone'] = new_p
                    save_data(data)
                    st.toast("Updated!")
                    st.rerun()

            # COLUMN 4: Delete
            with col4:
                st.write("") # spacing
                if st.button("🗑️ Delete", key=f"del_{name}"):
                    del data[target_year][name]
                    save_data(data)
                    st.rerun()
            
            st.divider()
else:
    st.info("No members found for this year. Use the sidebar to add someone.")
