-- As in our example database there is no example for the INTERSECT we insert a new person.
-- This person has the same lastname 'Victor' as the first name of another person.
INSERT INTO person VALUES (21, 'Paul', 'Victor', DATE'1966-04-02', 'Washington', '078-05-1121', 66);
COMMIT;
-- All firstnames which are used as lastname.
SELECT firstname  -- first SELECT command
FROM   person
  INTERSECT       -- looking for common values
SELECT lastname   -- second SELECT command
FROM   person;