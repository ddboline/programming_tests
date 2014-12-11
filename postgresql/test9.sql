--
-- Insert a new row for testing purpose with all columns filled with a usefull value
INSERT INTO person (id, firstname, lastname,  date_of_birth,    place_of_birth, ssn,           weight)
VALUES             (52, 'Lyn',     'Mutable', DATE'1951-05-13', 'Anchorage',    '078-05-1152', 69);
COMMIT;
SELECT * FROM person WHERE id = 52;
 
-- Delete a single column value (not the complete row)
UPDATE person SET ssn = NULL WHERE id = 52;
COMMIT;
SELECT * FROM person WHERE id = 52;      -- one row
SELECT * FROM person WHERE ssn IS NULL;  -- two rows: 51 + 52
