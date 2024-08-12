SELECT year, region, SUM(population) 
FROM datapop
GROUP BY 
GROUPING SETS ((year, region), year)