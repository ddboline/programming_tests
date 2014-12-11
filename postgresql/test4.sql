DELETE
FROM   person
WHERE  id = 3; -- Lisa Hamilton
 
-- no hit expected
SELECT *
FROM   person
WHERE  id = 3;
 
-- ROLLBACK restores the deletion
ROLLBACK;
 
-- ONE hit expected !!! Else: check AUTOCOMMIT
SELECT *
FROM   person
WHERE  id = 3;