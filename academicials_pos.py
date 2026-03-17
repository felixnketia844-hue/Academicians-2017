# -*- coding: utf-8 -*-
""
#Created on Mon Mar 16 18:31:12 2026
#@author: felix
# Student Monthly Dues System
import streamlit as st
import json
import os
from datetime import datetime

# --- DATABASE ---
def load_data():
    if not os.path.exists('members_data.json'):
        with open('members_data.json', 'w') as f: 
            json.dump({"years": ["2024", "2025", "2026", "2027"], "data": {}}, f)
    with open('members_data.json', 'r') as f: return json.load(f)

def save_data(data):
    with open('members_data.json', 'w') as f: json.dump(data, f, indent=4)

# --- CONFIG & DESIGN ---
st.set_page_config(page_title="Academicians 2017", layout="wide")

# This is the "Safe" Marquee and Button styling
st.markdown("""<style>
.marquee { background-color: #1E3A8A; color: white; padding: 15px; text-align: center; border-radius: 10px; font-weight: bold; }
div.stButton > button:first-child { background-color: #F59E0B; color: white; border-radius: 20px; font-weight: bold; }
</style>
<div class="marquee">✨ WELCOME TO THE OFFICIAL ACADEMICIANS 2017 LEDGER PORTAL ✨</div>""", unsafe_allow_html=True)

db = load_data()

# --- SIDEBAR ---
st.sidebar.header("📅 Settings & Entry")

# 1. Year Manager
new_year = st.sidebar.text_input("Add New Year")
if st.sidebar.button("Add Year"):
    if new_year and new_year not in db["years"]:
        db["years"].append(new_year)
        db["years"].sort()
        save_data(db)
        st.rerun()

target_year = st.sidebar.selectbox("Select Active Year", db["years"])
target_month = st.sidebar.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

# 2. Add Member with Gender
with st.sidebar.expander("➕ Register New Member"):
    n_name = st.text_input("Name")
    n_phone = st.text_input("Phone")
    n_gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    if st.button("Save Member"):
        if target_year not in db["data"]: db["data"][target_year] = {}
        if n_name:
            db["data"][target_year][n_name] = {"phone": n_phone, "gender": n_gender, "payments": []}
            save_data(db)
            st.success(f"{n_name} added!")
            st.rerun()

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

# --- MAIN PAGE ---
st.title(f"📊 Ledger: {target_month} {target_year}")

if target_year in db["data"] and db["data"][target_year]:
    search = st.text_input("🔍 Search Name or Gender")
    members = db["data"][target_year]
    
    # Table Header
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    c1.markdown("**Member & Gender**")
    c2.markdown("**Total Paid**")
    c3.markdown("**Pay 50**")
    c4.markdown("**Update/Delete**")
    st.divider()

    for name in list(members.keys()):
        info = members[name]
        icon = "👨" if info.get('gender') == "Male" else "👩"
        
        if search.lower() in name.lower() or search.lower() in info.get('gender', '').lower():
            paid = sum(p['amount'] for p in info['payments'])
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            col1.write(f"{icon} **{name}**\n({info['phone']})")
            col2.write(f"GHS {paid:.2f}")
            
            if col3.button("💳 Pay", key=f"p_{name}"):
                info['payments'].append({"amount": 50, "month": target_month, "date": str(datetime.now())})
                save_data(db)
                st.balloons()
                st.rerun()

            # UPDATE & DELETE POP-OVER
            with col4.popover("⚙️ Manage"):
                st.write("### Edit Details")
                u_phone = st.text_input("New Phone", value=info['phone'], key=f"up_{name}")
                u_gen = st.radio("New Gender", ["Male", "Female"], index=0 if info.get('gender')=="Male" else 1, key=f"ug_{name}")
                
                if st.button("Update Info", key=f"btn_u_{name}"):
                    info['phone'] = u_phone
                    info['gender'] = u_gen
                    save_data(db)
                    st.success("Updated!")
                    st.rerun()
                
                st.divider()
                if st.button("🗑️ Delete Member", key=f"btn_d_{name}"):
                    del db["data"][target_year][name]
                    save_data(db)
                    st.rerun()
else:
    st.info("No members found. Use the sidebar to add your first member!")

# WhatsApp Report
if st.button("📱 Generate WhatsApp Report"):
    report = f"*ACADEMICIANS 2017 - {target_month} {target_year}*\n"
    for n, i in db["data"].get(target_year, {}).items():
        p = sum(pm['amount'] for pm in i['payments'])
        report += f"• {n}: GHS {p}\n"
    st.text_area("Copy this:", value=report)
