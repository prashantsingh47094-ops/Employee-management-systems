/*
 * Employee Payroll Management System (C++)
 * Features: Add, View All, Payslip Generator, Update, Delete Records
 */
#include <iostream>
#include <vector>
#include <string>
#include <iomanip>

using namespace std;

struct Employee {
    string id, name, department;
    double basic;
};

vector<Employee> employees = {
    {"EMP101", "Rahul Sharma", "Engineering", 50000.0},
    {"EMP102", "Priya Patel",  "HR",          42000.0},
    {"EMP103", "Amit Kumar",   "Marketing",   38000.0}};

struct SalaryDetails {
    double hra, da, gross, pf, tax, deductions, net;
};

SalaryDetails calculateSalary(double b) {
    double hra = b * 0.20, da = b * 0.10, gross = b + hra + da;
    double pf = b * 0.12, tax = gross * 0.05, ded = pf + tax;
    return {hra, da, gross, pf, tax, ded, gross - ded};
}

int findEmployeeIndex(const string& id) {
    for (size_t i = 0; i < employees.size(); ++i)
        if (employees[i].id == id) return i;
    return -1;
}

void addEmployee() {
    string id;
    cout << "\nEnter Employee ID: "; cin >> id;
    if (findEmployeeIndex(id) != -1) {
        cout << "Error: Employee ID already exists!\n"; return;
    }
    Employee emp; emp.id = id;
    cin.ignore();
    cout << "Enter Employee Name: "; getline(cin, emp.name);
    cout << "Enter Department: "; getline(cin, emp.department);
    cout << "Enter Basic Salary (INR): ";
    if (!(cin >> emp.basic) || emp.basic < 0) {
        cout << "Invalid salary! Must be positive.\n";
        cin.clear(); cin.ignore(1000, '\n'); return;
    }
    employees.push_back(emp);
    cout << "Success: Employee '" << emp.name << "' (ID: " << emp.id << ") added!\n";
}

void viewAllEmployees() {
    if (employees.empty()) { cout << "\nNo employee records found.\n"; return; }
    cout << "\n=======================================================================\n"
         << left << setw(10) << "ID" << setw(18) << "Name" << setw(16) << "Department"
         << setw(14) << "Basic (INR)" << "Net Salary (INR)\n"
         << "-----------------------------------------------------------------------\n";
    for (const auto& emp : employees) {
        SalaryDetails s = calculateSalary(emp.basic);
        cout << left << setw(10) << emp.id << setw(18) << emp.name << setw(16) << emp.department
             << fixed << setprecision(2) << setw(14) << emp.basic << s.net << "\n";
    }
    cout << "=======================================================================\n";
}

void generatePayslip() {
    string id;
    cout << "\nEnter Employee ID for Payslip: "; cin >> id;
    int idx = findEmployeeIndex(id);
    if (idx == -1) {
        cout << "Error: Employee ID not found!\n"; return;
    }
    const auto& emp = employees[idx];
    SalaryDetails s = calculateSalary(emp.basic);

    cout << "\n=============================================\n           SALARY PAYSLIP                \n=============================================\n"
         << " Employee ID   : " << emp.id << "\n Name          : " << emp.name << "\n Department    : " << emp.department << "\n"
         << "---------------------------------------------\n" << fixed << setprecision(2)
         << " Basic Salary  : INR " << setw(10) << emp.basic << "\n HRA (20%)     : INR " << setw(10) << s.hra << "\n"
         << " DA (10%)      : INR " << setw(10) << s.da << "\n Gross Salary  : INR " << setw(10) << s.gross << "\n---------------------------------------------\n"
         << " PF (12%)      : INR " << setw(10) << s.pf << "\n Tax (5%)      : INR " << setw(10) << s.tax << "\n Total Deduct. : INR " << setw(10) << s.deductions << "\n"
         << "=============================================\n NET PAYABLE   : INR " << setw(10) << s.net << "\n=============================================\n";
}

void updateEmployee() {
    string id;
    cout << "\nEnter Employee ID to update: "; cin >> id;
    int idx = findEmployeeIndex(id);
    if (idx == -1) {
        cout << "Error: Employee ID not found!\n"; return;
    }
    auto& emp = employees[idx];
    cin.ignore();
    cout << "Current Name: " << emp.name << " | New Name: ";
    string newName; getline(cin, newName);
    if (!newName.empty()) emp.name = newName;
    cout << "Current Dept: " << emp.department << " | New Dept: ";
    string newDept; getline(cin, newDept);
    if (!newDept.empty()) emp.department = newDept;
    cout << "Current Basic: INR " << emp.basic << " | New Basic (-1 to keep): ";
    double newBasic;
    if (cin >> newBasic && newBasic >= 0) emp.basic = newBasic;
    else { cin.clear(); cin.ignore(1000, '\n'); }
    cout << "Employee details updated successfully!\n";
}

void deleteEmployee() {
    string id;
    cout << "\nEnter Employee ID to delete: "; cin >> id;
    int idx = findEmployeeIndex(id);
    if (idx == -1) {
        cout << "Error: Employee ID not found!\n"; return;
    }
    char confirm;
    cout << "Delete employee " << employees[idx].name << "? (y/n): "; cin >> confirm;
    if (confirm == 'y' || confirm == 'Y') {
        employees.erase(employees.begin() + idx);
        cout << "Employee ID " << id << " deleted successfully.\n";
    } else { cout << "Deletion cancelled.\n"; }
}

int main() {
    int choice;
    while (true) {
        cout << "\n==========================================\n"
             << "   EMPLOYEE PAYROLL MANAGEMENT SYSTEM     \n"
             << "==========================================\n"
             << " 1. Add New Employee\n 2. View All Employees\n"
             << " 3. Generate Salary Payslip\n 4. Update Employee Record\n"
             << " 5. Delete Employee Record\n 6. Exit\n"
             << "==========================================\n"
             << "Enter your choice (1-6): ";
        if (!(cin >> choice)) { cin.clear(); cin.ignore(1000, '\n'); continue; }

        switch (choice) {
            case 1: addEmployee(); break;
            case 2: viewAllEmployees(); break;
            case 3: generatePayslip(); break;
            case 4: updateEmployee(); break;
            case 5: deleteEmployee(); break;
            case 6: cout << "\nExiting Payroll System. Thank you!\n"; return 0;
            default: cout << "Invalid option! Please enter 1-6.\n";
        }
    }
}
