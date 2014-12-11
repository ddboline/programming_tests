-- order by weight classes
SELECT firstname, lastname, weight,
       CASE
         WHEN (weight IS NULL OR weight = 0) THEN 'weight is unknown'
         WHEN weight < 40                    THEN 'lightweight'
         WHEN weight BETWEEN 40 AND 85       THEN 'medium'
         ELSE                                     'heavyweight'
       END
FROM   person
ORDER  BY
       -- a "searched case" construct with IS NULL, BETWEEN and 'less than'.
       CASE
         WHEN (weight IS NULL OR weight = 0) THEN 0
         WHEN weight < 40                    THEN 1
         WHEN weight BETWEEN 40 AND 85       THEN 2
         ELSE                                     3 
       END, lastname, firstname;