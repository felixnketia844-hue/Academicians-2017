# -*- coding: utf-8 -*-
""
#Created on Mon Mar 16 18:31:12 2026
#@author: felix
# Student Monthly Dues System

students = []

# Add student
def add_student():
    name = input("Enter student name: ")
    group = input("Enter group name: ")
    monthly_due = float(input("Enter monthly due amount: "))
    paid = float(input("Amount paid this month: "))
    
    student = {
        "name": name,
        "group": group,
        "monthly_due": monthly_due,
        "paid": paid
    }
    
    students.append(student)
    print("Student added successfully!")

# View students
def view_students():
    if not students:
        print("No records found.")
        return
    
    for i, s in enumerate(students):
        balance = s["monthly_due"] - s["paid"]
        print(f"{i}. Name: {s['name']}, Group: {s['group']}, Due: {s['monthly_due']}, Paid: {s['paid']}, Balance: {balance}")

# Update payment
def update_payment():
    view_students()
    index = int(input("Enter student number to update: "))
    
    extra_payment = float(input("Enter additional payment: "))
    students[index]["paid"] += extra_payment
    
    print("Payment updated successfully!")

# Delete student
def delete_student():
    view_students()
    index = int(input("Enter student number to delete: "))
    
    students.pop(index)
    print("Student deleted successfully!")

# Reset for new month
def reset_month():
    for s in students:
        s["paid"] = 0
    print("All payments reset for new month!")

# Menu
while True:
    print("\n--- Student Dues System ---")
    print("1. Add Student")
    print("2. View Records")
    print("3. Update Payment")
    print("4. Delete Student")
    print("5. New Month Reset")
    print("6. Exit")

    choice = input("Choose option: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        update_payment()
    elif choice == "4":
        delete_student()
    elif choice == "5":
        reset_month()
    elif choice == "6":
        break
    else:
        print("Invalid choice")
