Vous devez analyser les salaires des employés (sauf le CEO) en les comparant à la médiane des salaires au sein de leur département respectif. Plus précisément, pour chaque employé, vous devez déterminer si son salaire est au-dessus, en dessous, ou exactement à la médiane des salaires de son département.

Pour cela, suivez les étapes suivantes :

- Calculez la médiane des salaires pour chaque département. La médiane est le salaire qui divise en deux groupes égaux le nombre total d'employés du département, avec la moitié ayant un salaire inférieur à la médiane et l'autre moitié un salaire supérieur.

- Comparez le salaire de chaque employé à la médiane de son département. Si le salaire est supérieur à la médiane, l'employé sera classé comme "Above Median". Si le salaire est inférieur, il sera classé comme "Below Median". Si le salaire est exactement égal à la médiane, il sera classé comme "At Median".

Écrivez une requête SQL qui affiche pour chaque employé son nom, son département, son salaire, ainsi que la classification de son salaire par rapport à la médiane de son département.