-- Retrieve the row. As defined in CREATE TABLE statement the weight has a default value of integer 0.
-- Date_of_birth and place_of_birth contain the NULL special marker.
SELECT * FROM person WHERE  id = 51;
 
-- use the IS NULL predicate within WHERE clause. The result contains 1 row.
SELECT * FROM person WHERE ssn IS NULL;
 
-- weight has a value!! We expect to retrieve no rows when we use the IS NULL predicate.
SELECT * FROM person WHERE weight IS NULL;
-- or, to say it the other way round, the number of rows is 0
SELECT COUNT(*) FROM person WHERE weight IS NULL;
-- but in the next statement the number of rows is 1
SELECT COUNT(*) FROM person WHERE weight = 0;
 
-- Negate the IS NULL predicate
SELECT COUNT(*) FROM person WHERE ssn IS NULL;     -- IS NULL
SELECT COUNT(*) FROM person WHERE ssn IS NOT NULL; -- Negation of IS NULL
 
SELECT COUNT(*)
FROM   person
WHERE  ssn IS NULL
OR     ssn IS NOT NULL; -- A tautology, which always retrieves ALL rows of a table
-- Same as above
SELECT COUNT(*)
FROM   person
WHERE  ssn IS NULL
OR NOT ssn IS NULL; -- A tautology, which always retrieves ALL rows of a table