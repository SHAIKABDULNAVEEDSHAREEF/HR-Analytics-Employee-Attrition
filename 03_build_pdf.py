"""
Builds the end-to-end HR Analytics & Employee Attrition project PDF report,
suitable for uploading to GitHub as project documentation.
"""

import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas as pdfcanvas

BASE = "/home/claude/hr_project"
CHARTS = f"{BASE}/charts"
DASH = f"{BASE}/dashboard"
OUT = f"{BASE}/outputs/HR_Analytics_Employee_Attrition_Project_Report.pdf"

NAVY = colors.HexColor("#12294B")
DARKNAVY = colors.HexColor("#0B1220")
GOLD = colors.HexColor("#C9A227")
TEAL = colors.HexColor("#1F7A6C")
RED = colors.HexColor("#B5443B")
LIGHTGREY = colors.HexColor("#F4F5F7")
TEXT = colors.HexColor("#20242C")
MUTED = colors.HexColor("#5B6472")

kpis = json.load(open(f"{BASE}/data/summary_kpis.json"))

# ------------------------------------------------------------------
# STYLES
# ------------------------------------------------------------------
styles = getSampleStyleSheet()

styles.add(ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=18, leading=22,
                           textColor=NAVY, spaceBefore=6, spaceAfter=10))
styles.add(ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=13, leading=16,
                           textColor=NAVY, spaceBefore=14, spaceAfter=6))
styles.add(ParagraphStyle("H3", fontName="Helvetica-Bold", fontSize=11, leading=14,
                           textColor=colors.HexColor("#8A6D00"), spaceBefore=8, spaceAfter=4))
styles.add(ParagraphStyle("Body", fontName="Helvetica", fontSize=9.7, leading=14.5,
                           textColor=TEXT, alignment=TA_JUSTIFY, spaceAfter=6))
styles.add(ParagraphStyle("BulletItem", fontName="Helvetica", fontSize=9.7, leading=14.5,
                           textColor=TEXT, leftIndent=12, spaceAfter=3))
styles.add(ParagraphStyle("Caption", fontName="Helvetica-Oblique", fontSize=8.3, leading=11,
                           textColor=MUTED, alignment=TA_CENTER, spaceBefore=3, spaceAfter=10))
styles.add(ParagraphStyle("KPI", fontName="Helvetica-Bold", fontSize=16, leading=18,
                           textColor=NAVY, alignment=TA_CENTER))
styles.add(ParagraphStyle("KPILabel", fontName="Helvetica", fontSize=8, leading=10,
                           textColor=MUTED, alignment=TA_CENTER))
styles.add(ParagraphStyle("CodeBlock", fontName="Courier", fontSize=7.6, leading=10.4,
                           textColor=colors.HexColor("#0B1220"), backColor=colors.HexColor("#F1F0E9"),
                           borderPadding=6, spaceAfter=8))

