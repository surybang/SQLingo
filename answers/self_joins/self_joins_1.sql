SELECT 
    emp.employee_id as "id employé",
    emp.employee_name as "nom employé",
    man.employee_id as "id manager",
    man.employee_name as "nom manager" 
FROM employees emp
LEFT JOIN employees man
ON man.manager_id = emp.employee_id
