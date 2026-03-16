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

# This is your "Marquee" and Custom Colors
st.markdown("""
    <style>
    .marquee {
        background-color: #1E3A8A;
        color: white;
        padding: 10px;
        font-weight: bold;
        border-radius: 5px;
        text-align: center;
    }
    .stButton>button {
        background-color: #F59E0B;
        color: white;
        border-radius: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #D97706;
        color: white;
    }
    </style>
    <div class="marquee">
        ✨ WELCOME TO ACADEMICIANS 2017 OFFICIAL LEDGER PORTAL ✨
    </div>
    """, unsafe_allow_html=True)

st.title("🎓 ACADEMICIANS 2017")
st.write("---")

data = load_data()

# --- SIDEBAR: ADD MEMBER ---
st.sidebar.markdown("### 👤 Add New Member")
new_name = st.sidebar.text_input("Full Name")
new_phone = st.sidebar.text_input("Phone Number")
if st.sidebar.button("➕ Add Member"):
    current_year = str(datetime.now().year)
    if current_year not in data:
        data[current_year] = {}
    
    if new_name and new_name not in data[current_year]:
        data[current_year][new_name] = {"phone": new_phone, "payments": []}
        save_data(data)
        st.sidebar.success(f"✅ {new_name} added!")
        st.rerun()

# --- MAIN PAGE: VIEW & PAY ---
years = list(data.keys())
if years:
    selected_year = st.selectbox("📅 Select Financial Year", years)
    
    st.subheader(f"Records for {selected_year}")
    members = data[selected_year]
    
    for name, info in members.items():
        total_paid = sum([p['amount'] for p in info.get('payments', [])])
        
        # Creating a nice "Card" look for each person
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            col1.markdown(f"**{name}** \n📞 {info['phone']}")
            col2.markdown(f"💰 Total Paid: **GHS {total_paid:.2f}**")
            
            if col3.button(f"Pay GHS 50", key=name):
                info['payments'].append({"amount": 50, "date": str(datetime.now())})
                save_data(data)
                st.balloons()
                st.success(f"Payment recorded for {name}!")
                st.rerun()
            st.write("---")

    # --- WHATSAPP REPORT ---
    if st.button("📱 Generate WhatsApp Report"):
        report = f"*ACADEMICIANS 2017 FINANCIAL REPORT ({selected_year})*\n"
        report += "----------------------------------\n"
        for name, info in members.items():
            paid = sum([p['amount'] for p in info.get('payments', [])])
            report += f"• {name}: GHS {paid:.2f}\n"
        
        st.text_area("Copy and Paste to WhatsApp:", value=report, height=200)
else:
    st.info("No records found. Add your first member in the sidebar!")