# ------------------------------------------------------------------
# COVER PAGE
# ------------------------------------------------------------------
def draw_cover(c, doc):
    c.saveState()
    w, h = A4
    c.setFillColor(DARKNAVY)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    # gold accent line
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(25*mm, h-55*mm, w-25*mm, h-55*mm)

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(25*mm, h-42*mm, "PORTFOLIO PROJECT  |  DATA ANALYTICS & BUSINESS INTELLIGENCE")

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 27)
    c.drawString(25*mm, h-70*mm, "HR Analytics &")
    c.setFillColor(GOLD)
    c.drawString(25*mm, h-80*mm, "Employee Attrition")

    c.setFillColor(colors.HexColor("#C7CDDB"))
    c.setFont("Helvetica", 11.5)
    c.drawString(25*mm, h-92*mm, "An End-to-End Analytics Project using SQL, Python (EDA) and Power BI")
    c.drawString(25*mm, h-99*mm, "to identify, quantify and explain workforce attrition drivers.")

    # tech stack chips
    chips = ["SQL", "Python", "Pandas", "Matplotlib", "Power BI", "EDA"]
    x = 25*mm
    y = h-115*mm
    c.setFont("Helvetica-Bold", 8.5)
    for chip in chips:
        cw = c.stringWidth(chip, "Helvetica-Bold", 8.5) + 14
        c.setFillColor(NAVY)
        c.roundRect(x, y, cw, 8*mm, 4, fill=1, stroke=1)
        c.setStrokeColor(GOLD)
        c.setFillColor(colors.white)
        c.drawString(x+7, y+2.8*mm, chip)
        x += cw + 6

    # KPI strip
    kx = 25*mm
    ky = h-145*mm
    kpi_items = [
        (f"{kpis['total_employees']:,}", "Employees Analyzed"),
        (f"{kpis['attrition_rate']}%", "Attrition Rate"),
        (f"Rs {kpis['avg_income']:,}", "Avg Monthly Income"),
        (f"{kpis['avg_tenure']} yrs", "Avg Tenure"),
    ]
    box_w = (w - 50*mm - 3*8) / 4
    for i, (val, label) in enumerate(kpi_items):
        bx = kx + i*(box_w+8)
        c.setFillColor(NAVY)
        c.roundRect(bx, ky, box_w, 22*mm, 4, fill=1, stroke=0)
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.roundRect(bx, ky, box_w, 22*mm, 4, fill=0, stroke=1)
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(bx+box_w/2, ky+13*mm, val)
        c.setFillColor(colors.HexColor("#AEB6C7"))
        c.setFont("Helvetica", 7.3)
        c.drawCentredString(bx+box_w/2, ky+5*mm, label)

    # footer / author block
    c.setStrokeColor(colors.HexColor("#26324D"))
    c.setLineWidth(0.8)
    c.line(25*mm, 32*mm, w-25*mm, 32*mm)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(25*mm, 24*mm, "Shaik Abdul Naveed Shareef")
    c.setFillColor(colors.HexColor("#AEB6C7"))
    c.setFont("Helvetica", 8.5)
    c.drawString(25*mm, 19.5*mm, "Aspiring Data Analyst | Data Analytics & AI (AnalytixLabs)")
    c.drawString(25*mm, 15*mm, "GitHub: github.com/SHAIKABDULNAVEEDSHAREEF   |   LinkedIn: linkedin.com/in/shaik-naveed-514895268")
    c.restoreState()

# ------------------------------------------------------------------
# HEADER / FOOTER FOR CONTENT PAGES
# ------------------------------------------------------------------
def header_footer(c, doc):
    c.saveState()
    w, h = A4
    c.setFillColor(NAVY)
    c.rect(0, h-16*mm, w, 16*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20*mm, h-10.5*mm, "HR Analytics & Employee Attrition")
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 8.5)
    c.drawRightString(w-20*mm, h-10.5*mm, "SQL  \u2022  Python  \u2022  Power BI")

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(20*mm, 12*mm, "Shaik Abdul Naveed Shareef  |  Data Analytics Portfolio Project")
    c.setFont("Helvetica", 8)
    c.drawRightString(w-20*mm, 12*mm, f"Page {doc.page - 1}")
    c.setStrokeColor(colors.HexColor("#E4E4E4"))
    c.line(20*mm, 15*mm, w-20*mm, 15*mm)
    c.restoreState()

def on_first_page(c, doc):
    draw_cover(c, doc)

def on_later_pages(c, doc):
    header_footer(c, doc)

# ------------------------------------------------------------------
# HELPER
# ------------------------------------------------------------------
def img(path, width=160*mm, caption=None):
    from PIL import Image as PILImage
    iw, ih = PILImage.open(path).size
    ratio = ih / iw
    elems = [Image(path, width=width, height=width*ratio)]
    if caption:
        elems.append(Paragraph(caption, styles["Caption"]))
    return elems

