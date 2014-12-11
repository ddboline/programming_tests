SELECT *
FROM   person
WHERE  CASE
         -- Modify weight depending on place of birth.
         WHEN place_of_birth = 'Dallas'   THEN weight * 0.8
         WHEN place_of_birth = 'Richland' THEN weight * 0.9
         ELSE                                  weight
       END > 80
OR     weight < 20; -- any other condition