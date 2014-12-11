-- Count the number of rows to determine the next ID. Caution: This handling of IDs is absolutly NOT recommended for real applications!
INSERT INTO person ( id,   firstname,        lastname,    date_of_birth,     place_of_birth, ssn,           weight)
VALUES             ((SELECT COUNT(*) + 1000 FROM person),  -- The scalar value subquery. It computes one single value, in this case the new ID.
-- VALUES          ((Select * FROM (SELECT COUNT(*) + 1000 FROM person) tmp), -- MySQL insists in using an intermediate table
                           'Larry, no. ?',   'Goldstein', CURRENT_DATE,      'Dallas',       '078-05-1120', 95);
COMMIT;