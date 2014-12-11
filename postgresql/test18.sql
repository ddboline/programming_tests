-- The statement doubles the number of rows within the table. It omits in the table subquery the WHERE clause and therefore
-- it reads all existing rows. Caution: This handling of IDs is absolutly NOT recommended for real applications!
INSERT INTO person (id,          firstname, lastname, date_of_birth, place_of_birth, ssn, weight)
  SELECT            id + 1100,   firstname, lastname, date_of_birth, place_of_birth, ssn, weight
  FROM   person;
COMMIT;