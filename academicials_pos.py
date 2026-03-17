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
    st.session_state.logged_in = True

def logout():
    st.session_state.logged_in = False
    st.rerun()

# --- PAGE CONFIG ---
st.set_page_config(page_title="Academicians 2017", layout="wide")

# 🔥 MOVING HEADER (MARQUEE)
st.markdown("""
<style>
.marquee {
    width: 100%;
    overflow: hidden;
    white-space: nowrap;
}
.marquee span {
    display: inline-block;
    padding-left: 100%;
    animation: marquee 10s linear infinite alternate;
    font-weight: bold;
    font-size: 20px;
    color: white;
}
@keyframes marquee {
    0% { transform: translateX(0); }
    100% { transform: translateX(-100%); }
}
</style>

<div style="background-color:#1E3A8A;padding:15px;border-radius:10px;text-align:center;">
    <div class="marquee">
        <span>✨ ACADEMICIANS 2017 OFFICIAL LEDGER ✨</span>
    </div>
</div>
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
st.sidebar
