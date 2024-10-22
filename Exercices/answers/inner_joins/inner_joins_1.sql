SELECT * 
FROM salaries
INNER JOIN seniorities
USING (employee_id)
