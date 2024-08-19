WITH department_medians AS (
    SELECT 
        department, 
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY wage) AS median_wage
    FROM 
        salaires
    GROUP BY 
        department
)

SELECT 
    s.name, 
    s.department, 
    s.wage,
    CASE 
        WHEN s.wage > dm.median_wage THEN 'Above Median'
        WHEN s.wage < dm.median_wage THEN 'Below Median'
        ELSE 'At Median'
    END AS comparison_to_median
FROM 
    salaires s
INNER JOIN department_medians dm 
ON s.department = dm.department
WHERE s.department != 'CEO'
