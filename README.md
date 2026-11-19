# 💼 Employee Payroll Management System
## 📌 About The Project

The **Employee Payroll Management System** is a simple project developed using Python. I created this project to make employee record management and salary calculation easier.

It allows users to manage employee information, calculate salaries automatically, and generate detailed payslips. All employee records are stored in a JSON file.

## ✨ Key Features

| Feature               | Description                      |
| --------------------- | -------------------------------- |
| ➕ Add Employee        | Add new employee details         |
| 👥 View Employees     | Display all employee records     |
| 🧾 Generate Payslip   | Generate detailed salary slips   |
| ✏️ Update Employee    | Modify existing employee details |
| 🗑️ Delete Employee   | Remove employee records          |
| 💾 JSON Storage       | Save employee data permanently   |
| 🧮 Salary Calculation | Calculate salary automatically   |

## 🛠️ Technologies Used

- **Python 3.x** – Main programming language.
- **JSON Module** – To store and manage employee data.
- **OS Module** – To check and manage files.

## 💰 Salary Calculation

The system calculates salary using the following components:

| Salary Component | Percentage |
| ---------------- | ---------: |
| HRA              |        20% |
| DA               |        10% |
| PF               |        12% |
| Income Tax       |         5% |

**Net Salary = Gross Salary - Total Deductions**

## 🚀 How to Run

**Step 1:** Install Python 3.x.

**Step 2:** Save the source code as `payroll.py`.

**Step 3:** Open the terminal in the project folder.

**Step 4:** Run the following command:

```bash
python payroll.py
```

## 📂 Project Structure

```text
Employee-Payroll-Management/
│
├── 📄 payroll.py
├── 📄 payroll_data.json
└── 📄 README.md
```

## 📚 What I Learned

While developing this project, I learned how to use Python functions, loops, conditional statements, dictionaries, exception handling, and file handling. I also understood how JSON is used to store data permanently.

## 🔮 Future Improvements

- Add a graphical user interface.
- Connect the project with a database.
- Generate payslips in PDF format.
- Add employee login functionality.

## 🎯 Conclusion

This project helped me understand the practical use of Python in real-life applications. It improved my programming skills and gave me experience in developing a simple employee management system.