def kpi_row(items):
    """items: list of (value, label)"""
    cells = []
    for val, label in items:
        cell = [Paragraph(val, styles["KPI"]), Paragraph(label, styles["KPILabel"])]
        cells.append(cell)
    t = Table([cells], colWidths=[170*mm/len(items)]*len(items))
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHTGREY),
        ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#DADFE6")),
        ("INNERGRID", (0,0), (-1,-1), 0.5, colors.HexColor("#DADFE6")),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    return t

def bullets(items):
    return [Paragraph(f"&#8226;&nbsp; {i}", styles["BulletItem"]) for i in items]

def section_rule():
    return HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceBefore=2, spaceAfter=10)

cell_style = ParagraphStyle("Cell", fontName="Helvetica", fontSize=8.4, leading=11.5, textColor=TEXT)
cell_style_b = ParagraphStyle("CellB", fontName="Helvetica-Bold", fontSize=8.4, leading=11.5, textColor=TEXT)
head_style = ParagraphStyle("Head", fontName="Helvetica-Bold", fontSize=8.6, leading=11.5, textColor=colors.white)

def P(text, bold=False):
    return Paragraph(text, cell_style_b if bold else cell_style)

def H(text):
    return Paragraph(text, head_style)

# ------------------------------------------------------------------
# BUILD STORY
# ------------------------------------------------------------------
story = []
story.append(PageBreak())

# ---- PAGE: Project Overview ----
story.append(Paragraph("1.&nbsp; Project Overview", styles["H1"]))
story.append(section_rule())
story.append(Paragraph(
    "Employee attrition is one of the costliest and most preventable problems an organization faces: "
    "replacing a departing employee typically costs 50-200% of their annual salary once recruiting, "
    "onboarding and lost productivity are accounted for. This project builds a complete, reproducible "
    "analytics pipeline &mdash; from raw HR records to an executive-ready Power BI dashboard &mdash; to answer four "
    "questions HR and business leaders repeatedly ask:", styles["Body"]))
story.append(Paragraph("", styles["Body"]))
story.extend(bullets([
    "What is our overall attrition rate, and is it within a healthy range?",
    "Which departments, job roles and salary bands are bleeding talent fastest?",
    "Does tenure or performance meaningfully predict who leaves?",
    "What employee-level factors (overtime, work-life balance, marital status, distance from home) "
    "correlate most strongly with exits?",
]))

story.append(Paragraph("1.1&nbsp; Objectives", styles["H2"]))
story.extend(bullets([
    "Calculate and segment the company-wide attrition rate across department, role, tenure and salary.",
    "Use SQL to structure and aggregate raw HR data into analysis-ready summary tables.",
    "Perform exploratory data analysis (EDA) in Python to quantify every relationship precisely, not just visually.",
    "Design a clean, two-page Power BI-style executive dashboard for non-technical stakeholders.",
    "Translate findings into specific, actionable HR retention recommendations.",
]))

story.append(Paragraph("1.2&nbsp; Tech Stack", styles["H2"]))
tech_table = Table([
    [H("Layer"), H("Tool(s)"), H("Purpose")],
    [P("Data Storage & Querying", True), P("SQL (MySQL / PostgreSQL syntax)"), P("Table design, aggregation, window functions, ranking queries")],
    [P("Data Analysis (EDA)", True), P("Python \u2013 pandas, NumPy, Matplotlib"), P("Cleaning, segmentation, statistical summaries, correlation analysis")],
    [P("Visualization / Dashboard", True), P("Power BI (dashboard design replicated for this report)"), P("Executive KPI cards, interactive-style visuals, 2-page report")],
    [P("Documentation", True), P("Python \u2013 ReportLab"), P("This end-to-end PDF project report")],
], colWidths=[38*mm, 56*mm, 76*mm])
tech_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), NAVY),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#DADFE6")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHTGREY]),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
]))
story.append(tech_table)

story.append(PageBreak())

