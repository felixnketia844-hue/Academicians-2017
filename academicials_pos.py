# -*- coding: utf-8 -*-
""
#Created on Mon Mar 16 18:31:12 2026
#@author: felix
# Student Monthly Dues System
import streamlit as st
import json
import os
from datetime import datetime

# --- DATABASE LOGIC ---
def load_data():
    if not os.path.exists('members_data.json'):
        # Pre-loading years 2017 through 2030
        years_list = [str(y) for y in range(2017, 2031)]
        with open('members_data.json', 'w') as f: 
            json.dump({"years": years_list, "data": {}}, f)
    with open('members_data.json', 'r') as f: return json.load(f)

def save_data(data):
    with open('members_data.json', 'w') as f: json.dump(data, f, indent=4)

# --- LOGIN SYSTEM ---
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔒 Academicians 2017 Portal")
        pin = st.text_input("Enter Access PIN", type="password")
        if st.button("Login"):
            if pin == "2017":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Incorrect PIN")
        return False
    return True

st.set_page_config(page_title="Academicians 2017", layout="wide")

if check_password():
    # --- BLUE MARQUEE ---
    st.markdown('<div style="background-color:#1E3A8A;color:white;padding:15px;text-align:center;border-radius:10px;font-weight:bold;">✨ WELCOME TO ACADEMICIANS 2017 OFFICIAL LEDGER ✨</div>', unsafe_allow_html=True)

    db = load_data()

    # --- SIDEBAR ---
    st.sidebar.header("⚙️ Management")
    if st.sidebar.button("Log Out"):
        del st.session_state["password_correct"]
        st.rerun()

    target_year = st.sidebar.selectbox("Select Year", db["years"])
    target_month = st.sidebar.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

    with st.sidebar.expander("➕ Register New Member"):
        n_name = st.text_input("Full Name")
        n_phone = st.text_input("Phone Number")
        n_gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
        if st.button("Save Member"):
            if target_year not in db["data"]: db["data"][target_year] = {}
            if n_name:
                db["data"][target_year][n_name] = {"phone": n_phone, "gender": n_gender, "payments": []}
                save_data(db)
                st.success(f"Added {n_name}!")
                st.rerun()

    # --- MAIN LEDGER ---
    st.title(f"📊 {target_month} {target_year} Records")
    
    if target_year in db["data"] and db["data"][target_year]:
        search = st.text_input("🔍 Search Name or Gender (Male/Female)")
        members = db["data"][target_year]
        
        # Columns
        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        c1.write("**Member Detail**")
        c2.write("**Total Paid**")
        c3.write("**Action**")
        c4.write("**Manage**")
        st.divider()

        for name in list(members.keys()):
            info = members[name]
            icon = "👨" if info.get('gender') == "Male" else "👩"
            
            if search.lower() in name.lower() or search.lower() in info.get('gender', '').lower():
                paid = sum(p['amount'] for p in info['payments'])
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                col1.write(f"{icon} **{name}**\n({info['phone']})")
                col2.write(f"GHS {paid:.2f}")
                
                if col3.button("💳 Pay 50", key=f"pay_{name}"):
                    info['payments'].append({"amount": 50, "month": target_month, "date": str(datetime.now())})
                    save_data(db)
                    st.balloons()
                    st.rerun()

                with col4.popover("⚙️ Edit"):
                    u_phone = st.text_input("Update Phone", value=info['phone'], key=f"u_p_{name}")
                    u_gen = st.radio("Update Gender", ["Male", "Female"], index=0 if info.get('gender')=="Male" else 1, key=f"u_g_{name}")
                    if st.button("Save Changes", key=f"u_b_{name}"):
                        info['phone'] = u_phone
                        info['gender'] = u_gen
                        save_data(db)
                        st.rerun()
                    if st.button("🗑️ Delete Member", key=f"d_b_{name}"):
                        del db["data"][target_year][name]
                        save_data(db)
                        st.rerun()
    else:
        st.info(f"No members registered for {target_year} yet.")

    # WhatsApp Report
    st.divider()
    if st.button("📱 Generate WhatsApp Report"):
        report = f"*ACADEMICIANS 2017 - {target_month} {target_year}*\n"
        current_data = db["data"].get(target_year, {})
        for n, i in current_data.items():
            p = sum(pm['amount'] for pm in i['payments'])
            report += f"• {n}: GHS {p}\n"
        st.text_area("Copy and paste to WhatsApp:", value=report)
