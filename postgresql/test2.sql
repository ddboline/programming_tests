-- Store a new person with id 99.
INSERT INTO person (id, firstname, lastname, date_of_birth,    place_of_birth, ssn,           weight)
VALUES             (99, 'Harriet', 'Flint',  DATE'1970-10-19', 'Dallas',       '078-05-1120', 65);
 
-- Is the new person really in the database? The process who executes the write operation will see its results,
-- even if they are actually not committed. (One hit expected.)
SELECT *
FROM   person
WHERE  id = 99;
 
-- Try COMMIT command
COMMIT;
 
-- Is she still in the database? (One hit expected.)
SELECT *
FROM   person
WHERE  id = 99;