-- store every second row in a new table 'hobby_shadow'
CREATE TABLE hobby_shadow AS SELECT * FROM hobby WHERE MOD(id, 2) = 0;
SELECT * FROM hobby_shadow;
 
-- INSERT / UPDATE depending on the column 'id'.
MERGE INTO  hobby_shadow                   t   -- the target
      USING (SELECT id, hobbyname, remark
             FROM   hobby)                 s   -- the source
      ON    (t.id = s.id)                      -- the 'match criterion'
  WHEN MATCHED THEN
UPDATE SET remark = concat(s.remark, ' Merge / Update')
  WHEN NOT MATCHED THEN
INSERT (id, hobbyname, remark) VALUES (s.id, s.hobbyname, concat(s.remark, ' Merge / Insert'))
;
COMMIT;
 
-- Check the result
SELECT * FROM hobby_shadow;