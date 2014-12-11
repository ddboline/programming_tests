-- The next two statements compute different weights depending on the old weight
INSERT INTO person (id,          firstname, lastname, date_of_birth, place_of_birth, ssn, weight)
  -- the subquery starts here
  SELECT            id + 1200,   firstname, lastname, date_of_birth, place_of_birth, ssn,
                    CASE WHEN weight < 40 THEN weight + 10
                         ELSE                  weight +  5
                         END
  FROM   person
  WHERE  id <= 10;                          -- only the original 10 rows from the example database
COMMIT;
 
-- The same semantic with a more complex syntax (to demonstrate the power of subselect)
INSERT INTO person (id,          firstname, lastname, date_of_birth, place_of_birth, ssn, weight)
  -- the first subquery starts here
  SELECT            id + 1300,   firstname, lastname, date_of_birth, place_of_birth, ssn,
                     -- here starts a subquery of the first subquery. The CASE construct evaluates different
                     -- weights depending on the old weight.
                    (SELECT CASE WHEN weight < 40 THEN weight + 10
                                 ELSE                  weight +  5
                                 END
                     FROM   person ssq      -- alias for the table name in sub-subquery
                     WHERE  sq.id = ssq.id  -- link the rows together
                    )
  FROM   person sq                          -- alias for the table name in subquery
  WHERE  id <= 10;                          -- only the original 10 rows from the example database
COMMIT;