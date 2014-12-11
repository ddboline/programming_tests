-- A correlated table subquery, looking for lastnames within e-mail-addresses
SELECT * 
FROM   person p
WHERE  id IN 
  (SELECT person_id 
   FROM   contact c
   WHERE  c.contact_type = 'email'
   AND    UPPER(c.contact_value) LIKE CONCAT(CONCAT('%', UPPER(p.lastname)), '%'));