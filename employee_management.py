"""Employee Payroll Management System (data saved in employees.json)."""

import json
import os
from datetime import datetime

DATA_FILE = "employees.json"
HRA_RATE, DA_RATE, PF_RATE = 0.20, 0.10, 0.12
OVERTIME_RATE = 300  # rupees per overtime hour

class Employee:
    def __init__(self, emp_id, name, department, designation, basic_salary):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.designation = designation
        self.basic_salary = basic_salary

def load_employees():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE) as f:
            return {k: Employee(**v) for k, v in json.load(f).items()}
    except (ValueError, TypeError, AttributeError):
        os.replace(DATA_FILE, DATA_FILE + ".bak")
        print(f"  Warning: data file kharab thi, backup '{DATA_FILE}.bak' me rakhi.")
        return {}

def save_employees(employees):
    with open(DATA_FILE, "w") as f:
        json.dump({k: vars(e) for k, e in employees.items()}, f, indent=4)

def calculate_tax(annual):
    """Simple slab based annual income tax."""
    tax = 0
    for limit, rate in ((1000000, 0.30), (500000, 0.20), (250000, 0.05)):
        if annual > limit:
            tax += (annual - limit) * rate
            annual = limit
    return tax

def calculate_salary(emp, overtime_hours=0, bonus=0):
    basic = emp.basic_salary
    hra, da = basic * HRA_RATE, basic * DA_RATE
    overtime = overtime_hours * OVERTIME_RATE
    regular = basic + hra + da + overtime
    pf = basic * PF_RATE
    base_tax = calculate_tax(regular * 12)
    tax = base_tax / 12 + (calculate_tax(regular * 12 + bonus) - base_tax)
    gross = regular + bonus
    return {"basic": basic, "hra": hra, "da": da, "overtime": overtime,
            "bonus": bonus, "gross": gross, "pf": pf, "tax": tax,
            "net": gross - pf - tax}

def get_text(prompt, default=None, keep_case=False):
    """Khali input nahi leta. default ho to khali par wahi value milti hai."""
    while True:
        value = input(prompt).strip()
        if not value and default is not None:
            return default
        if value:
            return value.upper() if keep_case else (value if value.isupper() else value.title())
        print("  Ye field khali nahi ho sakti.")

def get_number(prompt, minimum=0):
    while True:
        try:
            value = float(input(prompt))
            if value >= minimum:
                return value
            print(f"  Value {minimum} se kam nahi ho sakti.")
        except ValueError:
            print("  Galat input, dobara try karo.")

def find_employee(employees):
    emp = employees.get(get_text("Employee ID: ", keep_case=True))
    if not emp:
        print("  Employee nahi mila.")
    return emp

def add_employee(employees):
    emp_id = get_text("Employee ID: ", keep_case=True)
    if emp_id in employees:
        print("  Ye ID pehle se maujood hai!")
        return
    name = get_text("Name: ")
    dept = get_text("Department: ")
    desig = get_text("Designation: ")
    basic = get_number("Basic Salary (monthly): ", minimum=1)
    employees[emp_id] = Employee(emp_id, name, dept, desig, basic)
    save_employees(employees)
    print(f"  Done: {name} add ho gaya.")

def view_employees(employees):
    if not employees:
        print("  Koi employee record nahi hai.")
        return
    print("=" * 70)
    print(f"{'ID':<8}{'Name':<20}{'Department':<16}{'Designation':<16}{'Basic':>10}")
    print("=" * 70)
    for e in employees.values():
        print(f"{e.emp_id:<8}{e.name:<20}{e.department:<16}"
              f"{e.designation:<16}{e.basic_salary:>10.2f}")
    print("=" * 70)

def search_employee(employees):
    key = get_text("Naam, ID ya department search karo: ", keep_case=True).lower()
    found = [e for e in employees.values()
             if key in (e.name + " " + e.department).lower() or key == e.emp_id.lower()]
    if not found:
        print("  Koi match nahi mila.")
    for e in found:
        print(f"  {e.emp_id} | {e.name} | {e.department} | "
              f"{e.designation} | Rs.{e.basic_salary:.2f}")

