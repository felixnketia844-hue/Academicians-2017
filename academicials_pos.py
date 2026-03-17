# -*- coding: utf-8 -*-
""
#Created on Mon Mar 16 18:31:12 2026
#@author: felix
Iimport streamlit as st
import json
import os
from datetime import datetime

# --- DATABASE ---
def load_data():
    if not os.path.exists('members_data.json'):
        with open('members_data.json', 'w') as f: json.dump({"years": ["2024", "2025", "2026", "2027"], "data": {}}, f)
    with open('members_data.json', 'r') as f: return json.load(f)

def save_data(data):
    with open('members_data.json', 'w') as f: json.dump(data, f, indent=4)

# --- CONFIG ---
st.set_page_config(page_title="Academicians 2017", layout="wide")
st.markdown('<div style="background-color:#1E3A8A;color:white;padding:15px;text-align:center;border-radius:10px;font-weight:bold;">✨ ACADEMICIANS 2017 OFFICIAL LEDGER ✨</div>', unsafe_allow_html=True)

db = load_data()

# --- SIDEBAR ---
st.sidebar.header("🚪 Session")
if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

st.sidebar.divider()

# 1. YEAR MANAGER
st.sidebar.header("📅 Year Manager")
new_year_input = st.sidebar.text_input("Add New Year (e.g. 2028)")
if st.sidebar.button("Add Year"):
    if new_year_input and new_year_input not in db["years"]:
        db["years"].append(new_year_input)
        db["years"].sort()
        save_data(db)
        st.sidebar.success(f"Year {new_year_input} added!")
        st.rerun()

# 2. SELECTION
target_year = st.sidebar.selectbox("Select Active Year", db["years"])
target_month = st.sidebar.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

# 3. ADD MEMBER
with st.sidebar.expander("➕ Register New Member"):
    n_name = st.text_input("Full Name")
    n_phone = st.text_input("Phone")
    n_gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    if st.button("Save to System"):
        if target_year not in db["data"]: db["data"][target_year] = {}
        if n_name:
            db["data"][target_year][n_name] = {"phone": n_phone, "gender": n_gender, "payments": []}
            save_data(db)
            st.rerun()

# --- MAIN INTERFACE ---
st.title(f"📊 {target_month} {target_year} Records")

if target_year in db["data"] and db["data"][target_year]:
    search = st.text_input("🔍 Search Name or Gender")
    members = db["data"][target_year]
    
    # TABLE HEADER
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    c1.write("**Member Detail**")
    c2.write("**Total Paid**")
    c3.write("**Quick Pay**")
    c4.write("**Manage/Update**")
    st.divider()

    for name in list(members.keys()):
        info = members[name]
        if search.lower() in name.lower() or search.lower() in info.get('gender', '').lower():
            paid = sum(p['amount'] for p in info['payments'])
            
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            icon = "👨" if info.get('gender') == "Male" else "👩"
            col1.write(f"{icon} **{name}**\n({info['phone']})")
            col2.write(f"GHS {paid:.2f}")
            
            # QUICK PAY
            if col3.button("Pay 50", key=f"p_{name}"):
                info['payments'].append({"amount": 50, "month": target_month, "date": str(datetime.now())})
                save_data(db)
                st.balloons()
                st.rerun()

            # UPDATE & DELETE
            with col4.popover("Edit/Delete"):
                st.write("📝 Update Info")
                u_phone = st.text_input("New Phone", value=info['phone'], key=f"up_{name}")
                u_gen = st.selectbox("New Gender", ["Male", "Female"], index=0 if info.get('gender')=="Male" else 1, key=f"ug_{name}")
                
                if st.button("Save Changes", key=f"sv_{name}"):
                    info['phone'] = u_phone
                    info['gender'] = u_gen
                    save_data(db)
                    st.rerun()
                
                st.divider()
                if st.button("🗑️ Delete Member", key=f"del_{name}"):
                    del db["data"][target_year][name]
                    save_data(db)
                    st.rerun()
else:
    st.warning("No data found for this year. Add members in the sidebar!")