# ---- PAGE: Dataset Description ----
story.append(Paragraph("2.&nbsp; Dataset Description", styles["H1"]))
story.append(section_rule())
story.append(Paragraph(
    "The analysis uses a structured HR dataset of <b>1,500 employees</b> across 5 departments, "
    "modeled on real-world HR analytics schemas (in the style of IBM's well-known HR Attrition dataset). "
    "Attrition outcomes were generated using a probability model driven by realistic business factors "
    "&mdash; overtime, satisfaction scores, tenure, income, travel frequency and job level &mdash; so that "
    "relationships in the data mirror genuine workplace attrition patterns.", styles["Body"]))

story.append(Paragraph("2.1&nbsp; Schema (28 columns)", styles["H2"]))
schema_table = Table([
    [H("Category"), H("Fields")],
    [P("Identifiers", True), P("EmployeeID")],
    [P("Demographics", True), P("Age, Gender, MaritalStatus, Education, EducationField, DistanceFromHome")],
    [P("Job Info", True), P("Department, JobRole, JobLevel, BusinessTravel")],
    [P("Compensation", True), P("MonthlyIncome, PercentSalaryHike, StockOptionLevel")],
    [P("Tenure & Experience", True), P("TotalWorkingYears, YearsAtCompany, YearsInCurrentRole, YearsSinceLastPromotion, NumCompaniesWorked, TrainingTimesLastYear")],
    [P("Satisfaction & Performance", True), P("JobSatisfaction, EnvironmentSatisfaction, WorkLifeBalance, JobInvolvement, RelationshipSatisfaction, PerformanceRating")],
    [P("Work Pattern", True), P("OverTime")],
    [P("Target Variable", True), P("Attrition (Yes / No)")],
], colWidths=[40*mm, 130*mm])
schema_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), NAVY),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#DADFE6")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHTGREY]),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
]))
story.append(schema_table)

story.append(Paragraph("2.2&nbsp; Data Quality Checks", styles["H2"]))
story.extend(bullets([
    "Rows: 1,500  |  Columns: 28  |  Missing values: 0  |  Duplicate rows: 0",
    "All categorical fields validated against an expected value set (e.g. Attrition &isin; {Yes, No}).",
    "Numeric fields range-checked (e.g. Age 18-60, JobSatisfaction 1-4, MonthlyIncome &gt; 0).",
]))

story.append(Paragraph("2.3&nbsp; SQL Layer", styles["H2"]))
story.append(Paragraph(
    "A dedicated SQL script (<b>hr_attrition_analysis.sql</b>, included in the GitHub repo) creates the table "
    "schema and answers each business question using CASE-based segmentation, GROUP BY aggregation and a "
    "window-function ranking query to surface the top 5 highest-risk role/department combinations. Sample:",
    styles["Body"]))
story.append(Paragraph(
    "SELECT Department, COUNT(*) AS headcount,<br/>"
    "&nbsp;&nbsp;ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate_pct<br/>"
    "FROM hr_employee_attrition<br/>"
    "GROUP BY Department<br/>"
    "ORDER BY attrition_rate_pct DESC;",
    styles["CodeBlock"]))

story.append(PageBreak())

# ---- PAGE: EDA - Overview ----
story.append(Paragraph("3.&nbsp; Exploratory Data Analysis (EDA)", styles["H1"]))
story.append(section_rule())
story.append(Paragraph("3.1&nbsp; Headline Numbers", styles["H2"]))
story.append(kpi_row([
    (f"{kpis['total_employees']:,}", "Total Employees"),
    (f"{kpis['attrition_count']}", "Employees Who Left"),
    (f"{kpis['attrition_rate']}%", "Attrition Rate"),
    (f"{100-kpis['attrition_rate']:.2f}%", "Retention Rate"),
]))
story.append(Spacer(1, 8))
story.append(kpi_row([
    (f"Rs {kpis['avg_income']:,}", "Avg Monthly Income"),
    (f"{kpis['avg_tenure']} yrs", "Avg Tenure"),
    (f"{kpis['avg_age']} yrs", "Avg Age"),
    ("0", "Missing Values"),
]))
story.append(Spacer(1, 10))
story.append(Paragraph(
    f"Out of 1,500 employees, <b>{kpis['attrition_count']} ({kpis['attrition_rate']}%)</b> left the organization "
    "&mdash; a moderate attrition level, but concentrated sharply in specific segments explored below.",
    styles["Body"]))