def update_employee(employees):
    emp = find_employee(employees)
    if not emp:
        return
    print("  (Text khali chhodo / salary me 0 do to purani value rahegi)")
    for field in ("name", "department", "designation"):
        old = getattr(emp, field)
        setattr(emp, field, get_text(f"{field.title()} [{old}]: ", default=old))
    emp.basic_salary = get_number(f"Basic Salary [{emp.basic_salary}]: ") or emp.basic_salary
    save_employees(employees)
    print("  Done: record update ho gaya.")

def delete_employee(employees):
    emp = find_employee(employees)
    if emp and input(f"Pakka delete {emp.name}? (y/n): ").strip().lower() == "y":
        del employees[emp.emp_id]
        save_employees(employees)
        print("  Done: delete ho gaya.")

def generate_payslip(employees):
    emp = find_employee(employees)
    if not emp:
        return
    s = calculate_salary(emp, get_number("Overtime hours: "),
                         get_number("Bonus amount: "))
    bar, thin = "=" * 44, "-" * 44
    rows = [("Basic Salary", "basic"), ("HRA (20%)", "hra"), ("DA (10%)", "da"),
            ("Overtime", "overtime"), ("Bonus", "bonus"), ("Gross Salary", "gross"),
            thin, ("PF (12%)", "pf"), ("Income Tax", "tax"), bar, ("NET SALARY", "net")]
    lines = [bar, f"        PAYSLIP - {datetime.now():%B %Y}", bar,
             f"Employee ID : {emp.emp_id}", f"Name        : {emp.name}",
             f"Department  : {emp.department}", f"Designation : {emp.designation}", thin]
    lines += [r if isinstance(r, str) else f"{r[0]:<20}: {s[r[1]]:>12.2f}" for r in rows]
    lines.append(bar)
    print("\n".join(lines))
    filename = f"payslip_{emp.emp_id}_{datetime.now():%Y%m%d_%H%M%S}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Done: payslip '{filename}' me save ho gayi.")

def payroll_report(employees):
    if not employees:
        print("  Koi employee record nahi hai.")
        return
    total_gross = total_net = 0
    print("=" * 66)
    print(f"{'ID':<8}{'Name':<20}{'Gross':>12}{'Deductions':>14}{'Net':>12}")
    print("=" * 66)
    for e in employees.values():
        s = calculate_salary(e)
        total_gross += s["gross"]
        total_net += s["net"]
        print(f"{e.emp_id:<8}{e.name:<20}{s['gross']:>12.2f}"
              f"{s['pf'] + s['tax']:>14.2f}{s['net']:>12.2f}")
    print("=" * 66)
    print(f"Total Employees : {len(employees)}")
    print(f"Total Gross     : Rs.{total_gross:,.2f}")
    print(f"Total Net Payout: Rs.{total_net:,.2f}")

def main():
    employees = load_employees()
    actions = {"1": add_employee, "2": view_employees, "3": search_employee,
               "4": update_employee, "5": delete_employee,
               "6": generate_payslip, "7": payroll_report}
    try:
        while True:
            print("\n===== EMPLOYEE PAYROLL MANAGEMENT SYSTEM =====\n"
                  "1. Add Employee        5. Delete Employee\n"
                  "2. View All Employees  6. Generate Payslip\n"
                  "3. Search Employee     7. Payroll Report\n"
                  "4. Update Employee     8. Exit")
            choice = input("Choice (1-8): ").strip()
            if choice == "8":
                break
            if choice in actions:
                actions[choice](employees)
            else:
                print("  Galat choice, 1-8 me se chuno.")
    except (KeyboardInterrupt, EOFError):
        print()
    print("Dhanyavaad! Program band ho raha hai.")

if __name__ == "__main__":
    main()