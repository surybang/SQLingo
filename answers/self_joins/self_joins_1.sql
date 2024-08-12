SELECT * FROM 
employees le
LEFT JOIN employees re
ON le.manager_id = re.employee_id