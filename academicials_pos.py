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
        with open('members_data.json', 'w') as f:
            json.dump({}, f)
    with open('members_data.json', 'r') as f:
        return json.load(f)

def save_data(data):
    with open('members_data.json', 'w') as f:
        json.dump(data, f, indent=4)

# --- LOGIN/LOGOUT LOGIC ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = True  # Set to False if you want a password screen later

def logout():
    st.session_state.logged_in = False
    st.rerun()

# --- PAGE CONFIG ---
st.set_page_config(page_title="Academicians 2017", layout="wide")

# --- MARQUEE HEADER + SCROLLING TICKER ---
st.markdown("""
<style>
@keyframes scroll-left {
  0% { transform: translateX(100%); }
  100% { transform: translateX(-100%); }
}
.marquee {
  overflow: hidden;
  white-space: nowrap;
  box-sizing: border-box;
  background-color:#1E3A8A;
  border-radius:10px;
  padding: 15px;
  color:white;
  font-weight:bold;
  font-size:22px;
}
.marquee span {
  display: inline-block;
  padding-left: 100%;
  animation: scroll-left 15s linear infinite;
}
.submarquee {
  overflow: hidden;
  white-space: nowrap;
  box-sizing: border-box;
  font-size:16px;
  color:#f0f0f0;
  margin-top:5px;
}
.submarquee span {
  display:inline-block;
  padding-left:100%;
  animation: scroll-left 20s linear infinite;
}
</style>

<div class="marquee"><span>✨ ACADEMICIANS 2017 OFFICIAL LEDGER ✨</span></div>
<div class="submarquee"><span>Manage members | Track payments | Update or Delete | Safe & secure ledger</span></div>
""", unsafe_allow_html=True)

# --- LOGIN CHECK ---
if not st.session_state.logged_in:
    st.info("You have logged out.")
    if st.button("Log Back In"):
        st.session_state.logged_in = True
        st.rerun()
    st.stop()

data = load_data()

# --- SIDEBAR ---
st.sidebar.header("🚪 Session")
if st.sidebar.button("Logout of System"):
    logout()

st.sidebar.divider()
st.sidebar.header("📥 Data Entry")
target_year = st.sidebar.selectbox("Year", [str(y) for y in range(2024, 2031)])
target_month = st.sidebar.selectbox(
    "Month", 
    ["January","February","March","April","May","June",
     "July","August","September","October","November","December"]
)

# --- ADD NEW MEMBER ---
with st.sidebar.expander("➕ Add New Member"):
    new_name = st.text_input("Full Name")
    new_phone = st.text_input("Phone")
    new_gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    if st.button("Save Member"):
        if target_year not in data: data[target_year] = {}
        if new_name.strip():
            data[target_year][new_name] = {"phone": new_phone, "gender": new_gender, "payments": []}
            save_data(data)
            st.success("Member Saved!")
            st.rerun()
        else:
            st.error("Name is required!")

# --- MAIN INTERFACE ---
st.title(f"📊 Ledger: {target_month} {target_year}")

if target_year in data and data[target_year]:
    search = st.text_input("🔍 Search Name or Gender").strip().lower()
    members = data[target_year]

    # Quick Stats
    males = len([n for n,i in members.items() if i.get('gender')=="Male"])
    females = len([n for n,i in members.items() if i.get('gender')=="Female"])
    st.write(f"👥 **Stats:** {males} Males | {females} Females")

    # Table header
    col1, col2, col3, col4 = st.columns([2,1,1,1])
    col1.write("**Member Detail**")
    col2.write("**Total Paid**")
    col3.write("**Action**")
    col4.write("**Manage**")
    st.divider()

    for name in list(members.keys()):
        info = members[name]
        gender_icon = "👨" if info.get('gender')=="Male" else "👩"

        # Search filter
        if not search or search in name.lower() or search in info.get('gender','').lower():

            paid = sum(p['amount'] for p in info['payments'])
            c1,c2,c3,c4 = st.columns([2,1,1,1])
            c1.write(f"{gender_icon} **{name}**\n({info['phone']})")
            c2.write(f"GHS {paid:.2f}")

            # Custom payment
            amount = c3.number_input("Amount", min_value=0.0, key=f"amt_{name}")
            if c3.button("💳 Pay", key=f"pay_{name}"):
                if amount>0:
                    info['payments'].append({"amount":amount,"month":target_month,"date":str(datetime.now())})
                    save_data(data)
                    st.success("Payment added!")
                    st.rerun()

            # --- UPDATE / DELETE ---
            st.write("⚙️ Manage Member:")
            new_p = st.text_input("Phone", value=info['phone'], key=f"edit_p_{name}")
            new_g = st.selectbox("Gender", ["Male","Female"], index=0 if info.get('gender')=="Male" else 1, key=f"edit_g_{name}")
            if st.button("Update Member", key=f"up_{name}"):
                info['phone'] = new_p
                info['gender'] = new_g
                save_data(data)
                st.success("Updated!")
                st.rerun()
            confirm = st.checkbox("Confirm Delete", key=f"confirm_{name}")
            if confirm and st.button("🗑️ Delete Member", key=f"del_{name}"):
                del data[target_year][name]
                save_data(data)
                st.warning("Deleted!")
                st.rerun()
else:
    st.warning("No records for this year yet.")
