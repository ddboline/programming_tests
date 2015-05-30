--
-- show only important columns
SELECT p.firstname, p.lastname, c.contact_type AS "Kind of Contact", c.contact_value AS "Call Number"
FROM   person p
JOIN   contact c ON p.id = c.person_id;

-- show only desired rows
SELECT p.firstname, p.lastname, c.contact_type AS "Kind of Contact", c.contact_value AS "Call Number"
FROM   person p
JOIN   contact c ON p.id = c.person_id
WHERE  c.contact_type IN ('fixed line', 'mobile');
 
-- apply any sort order
SELECT p.firstname, p.lastname, c.contact_type AS "Kind of Contact", c.contact_value AS "Call Number"
FROM   person p
JOIN   contact c ON p.id = c.person_id
WHERE  c.contact_type IN ('fixed line', 'mobile')
ORDER BY p.lastname, p.firstname, c.contact_type DESC;
 
-- use functions: min() / max() / count()
SELECT COUNT(*)
FROM   person p
JOIN   contact c ON p.id = c.person_id
WHERE  c.contact_type IN ('fixed line', 'mobile');
 
-- JOIN a table with itself. Example: Search different persons with same lastname
SELECT p1.id, p1.firstname, p1.lastname, p2.id, p2.firstname, p2.lastname
FROM   person p1
JOIN   person p2 ON p1.lastname = p2.lastname -- for second incarnation of person we must use a different alias
WHERE  p1.id != p2.id
-- sorting of p2.lastname is not necessary as it is identical to the already sorted p1.lastname
ORDER BY p1.lastname, p1.firstname, p2.firstname;
 
-- JOIN more than two tables. Example: contact information of different persons with same lastname
SELECT p1.id, p1.firstname, p1.lastname, p2.id, p2.firstname, p2.lastname, c.contact_type, c.contact_value
FROM   person p1
JOIN   person p2 ON p1.lastname = p2.lastname
JOIN   contact c ON p2.id = c.person_id       -- contact info from person2. p1.id would lead to person1
WHERE  p1.id != p2.id
ORDER BY p1.lastname, p1.firstname, p2.lastname;

-- A list of persons and their contacts
SELECT p.firstname, p.lastname, c.contact_type, c.contact_value
FROM   person p
JOIN   contact c ON p.id = c.person_id  -- identical meaning: INNER JOIN ...
ORDER BY p.lastname, p.firstname, c.contact_type DESC, c.contact_value;

-- A list of ALL persons plus their contacts
SELECT    p.firstname, p.lastname, c.contact_type, c.contact_value
FROM      person p
LEFT JOIN contact c ON p.id = c.person_id  -- identical meaning: LEFT OUTER JOIN ...
ORDER BY  p.lastname, p.firstname, c.contact_type DESC, c.contact_value;

SELECT    p.firstname, p.lastname, c.contact_type, c.contact_value
FROM      contact c
LEFT JOIN person p  ON p.id = c.person_id  -- identical meaning: LEFT OUTER JOIN ...
ORDER BY  p.lastname, p.firstname, c.contact_type DESC, c.contact_value;

-- A list of ALL contact records with any corresponding person data, even if s
SELECT     p.firstname, p.lastname, c.contact_type, c.contact_value
FROM       person p
RIGHT JOIN contact c ON p.id = c.person_id  -- same as RIGHT OUTER JOIN ...
ORDER BY   p.lastname, p.firstname, c.contact_type DESC, c.contact_value;

SELECT    p.firstname, p.lastname, c.contact_type, c.contact_value
FROM      person p
FULL JOIN contact c ON p.id = c.person_id  -- identical meaning: FULL OUTER JOIN ...
ORDER BY  p.lastname, p.firstname, c.contact_type DESC, c.contact_value;

