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
    with open('members_data.json', 'r') as f: return json.load(f)

def save_data(data):
    with open('members_data.json', 'w') as f: json.dump(data, f, indent=4)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Academicians 2017", layout="wide")

# Safe Styling (No Indent Errors)
st.markdown('<div style="background-color:#1E3A8A;color:white;padding:15px;text-align:center;border-radius:10px;font-weight:bold;">✨ ACADEMICIANS 2017 OFFICIAL LEDGER ✨</div>', unsafe_allow_html=True)

data = load_data()

# --- SIDEBAR: INSERT DATA ---
st.sidebar.header("📥 Data Entry")
target_year = st.sidebar.selectbox("Select Year", [str(y) for y in range(2024, 2030)])
target_month = st.sidebar.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

with st.sidebar.expander("➕ Add New Member"):
    new_name = st.text_input("Full Name")
    new_phone = st.text_input("Phone")
    if st.button("Save Member"):
        if target_year not in data: data[target_year] = {}
        if new_name:
            data[target_year][new_name] = {"phone": new_phone, "payments": []}
            save_data(data)
            st.success("Added!")
            st.rerun()

# --- MAIN INTERFACE ---
st.title(f"📊 Ledger: {target_month} {target_year}")

if target_year in data and data[target_year]:
    # Search and Stats
    search = st.text_input("🔍 Search Member Name")
    members = data[target_year]
    
    # Review Summary
    total_collected = sum(sum(p['amount'] for p in info['payments']) for info in members.values())
    st.info(f"💰 **Total Review for {target_year}:** GHS {total_collected:.2f}")

    # Header
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    col1.write("**Member Name**")
    col2.write("**Total Paid**")
    col3.write("**Pay GHS 50**")
    col4.write("**Manage**")
    st.divider()

    for name in list(members.keys()):
        if search.lower() in name.lower():
            info = members[name]
            paid = sum(p['amount'] for p in info['payments'])
            
            c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
            c1.write(f"{name} \n ({info['phone']})")
            c2.write(f"GHS {paid:.2f}")
            
            # Update/Pay
            if c3.button("💳 Pay", key=f"pay_{name}"):
                info['payments'].append({"amount": 50, "month": target_month, "date": str(datetime.now())})
                save_data(data)
                st.balloons()
                st.rerun()

            # Edit/Delete Preview
            with c4.popover("⚙️"):
                new_p = st.text_input("Edit Phone", value=info['phone'], key=f"edit_{name}")
                if st.button("Update", key=f"up_{name}"):
                    info['phone'] = new_p
                    save_data(data)
                    st.rerun()
                if st.button("🗑️ Delete", key=f"del_{name}"):
                    del data[target_year][name]
                    save_data(data)
                    st.rerun()
else:
    st.warning(f"No records found for {target_year}. Please add a member in the sidebar.")

# --- WHATSAPP REPORT ---
if st.button("📱 Review & Copy WhatsApp Report"):
    report = f"*ACADEMICIANS 2017 - {target_month} {target_year}*\n"
    for n, i in data.get(target_year, {}).items():
        p = sum(pm['amount'] for pm in i['payments'])
        report += f"• {n}: GHS {p}\n"
    st.text_area("Report Preview:", value=report)