story.extend(img(f"{CHARTS}/01_overall_attrition_donut.png", width=90*mm,
                  caption="Fig 3.1 &mdash; Overall attrition split (Active vs Left)"))

story.append(Paragraph("3.2&nbsp; Department-Wise Analysis", styles["H2"]))
story.extend(img(f"{CHARTS}/02_department_attrition.png", width=155*mm,
                  caption="Fig 3.2 &mdash; Attrition rate by department (headcount labeled)"))
story.append(Paragraph(
    "<b>Sales (19.82%)</b> has the highest attrition rate of any department, nearly 3.4 points above "
    "Finance and HR (~16.5%). Research &amp; Development, the largest department by headcount (569 employees), "
    "sits close to the company average at 17.57%.", styles["Body"]))

story.append(PageBreak())

story.append(Paragraph("3.3&nbsp; Job Role Risk", styles["H2"]))
story.extend(img(f"{CHARTS}/03_jobrole_attrition.png", width=155*mm,
                  caption="Fig 3.3 &mdash; Top job roles by attrition risk (roles with n\u226515)"))
story.append(Paragraph(
    "HR Executive, Sales Representative and Research Scientist are the three highest-risk individual "
    "roles, each above 21% attrition &mdash; well above the 17.93% company average.", styles["Body"]))

story.append(Paragraph("3.4&nbsp; Salary Analysis", styles["H2"]))
story.extend(img(f"{CHARTS}/04_salary_band_attrition.png", width=155*mm,
                  caption="Fig 3.4 &mdash; Salary band: headcount vs attrition rate"))
story.append(Paragraph(
    "Attrition drops sharply as salary rises: employees earning under Rs 30,000/month leave at "
    "<b>21.59%</b>, versus just <b>3.33%</b> for the Rs 120,000+ band &mdash; a clear, almost linear "
    "relationship between compensation and retention.", styles["Body"]))
story.extend(img(f"{CHARTS}/05_income_active_vs_left.png", width=90*mm,
                  caption="Fig 3.5 &mdash; Average monthly income: employees who stayed vs left"))

story.append(PageBreak())

story.append(Paragraph("3.5&nbsp; Tenure &amp; Performance Analysis", styles["H2"]))
story.extend(img(f"{CHARTS}/06_tenure_attrition.png", width=155*mm,
                  caption="Fig 3.6 &mdash; Attrition rate by tenure band"))
story.append(Paragraph(
    "Attrition is heavily front-loaded: employees in their <b>first year</b> leave at <b>23.28%</b>, "
    "nearly 4x the rate of employees with 10+ years of tenure (6.06%). Risk stays elevated (22.49%) through "
    "year two, then falls steadily as tenure increases &mdash; a classic early-career flight-risk curve.",
    styles["Body"]))
story.extend(img(f"{CHARTS}/07_performance_attrition.png", width=90*mm,
                  caption="Fig 3.7 &mdash; Attrition by performance rating"))
story.append(Paragraph(
    "Interestingly, top performers (rating 4) show a marginally <i>higher</i> attrition rate (19.27%) than "
    "average performers (17.71%) &mdash; a common warning sign that high performers are being poached or are "
    "leaving for better opportunities elsewhere.", styles["Body"]))

story.append(PageBreak())

story.append(Paragraph("3.6&nbsp; Employee Demographics", styles["H2"]))
story.extend(img(f"{CHARTS}/08_demographics_gender_age.png", width=155*mm,
                  caption="Fig 3.8 &mdash; Gender split and age-band distribution (attrition % labeled)"))
story.extend(img(f"{CHARTS}/09_marital_status_attrition.png", width=90*mm,
                  caption="Fig 3.9 &mdash; Attrition by marital status"))
