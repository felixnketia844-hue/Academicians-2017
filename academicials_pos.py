# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 18:31:12 2026

@author: felix
""
import streamlit as st
import json
import os
from datetime import datetime

# --- DATABASE SETUP ---
def load_data():
    if not os.path.exists('members_yearly.json'):
        with open('members_yearly.json', 'w') as f:
            json.dump({}, f)
    with open('members_yearly.json', 'r') as f:
        return json.load(f)

def save_data(data):
    with open('members_yearly.json', 'w') as f:
        json.dump(data, f, indent=4)

# --- THEME & STYLING ---
st.set_page_config(page_title="Academicians 2017", layout="wide")

st.markdown("""
<style>
.marquee{
background-color:#1E3A8A;
color: white;
padding:15px;
font-weight:bold;
border-radius:10px;
text-align:center;
font-size:20px;
}
.stButton>button{
background-color: #F59E0B;
color: white;
border-radius:10px;
font-weight:bold;
width:100%;
}
</style>
<div class="marquee">
✨ WELCOME TO ACADEMICIANS 2017 OFFICIAL LEDGER PORTAL ✨
</div>
""", unsafe_allow_html=True)

st.title("🎓 Member Ledger")

data = load_data()

# --- SIDEBAR: ADD MEMBER ---
st.sidebar.header("👤 Register Member")
new_name = st.sidebar.text_input("Name")
new_phone = st.sidebar.text_input("Phone")
if st.sidebar.button("Add to System"):
    current_year = str(datetime.now().year)
    if current_year not in data:
        data[current_year] = {}
    if new_name:
        data[current_year][new_name] = {"phone": new_phone, "payments": []}
        save_data(data)
        st.sidebar.success("Member Added!")
        st.rerun()

# --- MAIN PAGE ---
years = list(data.keys())
if years:
    selected_year = st.selectbox("Select Year", years)
    members = data[selected_year]
    
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

    if st.button("📱 Generate WhatsApp Report"):
        report = f"*ACADEMICIANS 2017 ({selected_year})*\n"
        for n, i in members.items():
            p = sum([pm['amount'] for pm in i.get('payments', [])])
            report += f"• {n}: GHS {p}\n"
        st.text_area("Copy this:", value=report)
else:
    st.info("Start by adding a member in the sidebar!")
