# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 18:31:12 2026

@author: felix
"""  
import streamlit as st
import streamlit as st
import json
import os
from datetime import datetime

def initialize_files():
    if not os.path.exists('members_yearly.json'):
        with open('members_yearly.json', 'w') as f: json.dump({}, f)

class AcademiciansApp:
    def __init__(self, root):
        self.root = root
        st.tittle("ACADEMECIANLS 2017-Official ledger")
        self.root.geometry("1400x800")
        self.root.configure(bg="#1a1a1a")
        
        self.admin_pass = "2017"
        self.viewer_pass = "9999"
        self.security_pin = "1957"
        self.access_level = "Viewer"
        
        initialize_files()
        self.show_login()

    def show_login(self):
        for widget in self.root.winfo_children(): widget.destroy()
        f = tk.Frame(self.root, bg="#1a1a1a")
        f.place(relx=0.5, rely=0.5, anchor="center")
        sk.write (f, text="ACADEMICIANS 2017", font=("Impact", 50), fg="#f1c40f", bg="#1a1a1a").pack()
        self.code_ent = tk.Entry(f, show="*", justify="center", font=("Arial", 25), width=10)
        self.code_ent.pack(pady=20)
        tk.Button(f, text="SECURE LOGIN", command=self.check_login, bg="#27ae60", fg="white", font=("Arial", 12, "bold"), width=20).pack()

    def check_login(self):
        code = self.code_ent.get()
        if code == self.admin_pass: self.access_level = "Admin"; self.main_ui()
        elif code == self.viewer_pass: self.access_level = "Viewer"; self.main_ui()
        else: messagebox.showerror("Error", "Invalid Code")

    def main_ui(self):
        for widget in self.root.winfo_children(): widget.destroy()
        top = tk.Frame(self.root, bg="#2c3e50", pady=15)
        top.pack(fill="x")
        
        # Row 1: Search and Selection
        tk.Label(top, text="🔍 SEARCH:", bg="#2c3e50", fg="#f1c40f").grid(row=0, column=0, padx=5)
        self.search_var = tk.StringVar(); self.search_var.trace("w", lambda *args: self.refresh())
        tk.Entry(top, textvariable=self.search_var, width=20).grid(row=0, column=1, sticky="w")

        tk.Label(top, text="YEAR:", bg="#2c3e50", fg="white").grid(row=0, column=2, padx=5)
        self.y_sel = ttk.Combobox(top, values=[str(y) for y in range(2017, 2051)], width=6, state="readonly")
        self.y_sel.set(datetime.now().strftime("%Y")); self.y_sel.grid(row=0, column=3)
        self.y_sel.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        # Row 2: Inputs
        tk.Label(top, text="Name:", bg="#2c3e50", fg="white").grid(row=1, column=0, pady=10)
        self.n = tk.Entry(top, width=15); self.n.grid(row=1, column=1)
        tk.Label(top, text="Phone:", bg="#2c3e50", fg="white").grid(row=1, column=2)
        self.ph = tk.Entry(top, width=15); self.ph.grid(row=1, column=3)
        tk.Label(top, text="Amt:", bg="#2c3e50", fg="white").grid(row=1, column=4)
        self.amt = tk.Entry(top, width=8); self.amt.insert(0, "5.00"); self.amt.grid(row=1, column=5)

        # Action Buttons
        btn_f = tk.Frame(top, bg="#2c3e50")
        btn_f.grid(row=1, column=6, columnspan=4, padx=10)
        
        self.save_btn = tk.Button(btn_f, text="SAVE", command=self.save_entry, bg="#2ecc71", width=10)
        self.save_btn.pack(side="left", padx=2)
        self.upd_btn = tk.Button(btn_f, text="UPDATE", command=self.update_entry, bg="#3498db", fg="white", width=10)
        self.upd_btn.pack(side="left", padx=2)
        self.del_btn = tk.Button(btn_f, text="DELETE", command=self.delete_entry, bg="#e74c3c", fg="white", width=10)
        self.del_btn.pack(side="left", padx=2)
        
        tk.Button(top, text="SEND TO WHATSAPP", command=self.share_report, bg="#f39c12", width=18).grid(row=0, column=6, padx=10)
        tk.Button(top, text="LOGOUT", command=self.show_login, bg="#95a5a6").grid(row=0, column=7)

        if self.access_level == "Viewer":
            for b in [self.save_btn, self.upd_btn, self.del_btn]: b.config(state="disabled")

        # Table
        self.tree = ttk.Treeview(self.root, columns=("Name", "Phone", "Paid", "Debt", "Months"), show="headings", height=20)
        for col in self.tree["columns"]: self.tree.heading(col, text=col.upper())
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        self.total_lbl = tk.Label(self.root, text="TOTAL REVENUE: GHS 0.00", font=("Arial", 18, "bold"), bg="#1a1a1a", fg="#f1c40f")
        self.total_lbl.pack(pady=10)
        
        self.refresh()

    def refresh(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        year, search = self.y_sel.get(), self.search_var.get().lower()
        with open('members_yearly.json', 'r') as f: data = json.load(f)
        total_rev = 0
        curr_month_idx = datetime.now().month if year == datetime.now().strftime("%Y") else 12
        
        if year in data:
            for n, info in data[year].items():
                if search in n.lower():
                    paid = sum([p['amount'] for p in info.get('payments', [])])
                    debt = (curr_month_idx * 5) - paid
                    mlist = ", ".join([p['month'] for p in info.get('payments', [])])
                    self.tree.insert("", "end", values=(n, info.get('phone',''), f"{paid:.2f}", f"{max(0, debt):.2f}", mlist))
                    total_rev += paid
        self.total_lbl.config(text=f"{year} TOTAL REVENUE: GHS {total_rev:.2f}")

    def on_select(self, event):
        sel = self.tree.selection()
        if sel:
            v = self.tree.item(sel[0])['values']
            self.n.delete(0, tk.END); self.n.insert(0, v[0])
            self.ph.delete(0, tk.END); self.ph.insert(0, v[1])

    def save_entry(self):
        y, n, p, amt = self.y_sel.get(), self.n.get().strip(), self.ph.get().strip(), self.amt.get()
        if not n or not amt: return
        with open('members_yearly.json', 'r') as f: data = json.load(f)
        if y not in data: data[y] = {}
        if n not in data[y]: data[y][n] = {"phone": p, "payments": []}
        data[y][n]["payments"].append({"month": datetime.now().strftime("%b"), "amount": float(amt)})
        with open('members_yearly.json', 'w') as f: json.dump(data, f)
        self.n.delete(0, tk.END); self.refresh()

    def update_entry(self):
        if simpledialog.askstring("PIN", "Security PIN:") == self.security_pin:
            sel = self.tree.selection()
            if not sel: return
            old_name = self.tree.item(sel[0])['values'][0]
            year = self.y_sel.get()
            with open('members_yearly.json', 'r') as f: data = json.load(f)
            data[year][self.n.get()] = data[year].pop(old_name)
            data[year][self.n.get()]["phone"] = self.ph.get()
            with open('members_yearly.json', 'w') as f: json.dump(data, f)
            self.refresh()

    def delete_entry(self):
        if simpledialog.askstring("PIN", "Security PIN:") == self.security_pin:
            sel = self.tree.selection()
            if not sel: return
            name, year = self.tree.item(sel[0])['values'][0], self.y_sel.get()
            with open('members_yearly.json', 'r') as f: data = json.load(f)
            del data[year][name]
            with open('members_yearly.json', 'w') as f: json.dump(data, f)
            self.refresh()

    def share_report(self):
        year = self.y_sel.get()
        with open('members_yearly.json', 'r') as f: data = json.load(f)
        report = f"*ACADEMICIANS 2017 FINANCIAL REPORT ({year})*\n\n"
        if year in data:
            for n, info in data[year].items():
                paid = sum([p['amount'] for p in info.get('payments', [])])
                report += f"• {n}: GHS {paid:.2f}\n"
        
        with open("WhatsApp_Report.txt", "w", encoding="utf-8") as f: f.write(report)
        os.startfile("WhatsApp_Report.txt")
        st.sucess("Information Saved!")

if __name__ == "__main__":
    root = tk.Tk(); app = AcademiciansApp(root); root.mainloop()