story.append(Paragraph(
    "The under-25 age band shows the highest attrition (30.86%), consistent with the tenure finding: "
    "younger, newer employees are the highest flight risk. Single employees also churn more (18.79%) than "
    "married employees (17.76%).", styles["Body"]))

story.append(Paragraph("3.7&nbsp; Work-Life Drivers &amp; Correlation", styles["H2"]))
story.extend(img(f"{CHARTS}/10_overtime_wlb_attrition.png", width=155*mm,
                  caption="Fig 3.10 &mdash; Attrition by overtime status and work-life balance rating"))
story.append(Paragraph(
    "<b>Overtime is the single strongest behavioral driver:</b> employees who work overtime leave at "
    "<b>27.46%</b> &mdash; nearly double the 13.88% rate for those who don't. Work-life balance shows the "
    "same pattern: employees rating it \u2018Bad\u2019 (1) leave at 24.18% vs 16.47% for those rating it \u2018Excellent\u2019 (4).",
    styles["Body"]))
story.extend(img(f"{CHARTS}/11_correlation_attrition.png", width=110*mm,
                  caption="Fig 3.11 &mdash; Pearson correlation of numeric features with attrition"))
story.append(Paragraph(
    "Tenure-related fields (YearsAtCompany, TotalWorkingYears, JobSatisfaction) show the strongest negative "
    "correlation with attrition, while NumCompaniesWorked shows the strongest positive correlation &mdash; "
    "employees with a history of frequent job-hopping are more likely to leave again.", styles["Body"]))

story.append(PageBreak())

# ---- PAGE: Power BI Dashboard ----
story.append(Paragraph("4.&nbsp; Power BI Dashboard", styles["H1"]))
story.append(section_rule())
story.append(Paragraph(
    "The findings above are consolidated into a clean, 2-page executive Power BI dashboard using a "
    "navy-and-gold \u201cMidnight Executive\u201d design system for visual consistency with the rest of the "
    "portfolio. Page 1 gives leadership an at-a-glance overview; Page 2 supports HR teams with root-cause "
    "detail for retention planning.", styles["Body"]))
story.extend(img(f"{DASH}/dashboard_page1.png", width=170*mm,
                  caption="Fig 4.1 &mdash; Dashboard Page 1: Executive Overview"))
story.append(PageBreak())
story.extend(img(f"{DASH}/dashboard_page2.png", width=170*mm,
                  caption="Fig 4.2 &mdash; Dashboard Page 2: Attrition Deep-Dive"))

story.append(Paragraph("4.1&nbsp; Dashboard Design Notes", styles["H2"]))
story.extend(bullets([
    "5 KPI cards give an instant executive summary: headcount, attrition rate, active headcount, average income, average tenure.",
    "Page 1 (Overview) answers \u2018what is happening\u2019: overall split, department comparison, tenure and salary trends, demographics.",
    "Page 2 (Deep-Dive) answers \u2018why it's happening\u2019: role-level risk, overtime/work-life balance impact, and a correlation ranking of every numeric driver.",
    "An insight callout banner on Page 2 translates the correlation analysis into one plain-English takeaway for non-technical stakeholders.",
])) 

story.append(PageBreak())

# ---- PAGE: Insights & Recommendations ----
story.append(Paragraph("5.&nbsp; Key Insights &amp; Recommendations", styles["H1"]))
story.append(section_rule())

