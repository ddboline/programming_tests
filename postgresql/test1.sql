-- We have seen on this page: SELECT / FROM / WHERE / ORDER BY
SELECT p.lastname,
       p.weight,
       p.weight * 100 / (SELECT avg(p2.weight) FROM person p2) AS percentage_of_average
FROM   person p
WHERE  p.weight BETWEEN 70 AND 90
ORDER BY p.weight DESC, p.place_of_birth;