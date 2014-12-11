-- One value list results in one new row.
INSERT INTO person (id,  firstname,       lastname,    date_of_birth,     place_of_birth, ssn,           weight)
VALUES             (91,  'Larry, no. 91', 'Goldstein', DATE'1970-11-20', 'Dallas',        '078-05-1120', 95);
COMMIT;
 
-- The SQL standard - but not all implementations - supports a 'row value constructor' by
-- enumerate values inside a pair of parenthesis as show in the above green box.  
-- Three lists of values (= row value constructors) result in three new rows. Please note the comma after all 
-- but the last one.
INSERT INTO person (id,  firstname,       lastname,    date_of_birth,     place_of_birth, ssn,           weight)
VALUES             (92,  'Larry, no. 92', 'Goldstein', DATE'1970-11-20', 'Dallas',        '078-05-1120', 95),
                   (93,  'Larry, no. 93', 'Goldstein', DATE'1970-11-20', 'Dallas',        '078-05-1120', 95),
                   (94,  'Larry, no. 94', 'Goldstein', DATE'1970-11-20', 'Dallas',        '078-05-1120', 95);
COMMIT;