insight_rows_raw = [
    ["1", "Overtime employees churn at 27.46% vs 13.88% for non-overtime staff \u2014 the single strongest behavioral driver.",
     "Audit overtime load by team; cap sustained overtime and introduce compensatory time-off for high-overtime roles."],
    ["2", "First-year employees leave at 23.28%, more than double the rate of 10+ year veterans (6.06%).",
     "Strengthen onboarding and a structured 90-day / 12-month check-in program with a named mentor."],
    ["3", "Attrition falls sharply as salary rises (21.6% below Rs30K vs 3.3% above Rs120K).",
     "Benchmark entry-level and Sales compensation against market rate; review pay-for-tenure structures."],
    ["4", "Sales dept. and HR Executive / Sales Rep / Research Scientist roles show the highest role-level risk.",
     "Run targeted stay interviews and role-specific retention plans for these segments."],
    ["5", "Top performers (rating 4) attrite slightly more than average performers.",
     "Build a distinct high-performer retention track: accelerated promotion cycles, stretch projects, recognition."],
    ["6", "Low work-life balance and frequent past job-changes both correlate with higher attrition.",
     "Monitor NumCompaniesWorked and WorkLifeBalance scores as early-warning flags in HR systems."],
]
insight_data = [[H("#"), H("Insight"), H("Recommendation")]]
for n, ins, rec in insight_rows_raw:
    insight_data.append([P(n, True), P(ins), P(rec)])

insight_table = Table(insight_data, colWidths=[8*mm, 84*mm, 78*mm])
insight_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), NAVY),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#DADFE6")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHTGREY]),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("ALIGN", (0,0), (0,-1), "CENTER"),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
]))
story.append(insight_table)

story.append(Paragraph("6.&nbsp; Conclusion", styles["H1"]))
story.append(section_rule())
story.append(Paragraph(
    "This project demonstrates a full analytics workflow: structuring and querying HR data in SQL, "
    "quantifying every relationship with Python-based EDA rather than relying on visuals alone, and "
    "translating the results into an executive-ready Power BI-style dashboard with clear, prioritized "
    "recommendations. The overall attrition rate of 17.93% is not evenly distributed &mdash; it is "
    "concentrated in early-tenure, overtime-heavy, lower-salary Sales and support roles, giving HR "
    "leadership a specific, evidence-based starting point for retention interventions rather than a "
    "generic company-wide policy change.", styles["Body"]))

story.append(Paragraph("6.1&nbsp; Repository Structure", styles["H2"]))
story.append(Paragraph(
    "hr-analytics-employee-attrition/<br/>"
    "&nbsp;&nbsp;├── data/hr_employee_attrition.csv&nbsp;&nbsp;&mdash;&nbsp;raw dataset<br/>"
    "&nbsp;&nbsp;├── sql/hr_attrition_analysis.sql&nbsp;&nbsp;&mdash;&nbsp;SQL analysis queries<br/>"
    "&nbsp;&nbsp;├── python/01_generate_data.py&nbsp;&nbsp;&mdash;&nbsp;dataset generation<br/>"
    "&nbsp;&nbsp;├── python/02_eda_analysis.py&nbsp;&nbsp;&mdash;&nbsp;EDA + chart generation<br/>"
    "&nbsp;&nbsp;├── dashboard/&nbsp;&nbsp;&mdash;&nbsp;Power BI-style dashboard pages<br/>"
    "&nbsp;&nbsp;└── HR_Analytics_Employee_Attrition_Project_Report.pdf&nbsp;&nbsp;&mdash;&nbsp;this report",
    styles["CodeBlock"]))

story.append(Paragraph("6.2&nbsp; Links", styles["H2"]))
story.append(Paragraph(
    'GitHub: <link href="https://github.com/SHAIKABDULNAVEEDSHAREEF" color="#12294B">github.com/SHAIKABDULNAVEEDSHAREEF</link><br/>'
    'LinkedIn: <link href="https://linkedin.com/in/shaik-naveed-514895268" color="#12294B">linkedin.com/in/shaik-naveed-514895268</link><br/>'
    'Email: shaikabdulnaveedshareff@gmail.com',
    styles["Body"]))

# ------------------------------------------------------------------
doc = SimpleDocTemplate(OUT, pagesize=A4,
                         leftMargin=20*mm, rightMargin=20*mm,
                         topMargin=22*mm, bottomMargin=18*mm,
                         title="HR Analytics & Employee Attrition - Project Report",
                         author="Shaik Abdul Naveed Shareef")
doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
print("PDF built:", OUT)
