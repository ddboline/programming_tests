-- Restrict access to few rows
CREATE VIEW person_view_3 AS
  SELECT firstname, lastname, date_of_birth, place_of_birth, weight
  FROM   person
  WHERE  place_of_birth IN ('San Francisco', 'Richland');
 
-- Verify result:
SELECT *
FROM   person_view_3;