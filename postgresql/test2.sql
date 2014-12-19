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