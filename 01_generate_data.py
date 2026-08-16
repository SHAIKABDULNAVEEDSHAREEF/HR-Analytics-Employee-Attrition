"""
HR Analytics & Employee Attrition - Synthetic Dataset Generator
Generates a realistic, internally-consistent HR dataset of 1,500 employees.
Author: Shaik Abdul Naveed Shareef
"""

import numpy as np
import pandas as pd

np.random.seed(42)
N = 1500

departments = {
    "Sales": {"weight": 0.31, "roles": ["Sales Executive", "Sales Representative", "Sales Manager"], "base_salary": 42000},
    "Research & Development": {"weight": 0.38, "roles": ["Research Scientist", "Laboratory Technician", "Manufacturing Director", "R&D Manager"], "base_salary": 48000},
    "Human Resources": {"weight": 0.06, "roles": ["HR Executive", "HR Manager", "Recruiter"], "base_salary": 38000},
    "Finance": {"weight": 0.10, "roles": ["Financial Analyst", "Accountant", "Finance Manager"], "base_salary": 50000},
    "IT": {"weight": 0.15, "roles": ["Data Analyst", "Software Engineer", "IT Support", "IT Manager"], "base_salary": 55000},
}

dept_names = list(departments.keys())
dept_probs = [departments[d]["weight"] for d in dept_names]

education_fields = ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Human Resources", "Other"]
marital_status = ["Single", "Married", "Divorced"]
genders = ["Male", "Female"]

rows = []
for emp_id in range(1, N + 1):
    dept = np.random.choice(dept_names, p=dept_probs)
    role = np.random.choice(departments[dept]["roles"])
    age = int(np.clip(np.random.normal(36, 9), 20, 60))
    gender = np.random.choice(genders, p=[0.6, 0.4])
    marital = np.random.choice(marital_status, p=[0.32, 0.48, 0.20])
    education_level = np.random.choice([1, 2, 3, 4, 5], p=[0.08, 0.22, 0.35, 0.27, 0.08])
    education_field = np.random.choice(education_fields)
    distance = int(np.clip(np.random.exponential(8), 1, 40))

    years_at_company = int(np.clip(np.random.exponential(5.5), 0, min(age - 20, 37)))
    years_in_role = int(np.clip(years_at_company * np.random.uniform(0.3, 1.0), 0, years_at_company))
    years_since_promo = int(np.clip(np.random.exponential(2.2), 0, years_at_company))
    total_working_years = int(np.clip(years_at_company + np.random.randint(0, 8), 0, age - 18))

    job_level = int(np.clip(1 + years_at_company // 4 + np.random.randint(-1, 2), 1, 5))
    base = departments[dept]["base_salary"]
    monthly_income = int(np.clip(
        base * (1 + 0.35 * (job_level - 1)) * np.random.uniform(0.85, 1.2), 15000, 200000
    ))

    job_satisfaction = np.random.choice([1, 2, 3, 4], p=[0.13, 0.20, 0.31, 0.36])
    env_satisfaction = np.random.choice([1, 2, 3, 4], p=[0.15, 0.19, 0.30, 0.36])
    work_life_balance = np.random.choice([1, 2, 3, 4], p=[0.06, 0.24, 0.53, 0.17])
    performance_rating = np.random.choice([3, 4], p=[0.85, 0.15])
    job_involvement = np.random.choice([1, 2, 3, 4], p=[0.09, 0.26, 0.51, 0.14])
    relationship_satisfaction = np.random.choice([1, 2, 3, 4], p=[0.13, 0.21, 0.31, 0.35])

    overtime = np.random.choice(["Yes", "No"], p=[0.30, 0.70])
    business_travel = np.random.choice(
        ["Non-Travel", "Travel_Rarely", "Travel_Frequently"], p=[0.10, 0.71, 0.19]
    )
    training_times = np.random.choice([0, 1, 2, 3, 4, 5, 6], p=[0.04, 0.11, 0.35, 0.24, 0.15, 0.08, 0.03])
    stock_option = np.random.choice([0, 1, 2, 3], p=[0.42, 0.38, 0.15, 0.05])
    num_companies_worked = int(np.clip(np.random.poisson(2.7), 0, 9))
    percent_salary_hike = int(np.clip(np.random.normal(15, 3.5), 11, 25))

    # ---- Attrition probability model (logistic-style, business-realistic drivers) ----
    score = -1.95
    score += 0.9 if overtime == "Yes" else 0
    score += (4 - job_satisfaction) * 0.32
    score += (4 - work_life_balance) * 0.28
    score += (4 - env_satisfaction) * 0.22
    score += 0.55 if business_travel == "Travel_Frequently" else 0
    score += -0.05 * years_at_company
    score += 0.06 * max(0, 30 - age)
    score += -0.000012 * monthly_income
    score += 0.10 if marital == "Single" else -0.05
    score += 0.08 if dept == "Sales" else 0
    score += 0.05 * num_companies_worked
    score += -0.20 * job_level

    prob = 1 / (1 + np.exp(-score))
    attrition = "Yes" if np.random.random() < prob else "No"

    rows.append([
        emp_id, age, gender, marital, dept, role, job_level,
        education_level, education_field, distance,
        monthly_income, percent_salary_hike, stock_option,
        total_working_years, years_at_company, years_in_role,
        years_since_promo, num_companies_worked, training_times,
        overtime, business_travel, job_satisfaction, env_satisfaction,
        work_life_balance, job_involvement, relationship_satisfaction,
        performance_rating, attrition
    ])

columns = [
    "EmployeeID", "Age", "Gender", "MaritalStatus", "Department", "JobRole", "JobLevel",
    "Education", "EducationField", "DistanceFromHome",
    "MonthlyIncome", "PercentSalaryHike", "StockOptionLevel",
    "TotalWorkingYears", "YearsAtCompany", "YearsInCurrentRole",
    "YearsSinceLastPromotion", "NumCompaniesWorked", "TrainingTimesLastYear",
    "OverTime", "BusinessTravel", "JobSatisfaction", "EnvironmentSatisfaction",
    "WorkLifeBalance", "JobInvolvement", "RelationshipSatisfaction",
    "PerformanceRating", "Attrition"
]

df = pd.DataFrame(rows, columns=columns)
df.to_csv("/home/claude/hr_project/data/hr_employee_attrition.csv", index=False)

print("Dataset shape:", df.shape)
print("\nOverall attrition rate: {:.2f}%".format((df.Attrition == "Yes").mean() * 100))
print("\nAttrition by department:")
print(df.groupby("Department")["Attrition"].apply(lambda x: (x == "Yes").mean() * 100).round(2))
