-- persons combined with their hobbies
SELECT p.id p_id, p.firstname, p.lastname, h.hobbyname, h.id h_id
FROM   person       p
JOIN   person_hobby ph ON p.id = ph.person_id
JOIN   hobby        h  ON ph.hobby_id = h.id
ORDER BY p.lastname, p.firstname, h.hobbyname;

-- ALL persons plus their hobbies (if present)
SELECT p.id p_id, p.firstname, p.lastname, h.hobbyname, h.id h_id
FROM   person            p
LEFT JOIN   person_hobby ph ON p.id = ph.person_id
LEFT JOIN   hobby        h  ON ph.hobby_id = h.id
ORDER BY p.lastname, p.firstname, h.hobbyname;

-- Group over one column: place_of_birth leads to 6 resulting rows
SELECT place_of_birth, COUNT(*)
FROM   person
GROUP BY place_of_birth;
-- Group over two columns: place_of_birth plus lastname leads to 8 resulting rows with Richland and SF shown twice
SELECT place_of_birth, lastname, COUNT(*)
FROM   person
GROUP BY place_of_birth, lastname;

SELECT lastname, COUNT(*)  -- count() is a function which counts values or rows
FROM   person
GROUP BY lastname;

