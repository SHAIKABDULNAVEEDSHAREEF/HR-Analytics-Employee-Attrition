/* ============================================================================
   HR ANALYTICS & EMPLOYEE ATTRITION -- SQL ANALYSIS
   Author : Shaik Abdul Naveed Shareef
   Table  : hr_employee_attrition  (loaded from hr_employee_attrition.csv)
   Engine : Written for MySQL / PostgreSQL syntax (minor tweaks for SQL Server)
   ============================================================================ */

-- ------------------------------------------------------------------
-- 0. TABLE CREATION
-- ------------------------------------------------------------------
CREATE TABLE hr_employee_attrition (
    EmployeeID              INT PRIMARY KEY,
    Age                     INT,
    Gender                  VARCHAR(10),
    MaritalStatus           VARCHAR(15),
    Department              VARCHAR(40),
    JobRole                 VARCHAR(40),
    JobLevel                INT,
    Education               INT,
    EducationField           VARCHAR(30),
    DistanceFromHome        INT,
    MonthlyIncome           INT,
    PercentSalaryHike       INT,
    StockOptionLevel        INT,
    TotalWorkingYears       INT,
    YearsAtCompany          INT,
    YearsInCurrentRole      INT,
    YearsSinceLastPromotion INT,
    NumCompaniesWorked      INT,
    TrainingTimesLastYear   INT,
    OverTime                VARCHAR(5),
    BusinessTravel          VARCHAR(20),
    JobSatisfaction         INT,
    EnvironmentSatisfaction INT,
    WorkLifeBalance         INT,
    JobInvolvement          INT,
    RelationshipSatisfaction INT,
    PerformanceRating       INT,
    Attrition               VARCHAR(3)
);

-- ------------------------------------------------------------------
-- 1. OVERALL ATTRITION RATE
-- ------------------------------------------------------------------
SELECT
    COUNT(*)                                              AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)    AS employees_left,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employee_attrition;

-- ------------------------------------------------------------------
-- 2. DEPARTMENT-WISE ATTRITION
-- ------------------------------------------------------------------
SELECT
    Department,
    COUNT(*)                                                       AS headcount,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)             AS attrition_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct,
    ROUND(AVG(MonthlyIncome), 0)                                   AS avg_monthly_income
FROM hr_employee_attrition
GROUP BY Department
ORDER BY attrition_rate_pct DESC;

-- ------------------------------------------------------------------
-- 3. JOB ROLE ATTRITION (top risk roles)
-- ------------------------------------------------------------------
SELECT
    Department,
    JobRole,
    COUNT(*)                                                       AS headcount,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employee_attrition
GROUP BY Department, JobRole
HAVING COUNT(*) >= 15
ORDER BY attrition_rate_pct DESC
LIMIT 10;

-- ------------------------------------------------------------------
-- 4. SALARY ANALYSIS -- income bands vs attrition
-- ------------------------------------------------------------------
SELECT
    CASE
        WHEN MonthlyIncome < 30000 THEN '1. Below 30K'
        WHEN MonthlyIncome BETWEEN 30000 AND 49999 THEN '2. 30K-50K'
        WHEN MonthlyIncome BETWEEN 50000 AND 79999 THEN '3. 50K-80K'
        WHEN MonthlyIncome BETWEEN 80000 AND 119999 THEN '4. 80K-120K'
        ELSE '5. 120K+'
    END                                                             AS salary_band,
    COUNT(*)                                                        AS headcount,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employee_attrition
GROUP BY salary_band
ORDER BY salary_band;

-- Average salary: stayed vs left, by department
SELECT
    Department,
    Attrition,
    ROUND(AVG(MonthlyIncome), 0)   AS avg_monthly_income,
    COUNT(*)                        AS headcount
FROM hr_employee_attrition
GROUP BY Department, Attrition
ORDER BY Department, Attrition;

-- ------------------------------------------------------------------
-- 5. TENURE ANALYSIS
-- ------------------------------------------------------------------
SELECT
    CASE
        WHEN YearsAtCompany < 1  THEN '0. < 1 yr'
        WHEN YearsAtCompany BETWEEN 1 AND 2  THEN '1. 1-2 yrs'
        WHEN YearsAtCompany BETWEEN 3 AND 5  THEN '2. 3-5 yrs'
        WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '3. 6-10 yrs'
        ELSE '4. 10+ yrs'
    END                                                             AS tenure_band,
    COUNT(*)                                                        AS headcount,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employee_attrition
GROUP BY tenure_band
ORDER BY tenure_band;

-- ------------------------------------------------------------------
-- 6. PERFORMANCE RATING vs ATTRITION
-- ------------------------------------------------------------------
SELECT
    PerformanceRating,
    COUNT(*)                                                        AS headcount,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct,
    ROUND(AVG(YearsAtCompany), 1)                                   AS avg_tenure_years
FROM hr_employee_attrition
GROUP BY PerformanceRating;

-- ------------------------------------------------------------------
-- 7. EMPLOYEE DEMOGRAPHICS
-- ------------------------------------------------------------------
-- Gender split
SELECT Gender, COUNT(*) AS headcount,
       ROUND(100.0 * SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate_pct
FROM hr_employee_attrition GROUP BY Gender;

-- Age band split
SELECT
    CASE
        WHEN Age < 25 THEN '1. <25'
        WHEN Age BETWEEN 25 AND 34 THEN '2. 25-34'
        WHEN Age BETWEEN 35 AND 44 THEN '3. 35-44'
        WHEN Age BETWEEN 45 AND 54 THEN '4. 45-54'
        ELSE '5. 55+'
    END AS age_band,
    COUNT(*) AS headcount,
    ROUND(100.0 * SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate_pct
FROM hr_employee_attrition
GROUP BY age_band
ORDER BY age_band;

-- Marital status split
SELECT MaritalStatus, COUNT(*) AS headcount,
       ROUND(100.0 * SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate_pct
FROM hr_employee_attrition GROUP BY MaritalStatus;

-- ------------------------------------------------------------------
-- 8. WORK-LIFE / OVERTIME DRIVERS OF ATTRITION
-- ------------------------------------------------------------------
SELECT
    OverTime,
    COUNT(*)                                                        AS headcount,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employee_attrition
GROUP BY OverTime;

SELECT
    WorkLifeBalance,
    COUNT(*)                                                        AS headcount,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employee_attrition
GROUP BY WorkLifeBalance
ORDER BY WorkLifeBalance;

-- ------------------------------------------------------------------
-- 9. TOP RETENTION-RISK SEGMENT (window function example)
-- ------------------------------------------------------------------
SELECT * FROM (
    SELECT
        Department, JobRole,
        COUNT(*) AS headcount,
        ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate_pct,
        RANK() OVER (ORDER BY 100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*) DESC) AS risk_rank
    FROM hr_employee_attrition
    GROUP BY Department, JobRole
    HAVING COUNT(*) >= 15
) ranked
WHERE risk_rank <= 5;
