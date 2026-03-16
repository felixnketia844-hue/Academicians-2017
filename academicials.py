# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 18:31:12 2026

@author: felix
"""

import tkinter as t-k
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

def initialize_files():
    if not os.path.exists('members.json'):
        with open('members.json', 'w') as f: json.dump({}, f)

class AcademiciansApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ACADEMICIANS 2017 - History & Treasury")
        self.root.geometry("1100x850")
        self.root.configure(bg="#1a1a1a")
        self.admin_code = "2017"
        self.show_login()

    def show_login(self):
        for widget in self.root.winfo_children(): widget.destroy()
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(frame, text="ACADEMICIANS 2017", font=("Impact", 35), fg="#f1c40f", bg="#1a1a1a").pack()
        self.code_ent = tk.Entry(frame, show="*", justify="center", font=("Arial", 20), width=8)
        self.code_ent.pack(pady=20)
        tk.Button(frame, text="LOGIN", command=self.check_login, bg="#27ae60", fg="white", width=15).pack()

    def check_login(self):
        if self.code_ent.get() == self.admin_code: self.main_ui()
        else: messagebox.showerror("Denied", "Incorrect Class Code!")

    def main_ui(self):
        for widget in self.root.winfo_children(): widget.destroy()
        
        # --- TOP NAV ---
        top = tk.Frame(self.root, bg="#2c3e50")
        top.pack(fill="x")
        tk.Label(top, text="ACADEMICIANS 2017 PORTAL", fg="white", bg="#2c3e50", font=("Arial", 12)).pack(side="left", padx=10)
        tk.Button(top, text="LOGOUT", command=self.show_login, bg="#e74c3c", fg="white").pack(side="right", padx=10, pady=5)

        # --- REGISTRATION ---
        reg = tk.LabelFrame(self.root, text=" Register New Person ", bg="#1a1a1a", fg="white", padx=10, pady=10)
        reg.pack(fill="x", padx=20, pady=10)
        
        tk.Label(reg, text="Name:", bg="#1a1a1a", fg="white").grid(row=0, column=0)
        self.n = tk.Entry(reg); self.n.grid(row=0, column=1, padx=5)
        
        tk.Label(reg, text="Gender:", bg="#1a1a1a", fg="white").grid(row=0, column=2)
        self.g = ttk.Combobox(reg, values=["Male", "Female"], width=8); self.g.grid(row=0, column=3, padx=5)
        
        tk.Label(reg, text="Role:", bg="#1a1a1a", fg="white").grid(row=0, column=4)
        self.r = ttk.Combobox(reg, values=["Leader", "Member"], width=10); self.r.grid(row=0, column=5, padx=5)
        
        tk.Button(reg, text="+ ADD", command=self.save_member, bg="#2ecc71", fg="white").grid(row=0, column=6, padx=10)

        # --- TABS FOR LEADERS & MEMBERS ---
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=5)

        self.leader_tab = tk.Frame(self.tabs)
        self.member_tab = tk.Frame(self.tabs)
        self.tabs.add(self.leader_tab, text="  EXECUTIVE LEADERS  ")
        self.tabs.add(self.member_tab, text="  GENERAL MEMBERS  ")

        self.l_tree = self.create_tree(self.leader_tab)
        self.m_tree = self.create_tree(self.member_tab)

        # --- PAYMENT & HISTORY SECTION ---
        bottom_frame = tk.Frame(self.root, bg="#1a1a1a")
        bottom_frame.pack(fill="x", padx=20, pady=10)

        # Payment Input
        pay_frame = tk.LabelFrame(bottom_frame, text=" Make Current Payment ", bg="#2c3e50", fg="white", padx=10, pady=10)
        pay_frame.pack(side="left", fill="y")
        
        tk.Label(pay_frame, text="Amount GHS:", bg="#2c3e50", fg="white").pack()
        self.amt = tk.Entry(pay_frame, font=("Arial", 12), width=10); self.amt.insert(0, "5"); self.amt.pack(pady=5)
        tk.Button(pay_frame, text="💰 CONFIRM", command=self.pay, bg="#f1c40f", font=("Arial", 10, "bold")).pack()

        # History View (PREVIOUS PAYMENTS)
        hist_frame = tk.LabelFrame(bottom_frame, text=" Previous Payment History ", bg="#1a1a1a", fg="#f1c40f", padx=10, pady=10)
        hist_frame.pack(side="right", fill="both", expand=True, padx=10)
        
        self.hist_tree = ttk.Treeview(hist_frame, columns=("Date", "Amount"), show="headings", height=5)
        self.hist_tree.heading("Date", text="Date/Time")
        self.hist_tree.heading("Amount", text="Amount Paid")
        self.hist_tree.pack(fill="both", expand=True)

        self.l_tree.bind("<<TreeviewSelect>>", lambda e: self.show_history(self.l_tree))
        self.m_tree.bind("<<TreeviewSelect>>", lambda e: self.show_history(self.m_tree))

        self.refresh()

    def create_tree(self, parent):
        t = ttk.Treeview(parent, columns=("Name", "Gender", "Total"), show="headings", height=8)
        t.heading("Name", text="Name"); t.heading("Gender", text="Gender"); t.heading("Total", text="Current Total (GHS)")
        t.pack(fill="both", expand=True)
        return t

    def save_member(self):
        name, gen, role = self.n.get(), self.g.get(), self.r.get()
        if name and gen and role:
            with open('members.json', 'r') as f: data = json.load(f)
            data[name] = {"gender": gen, "role": role, "total_paid": 0, "history": []}
            with open('members.json', 'w') as f: json.dump(data, f)
            self.refresh(); messagebox.showinfo("Success", f"{name} added!")
        else: messagebox.showerror("Error", "Fill all fields!")

    def show_history(self, tree):
        for i in self.hist_tree.get_children(): self.hist_tree.delete(i)
        sel = tree.selection()
        if not sel: return
        name = tree.item(sel)['values'][0]
        with open('members.json', 'r') as f: data = json.load(f)
        for entry in data[name].get('history', []):
            self.hist_tree.insert("", "0", values=(entry['date'], f"GHS {entry['amount']}"))

    def pay(self):
        sel_l, sel_m = self.l_tree.selection(), self.m_tree.selection()
        if not sel_l and not sel_m: return
        tree = self.l_tree if sel_l else self.m_tree
        name = tree.item(tree.selection())['values'][0]
        
        try:
            money = float(self.amt.get())
            date = datetime.now().strftime("%d-%b-%Y %H:%M")
            with open('members.json', 'r') as f: data = json.load(f)
            data[name]['total_paid'] += money
            data[name]['history'].append({"date": date, "amount": money})
            with open('members.json', 'w') as f: json.dump(data, f)
            self.refresh(); self.show_history(tree)
            messagebox.showinfo("Success", f"Paid GHS {money}")
        except: messagebox.showerror("Error", "Check Amount")

    def refresh(self):
        for t in [self.l_tree, self.m_tree]:
            for i in t.get_children(): t.delete(i)
        with open('members.json', 'r') as f: data = json.load(f)
        for name, info in data.items():
            vals = (name, info['gender'], f"{info['total_paid']:.2f}")
            if info['role'] == "Leader": self.l_tree.insert("", "end", values=vals)
            else: self.m_tree.insert("", "end", values=vals)

if __name__ == "__main__":
    initialize_files(); root = tk.Tk(); app = AcademiciansApp(root); root.mainloop()