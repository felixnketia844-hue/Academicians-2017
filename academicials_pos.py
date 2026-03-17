# -*- coding: utf-8 -*-
Created on Mon Mar 16 18:31:12 2026

@author: felix
""
import streamlit as st
import json
import os
from datetime import datetime

# 1. Setup the Database
def load_data():
    if not os.path.exists('members_yearly.json'):
        with open('members_yearly.json', 'w') as f:
            json.dump({}, f)
    with open('members_yearly.json', 'r') as f:
        return json.load(f)

def save_data(data):
    with open('members_yearly.json', 'w') as f:
        json.dump(data, f, indent=4)

# 2. Page Configuration
st.set_page_config(page_title="Academicians 2017")
st.title("🎓 ACADEMICIANS 2017")
st.write("Official Financial Ledger Portal")

data = load_data()

# 3. Sidebar for Adding Members
st.sidebar.header("Register New Member")
new_name = st.sidebar.text_input("Name")
new_phone = st.sidebar.text_input("Phone Number")
if st.sidebar.button("Add Member"):
    current_year = str(datetime.now().year)
    if current_year not in data:
        data[current_year] = {}
    if new_name:
        data[current_year][new_name] = {"phone": new_phone, "payments": []}
        save_data(data)
        st.sidebar.success(f"{new_name} added successfully!")
        st.rerun()

# 4. Main Ledger Table
years = list(data.keys())
if years:
    selected_year = st.selectbox("Select Year", years)
    members = data[selected_year]
    
    st.subheader(f"Records for {selected_year}")
    for name, info in members.items():
        paid = sum([p['amount'] for p in info.get('payments', [])])
        col1, col2, col3 = st.columns([2, 1, 1])
        col1.write(f"**{name}**")
        col2.write(f"GHS {paid:.2f}")
        if col3.button(f"Pay 50", key=name):
            info['payments'].append({"amount": 50, "date": str(datetime.now())})
            save_data(data)
            st.balloons()
            st.rerun()

    # 5. WhatsApp Section
    st.divider()
    if st.button("Generate WhatsApp Report"):
        report = f"*ACADEMICIANS 2017 REPORT ({selected_year})*\n"
        for n, i in members.items():
            total = sum([p['amount'] for p in i.get('payments', [])])
            report += f"• {n}: GHS {total}\n"
        st.text_area("Copy/Paste to WhatsApp:", value=report)
else:
    st.info("No members found. Use the sidebar to add your first member!")
