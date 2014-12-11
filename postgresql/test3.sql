-- Remove the new person
DELETE
FROM   person
WHERE  id = 99;
 
-- Is the person really gone away? Again, the process who performs the write operation will see the changes, even 
-- if they are actually not committed. (No hit expected.)
SELECT *
FROM   person
WHERE  id = 99;
 
-- Try COMMIT command
COMMIT;
 
-- Is the person still in the database? (No hit expected.)
SELECT *
FROM   person
WHERE  id = 99;