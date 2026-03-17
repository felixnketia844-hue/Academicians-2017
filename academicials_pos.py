# -*- coding: utf-8 -*-
""
#Created on Mon Mar 16 18:31:12 2026
#@author: felix
# Student Monthly Dues System
import streamlit as st
import json
import os
from datetime import datetime

# --- 1. DATA STORAGE ---
def load_data():
    if not os.path.exists('members_data.json'):
        # Initialize with separate keys for members and expenses
        with open('members_data.json', 'w') as f: json.dump({"members": {}, "expenses": {}}, f)
    with open('members_data.json', 'r') as f: 
        try: 
            db = json.load(f)
            if "members" not in db: db = {"members": db, "expenses": {}}
            return db
        except: 
            return {"members": {}, "expenses": {}}

def save_data(data):
    with open('members_data.json', 'w') as f: 
        json.dump(data, f, indent=4)

# --- 2. SETUP ---
st.set_page_config(page_title="Academicians 2017", layout="wide")
db = load_data()

# --- 3. SIDEBAR ---
st.sidebar.header("⚙️ Settings")
year_list = [str(y) for y in range(2024, 2051)]
target_year = st.sidebar.selectbox("Select Year", year_list)
target_month = st.sidebar.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

st.sidebar.divider()

# ADD NEW MEMBER
with st.sidebar.expander("➕ REGISTER NEW MEMBER"):
    new_name = st.text_input("Full Name")
    new_phone = st.text_input("Phone Number")
    if st.button("Save Member", use_container_width=True):
        if target_year not in db["members"]: db["members"][target_year] = {}
        if new_name:
            db["members"][target_year][new_name] = {"phone": new_phone, "gender": "N/A", "payments": []}
            save_data(db)
            st.rerun()

# RECORD EXPENDITURE (SPENDING)
with st.sidebar.expander("💸 RECORD EXPENSES (SPENDING)"):
    exp_desc = st.text_input("What did you buy?")
    exp_amt = st.number_input("Amount Spent (GHS)", min_value=0.0)
    if st.button("Save Expense", use_container_width=True):
        if target_year not in db["expenses"]: db["expenses"][target_year] = {}
        if target_month not in db["expenses"][target_year]: db["expenses"][target_year][target_month] = []
        
        if exp_desc and exp_amt > 0:
            db["expenses"][target_year][target_month].append({
                "description": exp_desc,
                "amount": exp_amt,
                "date": datetime.now().strftime("%Y-%m-%d")
            })
            save_data(db)
            st.success("Expense recorded!")
            st.rerun()

# --- 4. MAIN SCREEN ---
st.title(f"📊 Ledger & Spending: {target_month} {target_year}")
search = st.text_input("🔍 Search Members...", placeholder="Type name here...")

st.divider()

total_income = 0.0
total_spent = 0.0

# --- DISPLAY MEMBERS & INCOME ---
if target_year in db["members"] and db["members"][target_year]:
    members = db["members"][target_year]
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    col1.subheader("Member")
    col2.subheader("Payments")
    col3.subheader("Update")
    col4.subheader("Remove")

    for name in list(members.keys()):
        info = members[name]
        this_month_paid = sum(p['amount'] for p in info['payments'] if p['month'] == target_month)
        total_income += this_month_paid

        if search.lower() in name.lower():
            c1, c2, c3, c4 = st.columns([2, 2, 2, 1])
            with c1:
                st.write(f"**{name}**")
                st.caption(f"📞 {info['phone']}")
            with c2:
                amt = st.number_input("GHS", min_value=0.0, key=f"p_{name}")
                if st.button(f"Pay", key=f"b_{name}"):
                    info['payments'].append({"amount": amt, "month": target_month, "date": str(datetime.now())})
                    save_data(db); st.rerun()
                st.write(f"Total: **{this_month_paid}**")
            with c3:
                new_p = st.text_input("Edit", value=info['phone'], key=f"e_{name}")
                if st.button("Update", key=f"u_{name}"):
                    info['phone'] = new_p; save_data(db); st.rerun()
            with c4:
                if st.button("🗑️", key=f"d_{name}"):
                    del db["members"][target_year][name]; save_data(db); st.rerun()
            st.divider()

# --- DISPLAY EXPENSES ---
st.subheader("📋 Spending Log (Expenses)")
if target_year in db["expenses"] and target_month in db["expenses"][target_year]:
    for i, ex in enumerate(db["expenses"][target_year][target_month]):
        total_spent += ex['amount']
        st.write(f"🔴 Spent **GHS {ex['amount']}** on *{ex['description']}* ({ex['date']})")
else:
    st.write("No expenses recorded for this month.")

st.divider()

# --- 5. FINAL SUMMARY ---
st.header("📈 Financial Summary")
m1, m2, m3 = st.columns(3)
m1.metric("Total Income", f"GHS {total_income:.2f}")
m2.metric("Total Spent", f"GHS {total_spent:.2f}", delta=f"-{total_spent}", delta_color="inverse")
m3.metric("Net Balance", f"GHS {total_income - total_spent:.2f}")
