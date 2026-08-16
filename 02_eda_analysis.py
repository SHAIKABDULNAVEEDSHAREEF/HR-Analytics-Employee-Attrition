"""
HR Analytics & Employee Attrition - Exploratory Data Analysis (EDA)
Produces cleaned summary tables + publication-quality charts for the report
and dashboard.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#222222",
    "text.color": "#222222",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "axes.titleweight": "bold",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

NAVY = "#12294B"
GOLD = "#C9A227"
TEAL = "#1F7A6C"
RED  = "#B5443B"
GREY = "#8A94A6"
PALETTE = [NAVY, GOLD, TEAL, RED, GREY, "#5B7FBF"]

df = pd.read_csv("/home/claude/hr_project/data/hr_employee_attrition.csv")
CHARTS = "/home/claude/hr_project/charts"

# ---------------------------------------------------------------
def savefig(fig, name):
    fig.tight_layout()
    fig.savefig(f"{CHARTS}/{name}.png", dpi=200, bbox_inches="tight", facecolor="white")
    # also save a transparent/dashboard-ready variant with light-on-dark styling
    plt.close(fig)

# =================================================================
# 1. DATASET OVERVIEW
# =================================================================
total_emp = len(df)
attrition_count = (df.Attrition == "Yes").sum()
attrition_rate = round(100 * attrition_count / total_emp, 2)
active_emp = total_emp - attrition_count
avg_income = round(df.MonthlyIncome.mean(), 0)
avg_tenure = round(df.YearsAtCompany.mean(), 1)
avg_age = round(df.Age.mean(), 1)

print("="*60)
print("DATASET OVERVIEW")
print("="*60)
print(f"Total Employees        : {total_emp}")
print(f"Employees who left     : {attrition_count}")
print(f"Active Employees       : {active_emp}")
print(f"Overall Attrition Rate : {attrition_rate}%")
print(f"Avg Monthly Income     : {avg_income}")
print(f"Avg Tenure (yrs)       : {avg_tenure}")
print(f"Avg Age                : {avg_age}")
print(f"Missing values total   : {df.isna().sum().sum()}")
print(f"Duplicate rows         : {df.duplicated().sum()}")

# =================================================================
# 2. ATTRITION DONUT (overall)
# =================================================================
fig, ax = plt.subplots(figsize=(7.2, 5.2))
sizes = [attrition_count, active_emp]
labels = [f"Left\n{attrition_count} ({attrition_rate}%)", f"Active\n{active_emp} ({100-attrition_rate:.1f}%)"]
wedges, _ = ax.pie(sizes, colors=[RED, NAVY], startangle=90, wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2))
ax.legend(wedges, labels, loc="center", frameon=False, fontsize=11)
ax.set_title("Overall Attrition Split", fontsize=14, pad=15)
savefig(fig, "01_overall_attrition_donut")

# =================================================================
# 3. DEPARTMENT-WISE ATTRITION
# =================================================================
dept_stats = df.groupby("Department").agg(
    headcount=("EmployeeID", "count"),
    attrition_count=("Attrition", lambda x: (x == "Yes").sum()),
    avg_income=("MonthlyIncome", "mean"),
).reset_index()
dept_stats["attrition_rate"] = round(100 * dept_stats.attrition_count / dept_stats.headcount, 2)
dept_stats = dept_stats.sort_values("attrition_rate", ascending=False)

fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.barh(dept_stats.Department, dept_stats.attrition_rate, color=NAVY)
for i, (b, v, h) in enumerate(zip(bars, dept_stats.attrition_rate, dept_stats.headcount)):
    ax.text(v + 0.3, b.get_y() + b.get_height()/2, f"{v}%  (n={h})", va="center", fontsize=10)
ax.set_xlabel("Attrition Rate (%)")
ax.set_title("Attrition Rate by Department", fontsize=14)
ax.invert_yaxis()
ax.spines[['top','right']].set_visible(False)
ax.set_xlim(0, dept_stats.attrition_rate.max() + 6)
savefig(fig, "02_department_attrition")

# =================================================================
# 4. JOB ROLE ATTRITION (top risk roles)
# =================================================================
role_stats = df.groupby(["Department", "JobRole"]).agg(
    headcount=("EmployeeID", "count"),
    attrition_count=("Attrition", lambda x: (x == "Yes").sum())
).reset_index()
role_stats = role_stats[role_stats.headcount >= 15]
role_stats["attrition_rate"] = round(100 * role_stats.attrition_count / role_stats.headcount, 2)
role_stats = role_stats.sort_values("attrition_rate", ascending=False).head(8)

fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.barh(role_stats.JobRole, role_stats.attrition_rate, color=GOLD)
for b, v in zip(bars, role_stats.attrition_rate):
    ax.text(v + 0.3, b.get_y() + b.get_height()/2, f"{v}%", va="center", fontsize=10)
ax.set_xlabel("Attrition Rate (%)")
ax.set_title("Top Job Roles by Attrition Risk", fontsize=14)
ax.invert_yaxis()
ax.spines[['top','right']].set_visible(False)
savefig(fig, "03_jobrole_attrition")

# =================================================================
# 5. SALARY ANALYSIS
# =================================================================
def salary_band(x):
    if x < 30000: return "1. <30K"
    elif x < 50000: return "2. 30K-50K"
    elif x < 80000: return "3. 50K-80K"
    elif x < 120000: return "4. 80K-120K"
    else: return "5. 120K+"

df["SalaryBand"] = df.MonthlyIncome.apply(salary_band)
salary_stats = df.groupby("SalaryBand").agg(
    headcount=("EmployeeID", "count"),
    attrition_count=("Attrition", lambda x: (x == "Yes").sum())
).reset_index()
salary_stats["attrition_rate"] = round(100 * salary_stats.attrition_count / salary_stats.headcount, 2)

fig, ax1 = plt.subplots(figsize=(8, 4.5))
ax1.bar(salary_stats.SalaryBand, salary_stats.headcount, color=GREY, alpha=0.55, label="Headcount")
ax1.set_ylabel("Headcount")
ax2 = ax1.twinx()
ax2.plot(salary_stats.SalaryBand, salary_stats.attrition_rate, color=RED, marker="o", linewidth=2.5, label="Attrition Rate")
for x, y in zip(salary_stats.SalaryBand, salary_stats.attrition_rate):
    ax2.annotate(f"{y}%", (x, y), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9, color=RED, fontweight="bold")
ax2.set_ylabel("Attrition Rate (%)")
ax1.set_title("Salary Band: Headcount vs Attrition Rate", fontsize=14)
ax1.spines[['top']].set_visible(False)
ax2.spines[['top']].set_visible(False)
fig.legend(loc="upper right", bbox_to_anchor=(0.88, 0.88), frameon=False, fontsize=9)
savefig(fig, "04_salary_band_attrition")

# Avg income: stayed vs left
income_compare = df.groupby("Attrition")["MonthlyIncome"].mean().round(0)
fig, ax = plt.subplots(figsize=(5, 4.5))
bars = ax.bar(["Active", "Left"], [income_compare["No"], income_compare["Yes"]], color=[NAVY, RED], width=0.5)
for b, v in zip(bars, [income_compare["No"], income_compare["Yes"]]):
    ax.text(b.get_x()+b.get_width()/2, v+1500, f"{int(v):,}", ha="center", fontsize=11, fontweight="bold")
ax.set_ylabel("Avg Monthly Income")
ax.set_title("Avg Monthly Income: Active vs Left", fontsize=13)
ax.spines[['top','right']].set_visible(False)
savefig(fig, "05_income_active_vs_left")

# =================================================================
# 6. TENURE ANALYSIS
# =================================================================
def tenure_band(x):
    if x < 1: return "0. <1 yr"
    elif x <= 2: return "1. 1-2 yrs"
    elif x <= 5: return "2. 3-5 yrs"
    elif x <= 10: return "3. 6-10 yrs"
    else: return "4. 10+ yrs"

df["TenureBand"] = df.YearsAtCompany.apply(tenure_band)
tenure_stats = df.groupby("TenureBand").agg(
    headcount=("EmployeeID", "count"),
    attrition_count=("Attrition", lambda x: (x == "Yes").sum())
).reset_index().sort_values("TenureBand")
tenure_stats["attrition_rate"] = round(100 * tenure_stats.attrition_count / tenure_stats.headcount, 2)
tenure_labels = [t.split(". ")[1] for t in tenure_stats.TenureBand]

fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(tenure_labels, tenure_stats.attrition_rate, color=TEAL)
for b, v in zip(bars, tenure_stats.attrition_rate):
    ax.text(b.get_x()+b.get_width()/2, v+0.4, f"{v}%", ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("Attrition Rate (%)")
ax.set_title("Attrition Rate by Tenure Band", fontsize=14)
ax.spines[['top','right']].set_visible(False)
savefig(fig, "06_tenure_attrition")

# Performance rating vs attrition
perf_stats = df.groupby("PerformanceRating").agg(
    headcount=("EmployeeID", "count"),
    attrition_count=("Attrition", lambda x: (x == "Yes").sum()),
    avg_tenure=("YearsAtCompany", "mean")
).reset_index()
perf_stats["attrition_rate"] = round(100*perf_stats.attrition_count/perf_stats.headcount, 2)

fig, ax = plt.subplots(figsize=(5.5, 4.5))
bars = ax.bar(perf_stats.PerformanceRating.astype(str), perf_stats.attrition_rate, color=[GOLD, NAVY])
for b, v in zip(bars, perf_stats.attrition_rate):
    ax.text(b.get_x()+b.get_width()/2, v+0.4, f"{v}%", ha="center", fontsize=11, fontweight="bold")
ax.set_xlabel("Performance Rating")
ax.set_ylabel("Attrition Rate (%)")
ax.set_title("Attrition by Performance Rating", fontsize=13)
ax.spines[['top','right']].set_visible(False)
savefig(fig, "07_performance_attrition")

# =================================================================
# 7. DEMOGRAPHICS
# =================================================================
# Gender
gender_stats = df.groupby("Gender").agg(
    headcount=("EmployeeID", "count"),
    attrition_count=("Attrition", lambda x: (x == "Yes").sum())
).reset_index()
gender_stats["attrition_rate"] = round(100*gender_stats.attrition_count/gender_stats.headcount, 2)

# Age band
def age_band(x):
    if x < 25: return "1. <25"
    elif x < 35: return "2. 25-34"
    elif x < 45: return "3. 35-44"
    elif x < 55: return "4. 45-54"
    else: return "5. 55+"
df["AgeBand"] = df.Age.apply(age_band)
age_stats = df.groupby("AgeBand").agg(
    headcount=("EmployeeID", "count"),
    attrition_count=("Attrition", lambda x: (x == "Yes").sum())
).reset_index().sort_values("AgeBand")
age_stats["attrition_rate"] = round(100*age_stats.attrition_count/age_stats.headcount, 2)
age_labels = [a.split(". ")[1] for a in age_stats.AgeBand]

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].bar(gender_stats.Gender, gender_stats.headcount, color=[NAVY, GOLD])
for i, (h, r) in enumerate(zip(gender_stats.headcount, gender_stats.attrition_rate)):
    axes[0].text(i, h+15, f"n={h}\nattr {r}%", ha="center", fontsize=9)
axes[0].set_title("Gender Distribution & Attrition", fontsize=12)
axes[0].spines[['top','right']].set_visible(False)

axes[1].bar(age_labels, age_stats.headcount, color=TEAL)
for i, (h, r) in enumerate(zip(age_stats.headcount, age_stats.attrition_rate)):
    axes[1].text(i, h+10, f"{r}%", ha="center", fontsize=9, color=RED, fontweight="bold")
axes[1].set_title("Age Band Distribution (attrition % labeled)", fontsize=12)
axes[1].spines[['top','right']].set_visible(False)
savefig(fig, "08_demographics_gender_age")

# Marital status
marital_stats = df.groupby("MaritalStatus").agg(
    headcount=("EmployeeID", "count"),
    attrition_count=("Attrition", lambda x: (x == "Yes").sum())
).reset_index()
marital_stats["attrition_rate"] = round(100*marital_stats.attrition_count/marital_stats.headcount, 2)

fig, ax = plt.subplots(figsize=(6, 4.5))
bars = ax.bar(marital_stats.MaritalStatus, marital_stats.attrition_rate, color=[NAVY, GOLD, RED])
for b, v in zip(bars, marital_stats.attrition_rate):
    ax.text(b.get_x()+b.get_width()/2, v+0.3, f"{v}%", ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("Attrition Rate (%)")
ax.set_title("Attrition by Marital Status", fontsize=13)
ax.spines[['top','right']].set_visible(False)
savefig(fig, "09_marital_status_attrition")

# =================================================================
# 8. OVERTIME & WORK-LIFE BALANCE (key drivers)
# =================================================================
ot_stats = df.groupby("OverTime").agg(
    headcount=("EmployeeID", "count"),
    attrition_count=("Attrition", lambda x: (x == "Yes").sum())
).reset_index()
ot_stats["attrition_rate"] = round(100*ot_stats.attrition_count/ot_stats.headcount, 2)

wlb_stats = df.groupby("WorkLifeBalance").agg(
    headcount=("EmployeeID", "count"),
    attrition_count=("Attrition", lambda x: (x == "Yes").sum())
).reset_index().sort_values("WorkLifeBalance")
wlb_stats["attrition_rate"] = round(100*wlb_stats.attrition_count/wlb_stats.headcount, 2)
wlb_map = {1: "1-Bad", 2: "2-Fair", 3: "3-Good", 4: "4-Excellent"}
wlb_stats["label"] = wlb_stats.WorkLifeBalance.map(wlb_map)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
bars0 = axes[0].bar(ot_stats.OverTime, ot_stats.attrition_rate, color=[NAVY, RED])
for b, v in zip(bars0, ot_stats.attrition_rate):
    axes[0].text(b.get_x()+b.get_width()/2, v+0.5, f"{v}%", ha="center", fontsize=11, fontweight="bold")
axes[0].set_title("Attrition by OverTime Status", fontsize=12)
axes[0].set_ylabel("Attrition Rate (%)")
axes[0].spines[['top','right']].set_visible(False)

bars1 = axes[1].bar(wlb_stats.label, wlb_stats.attrition_rate, color=GOLD)
for b, v in zip(bars1, wlb_stats.attrition_rate):
    axes[1].text(b.get_x()+b.get_width()/2, v+0.5, f"{v}%", ha="center", fontsize=10, fontweight="bold")
axes[1].set_title("Attrition by Work-Life Balance", fontsize=12)
axes[1].spines[['top','right']].set_visible(False)
savefig(fig, "10_overtime_wlb_attrition")

# =================================================================
# 9. CORRELATION HEATMAP (numeric drivers)
# =================================================================
num_cols = ["Age","MonthlyIncome","DistanceFromHome","TotalWorkingYears","YearsAtCompany",
            "YearsInCurrentRole","YearsSinceLastPromotion","NumCompaniesWorked",
            "JobSatisfaction","EnvironmentSatisfaction","WorkLifeBalance","JobInvolvement",
            "PerformanceRating"]
corr_df = df[num_cols].copy()
corr_df["Attrition"] = (df.Attrition == "Yes").astype(int)
corr = corr_df.corr()["Attrition"].drop("Attrition").sort_values()

fig, ax = plt.subplots(figsize=(7, 6))
colors_bar = [RED if v > 0 else NAVY for v in corr.values]
bars = ax.barh(corr.index, corr.values, color=colors_bar)
ax.axvline(0, color="#333", linewidth=0.8)
ax.set_title("Correlation with Attrition (numeric features)", fontsize=13)
ax.spines[['top','right']].set_visible(False)
savefig(fig, "11_correlation_attrition")

print("\nAll charts saved to:", CHARTS)

# =================================================================
# EXPORT SUMMARY TABLES (used in PDF + dashboard)
# =================================================================
summary = {
    "total_employees": total_emp,
    "attrition_count": int(attrition_count),
    "active_employees": int(active_emp),
    "attrition_rate": attrition_rate,
    "avg_income": int(avg_income),
    "avg_tenure": avg_tenure,
    "avg_age": avg_age,
}
import json
with open("/home/claude/hr_project/data/summary_kpis.json", "w") as f:
    json.dump(summary, f, indent=2)

dept_stats.to_csv("/home/claude/hr_project/data/dept_stats.csv", index=False)
role_stats.to_csv("/home/claude/hr_project/data/role_stats.csv", index=False)
salary_stats.to_csv("/home/claude/hr_project/data/salary_stats.csv", index=False)
tenure_stats.to_csv("/home/claude/hr_project/data/tenure_stats.csv", index=False)
perf_stats.to_csv("/home/claude/hr_project/data/perf_stats.csv", index=False)
gender_stats.to_csv("/home/claude/hr_project/data/gender_stats.csv", index=False)
age_stats.to_csv("/home/claude/hr_project/data/age_stats.csv", index=False)
marital_stats.to_csv("/home/claude/hr_project/data/marital_stats.csv", index=False)
ot_stats.to_csv("/home/claude/hr_project/data/ot_stats.csv", index=False)
wlb_stats.to_csv("/home/claude/hr_project/data/wlb_stats.csv", index=False)

print("\nSummary KPIs:", summary)
