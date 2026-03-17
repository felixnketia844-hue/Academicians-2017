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
            json.dump({"years": ["2017", "2024", "2025", "2026"], "data": {}}, f)
    with open('members_data.json', 'r') as f: return json.load(f)

def save_data(data):
    with open('members_data.json', 'w') as f: json.dump(data, f, indent=4)

# --- SECURITY ---
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔒 Academicians 2017 Portal")
        pin = st.text_input("Enter Access PIN", type="password")
        if st.button("Login"):
            if pin == "2017": # YOU CAN CHANGE THIS PIN
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Incorrect PIN")
        return False
    return True

st.set_page_config(page_title="Academicians 2017", layout="wide")

if check_password():
    # --- STYLING ---
    st.markdown("""<style>
    .marquee { background-color: #1E3A8A; color: white; padding: 15px; text-align: center; border-radius: 10px; font-weight: bold; }
    div.stButton > button:first-child { background-color: #F59E0B; color: white; border-radius: 20px; font-weight: bold; }
    </style>
    <div class="marquee">✨ WELCOME TO THE OFFICIAL ACADEMICIANS 2017 LEDGER PORTAL ✨</div>""", unsafe_allow_html=True)

    db = load_data()

    # --- SIDEBAR ---
    st.sidebar.header("⚙️ Management")
    if st.sidebar.button("Log Out"):
        del st.session_state["password_correct"]
        st.rerun()

    target_year = st.sidebar.selectbox("Select Year", db["years"])
    target_month = st.sidebar.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

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
        c4.markdown("**Manage**")
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

                with col4.popover("⚙️ Edit"):
                    u_phone = st.text_input("New Phone", value=info['phone'], key=f"up_{name}")
                    u_gen = st.radio("New Gender", ["Male", "Female"], index=0 if info.get('gender')=="Male" else 1, key=f"ug_{name}")
                    if st.button("Update Info", key=f"btn_u_{name}"):
                        info['phone'] = u_phone
                        info['gender'] = u_gen
                        save_data(db)
                        st.rerun()
                    if st.button("🗑️ Delete", key=f"btn_d_{name}"):
                        del db["data"][target_year][name]
                        save_data(db)
                        st.rerun()
    else:
        st.info("No members found. Use the sidebar to add someone!")

    # WhatsApp Report
    if st.button("📱 Generate WhatsApp Report"):
        report = f"*ACADEMICIANS 2017 - {target_month} {target_year}*\n"
        for n, i in db["data"].get(target_year, {}).items():
            p = sum(pm['amount'] for pm in i['payments'])
            report += f"• {n}: GHS {p}\n"
        st.text_area("Copy this:", value=report)
