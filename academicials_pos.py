# -*- coding: utf-8 -*-
""
#Created on Mon Mar 16 18:31:12 2026
#@author: felix
# Student Monthly Dues System
import streamlit as st
import json
import os
from datetime import datetime

# --- 1. DATA STORAGE ---
def load_data():
    if not os.path.exists('members_data.json'):
        with open('members_data.json', 'w') as f: json.dump({}, f)
    with open('members_data.json', 'r') as f: 
        try:
            return json.load(f)
        except:
            return {}

def save_data(data):
    with open('members_data.json', 'w') as f: 
        json.dump(data, f, indent=4)

# --- 2. SETUP ---
st.set_page_config(page_title="Academicians 2017", layout="wide")
data = load_data()

# --- 3. SIDEBAR (ONLY FOR ADDING) ---
st.sidebar.header("⚙️ Settings")
target_year = st.sidebar.selectbox("Select Year", [str(y) for y in range(2024, 2031)])
target_month = st.sidebar.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

with st.sidebar.expander("➕ ADD NEW MEMBER HERE"):
    new_name = st.text_input("Full Name")
    new_phone = st.text_input("Phone Number")
    new_gender = st.selectbox("Gender", ["Male", "Female"])
    if st.button("Save New Member"):
        if target_year not in data: data[target_year] = {}
        if new_name:
            data[target_year][new_name] = {"phone": new_phone, "gender": new_gender, "payments": []}
            save_data(data)
            st.rerun()

# --- 4. MAIN SCREEN (WHERE THE BUTTONS ARE) ---
st.markdown(f"## 📊 {target_month} {target_year} Ledger")

# SEARCH BAR
search = st.text_input("🔍 SEARCH: Type name or gender here to find someone", placeholder="Type here...")

st.divider()

if target_year in data and data[target_year]:
    members = data[target_year]
    
    # Header Row
    h1, h2, h3, h4 = st.columns([2, 2, 2, 1])
    h1.write("**MEMBER INFO**")
    h2.write("**PAYMENT (GHS)**")
    h3.write("**UPDATE PHONE**")
    h4.write("**DELETE**")
    st.divider()

    for name in list(members.keys()):
        info = members[name]
        
        # Search Filter Logic
        if search.lower() in name.lower() or search.lower() in info.get('gender','').lower():
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            
            # INFO
            with col1:
                st.write(f"**{name}**")
                st.caption(f"{info.get('gender')} | {info.get('phone')}")
            
            # PAYMENT (AMOUNT)
            with col2:
                amt = st.number_input(f"Enter Amt", min_value=0.0, key=f"amt_{name}")
                if st.button(f"Confirm Payment", key=f"btn_{name}"):
                    if amt > 0:
                        info['payments'].append({"amount": amt, "month": target_month, "date": str(datetime.now())})
                        save_data(data)
                        st.success(f"Paid {amt}")
                        st.rerun()
                
                # Show total for this specific month
                this_month_total = sum(p['amount'] for p in info['payments'] if p['month'] == target_month)
                st.write(f"Paid this month: **GHS {this_month_total}**")

            # UPDATE
            with col3:
                up_phone = st.text_input("New Phone", value=info['phone'], key=f"up_{name}")
                if st.button("Save Update", key=f"sav_{name}"):
                    info['phone'] = up_phone
                    save_data(data)
                    st.toast("Updated!")
                    st.rerun()

            # DELETE
            with col4:
                if st.button("🗑️ DELETE", key=f"del_{name}"):
                    del data[target_year][name]
                    save_data(data)
                    st.rerun()
            
            st.divider()
else:
    st.warning(f"No members found for the year {target_year}. Add a member in the sidebar first!")
