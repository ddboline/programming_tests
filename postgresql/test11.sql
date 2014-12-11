-- Technical term: "simple case" 
-- Select id, contact_type in a translated version and contact_value
SELECT id,
       CASE contact_type
         WHEN 'fixed line' THEN 'Phone'
         WHEN 'mobile'     THEN 'Phone'
         ELSE                   'Not a telephone number'
       END,
       contact_value
FROM   contact;

-- Technical term: "searched case" 
-- Select persons name, weight and a denomination of the weight 
SELECT firstname,
       lastname,
       weight,
       CASE
         WHEN (weight IS NULL OR weight = 0) THEN 'weight is unknown'
         WHEN weight < 40                    THEN 'lightweight'
         WHEN weight BETWEEN 40 AND 85       THEN 'medium'
         ELSE                                     'heavyweight'
       END
FROM   person
order by weight;

SELECT *
FROM   contact
ORDER  BY
       -- a "simple case" construct as substitution for a column name
       CASE contact_type
         WHEN 'fixed line' THEN 0
         WHEN 'mobile'     THEN 1
         WHEN 'email'      THEN 2
         WHEN 'icq'        THEN 3
         ELSE                   4
       END,
       contact_value;

