# -*- coding: utf-8 -*-
""
#Created on Mon Mar 16 18:31:12 2026
#@author: felix
""
import streamlit as st
import json
import os
from datetime import datetime

# --- DATABASE ---
def load_data():
    if not os.path.exists('members_yearly.json'):
        with open('members_yearly.json', 'w') as f:
            json.dump({}, f)
    with open('members_yearly.json', 'r') as f:
        return json.load(f)

def save_data(data):
    with open('members_yearly.json', 'w') as f:
        json.dump(data, f, indent=4)

# --- THEME & MARQUEE ---
st.set_page_config(page_title="Academicians 2017", layout="wide")

# This adds the Blue Marquee and Gold Buttons safely
st.markdown("""<style>
.stApp { background-color: #f0f2f6; }
.marquee-text {
    background-color: #1E3A8A;
    color: white;
    padding: 15px;
    font-weight: bold;
    text-align: center;
    border-radius: 10px;
    border: 2px solid #F59E0B;
}
div.stButton > button:first-child {
    background-color: #F59E0B;
    color: white;
    font-weight: bold;
    border-radius: 20px;
}
</style>
<div class="marquee-text">
✨ WELCOME TO THE OFFICIAL ACADEMICIANS 2017 LEDGER PORTAL ✨
</div>""", unsafe_allow_html=True)

st.title("🎓 Financial Records")

data = load_data()

# --- SIDEBAR ---
st.sidebar.markdown("### 👤 Member Registration")
new_name = st.sidebar.text_input("Full Name")
new_phone = st.sidebar.text_input("WhatsApp Number")

if st.sidebar.button("Add Member to System"):
    current_year = str(datetime.now().year)
    if current_year not in data:
        data[current_year] = {}
    if new_name:
        data[current_year][new_name] = {"phone": new_phone, "payments": []}
        save_data(data)
        st.sidebar.success(f"Successfully added {new_name}!")
        st.rerun()

# --- MAIN TABLE ---
years = list(data.keys())
if years:
    selected_year = st.selectbox("📅 Filter by Year", years)
    members = data[selected_year]
    
    # Header Row
    c1, c2, c3 = st.columns([2, 1, 1])
    c1.markdown("### Name")
    c2.markdown("### Amount (GHS)")
    c3.markdown("### Action")
    st.divider()

    for name, info in members.items():
        total_paid = sum([p['amount'] for p in info.get('payments', [])])
        col1, col2, col3 = st.columns([2, 1, 1])
        
        col1.write(f"**{name}**")
        col2.write(f"GHS {total_paid:.2f}")
        
        if col3.button(f"Pay 50.00", key=name):
            info['payments'].append({"amount": 50, "date": str(datetime.now())})
            save_data(data)
            st.balloons()
            st.rerun()
else:
    st.info("The ledger is currently empty. Use the sidebar on the left to add members!")
