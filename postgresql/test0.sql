-- comment lines starts with two consecutive minus signs followed by a space '-- '
CREATE TABLE person (
  -- define columns (name / type / default value / nullable)
  id             DECIMAL      NOT NULL,
  firstname      VARCHAR(50)  NOT NULL,
  lastname       VARCHAR(50)  NOT NULL,
  date_of_birth  DATE,
  place_of_birth VARCHAR(50),
  ssn            CHAR(11),
  weight         DECIMAL DEFAULT 0 NOT NULL,
  -- select one of the defined columns as the Primary Key and
  -- guess a meaningfull name for the Primary Key constraint: 'person_pk' may be a good choice 
  CONSTRAINT person_pk PRIMARY KEY (id)
);

commit;

--
-- After we have done a lot of tests we may want to reset the data to its original version.
-- To do so use the DELETE command. But be aware of Foreign Keys: you may be forced to delete
-- persons at the very end - with DELETE it's just the opposite sequence of tables in comparition to INSERTs.
-- Be careful and don't confuse DELETE with DROP !!
--
-- DELETE FROM person_hobby;
-- DELETE FROM hobby;
-- DELETE FROM contact;
-- DELETE FROM person;
-- COMMIT;
 
INSERT INTO person VALUES (1,  'Larry',  'Goldstein', DATE'1970-11-20', 'Dallas',        '078-05-1120', 95);
INSERT INTO person VALUES (2,  'Tom',    'Burton',    DATE'1977-01-22', 'Birmingham',    '078-05-1121', 75);
INSERT INTO person VALUES (3,  'Lisa',   'Hamilton',  DATE'1975-12-23', 'Richland',      '078-05-1122', 56);
INSERT INTO person VALUES (4,  'Kim',    'Goldstein', DATE'2011-06-01', 'Shanghai',      '078-05-1123', 11);
INSERT INTO person VALUES (5,  'James',  'de Winter', DATE'1975-12-23', 'San Francisco', '078-05-1124', 75);
INSERT INTO person VALUES (6,  'Elias',  'Baker',     DATE'1939-10-03', 'San Francisco', '078-05-1125', 55);
INSERT INTO person VALUES (7,  'Yorgos', 'Stefanos',  DATE'1975-12-23', 'Athens',        '078-05-1126', 64);
INSERT INTO person VALUES (8,  'John',   'de Winter', DATE'1977-01-22', 'San Francisco', '078-05-1127', 77);
INSERT INTO person VALUES (9,  'Richie', 'Rich',      DATE'1975-12-23', 'Richland',      '078-05-1128', 90);
INSERT INTO person VALUES (10, 'Victor', 'de Winter', DATE'1979-02-28', 'San Francisco', '078-05-1129', 78);
COMMIT;

CREATE TABLE contact (
  -- define columns (name / type / default value / nullable)
  id             DECIMAL      NOT NULL,
  person_id      DECIMAL      NOT NULL,
  -- use a default value, if contact_type is omitted
  contact_type   VARCHAR(25)  DEFAULT 'email' NOT NULL,
  contact_value  VARCHAR(50)  NOT NULL,
  -- select one of the defined columns as the Primary Key
  CONSTRAINT contact_pk PRIMARY KEY (id),
  -- define Foreign Key relation between column person_id and column id of table person
  CONSTRAINT contact_fk FOREIGN KEY (person_id) REFERENCES person(id),
  -- more contraint(s)
  CONSTRAINT contact_check CHECK (contact_type IN ('fixed line', 'mobile', 'email', 'icq', 'skype'))
);

CREATE TABLE hobby (
  -- define columns (name / type / default value / nullable)
  id             DECIMAL      NOT NULL,
  hobbyname      VARCHAR(100) NOT NULL,
  remark         VARCHAR(1000),
  -- select one of the defined columns as the Primary Key
  CONSTRAINT hobby_pk PRIMARY KEY (id),
  -- forbid duplicate recording of a hobby 
  CONSTRAINT hobby_unique UNIQUE (hobbyname)
);

CREATE TABLE person_hobby (
  -- define columns (name / type / default value / nullable)
  id             DECIMAL      NOT NULL,
  person_id      DECIMAL      NOT NULL,
  hobby_id       DECIMAL      NOT NULL,
  -- Also this table has its own Primary Key!
  CONSTRAINT person_hobby_pk PRIMARY KEY (id),
  -- define Foreign Key relation between column person_id and column id of table person
  CONSTRAINT person_hobby_fk_1 FOREIGN KEY (person_id) REFERENCES person(id),
  -- define Foreign Key relation between column hobby_id and column id of table hobby
  CONSTRAINT person_hobby_fk_2 FOREIGN KEY (hobby_id) REFERENCES hobby(id)
);

commit;

-- DELETE FROM contact;
-- COMMIT;
 
INSERT INTO contact VALUES (1,  1,  'fixed line', '555-0100');
INSERT INTO contact VALUES (2,  1,  'email',      'larry.goldstein@acme.xx');
INSERT INTO contact VALUES (3,  1,  'email',      'lg@my_company.xx');
INSERT INTO contact VALUES (4,  1,  'icq',        '12111');
INSERT INTO contact VALUES (5,  4,  'fixed line', '5550101');
INSERT INTO contact VALUES (6,  4,  'mobile',     '10123444444');
INSERT INTO contact VALUES (7,  5,  'email',      'james.dewinter@acme.xx');
INSERT INTO contact VALUES (8,  7,  'fixed line', '+30000000000000');
INSERT INTO contact VALUES (9,  7,  'mobile',     '+30695100000000');
COMMIT;

-- DELETE FROM hobby;
-- COMMIT;
 
INSERT INTO hobby VALUES (1,  'Painting',
                              'Applying paint, pigment, color or other medium to a surface.');
INSERT INTO hobby VALUES (2,  'Fishing',
                              'Catching fishes.');
INSERT INTO hobby VALUES (3,  'Underwater Diving',
                              'Going underwater with or without breathing apparatus (scuba diving / breath-holding).');
INSERT INTO hobby VALUES (4,  'Chess',
                              'Two players have 16 figures each. They move them on an eight-by-eight grid according to special rules.');
INSERT INTO hobby VALUES (5,  'Literature', 'Reading books.');
INSERT INTO hobby VALUES (6,  'Yoga',
                              'A physical, mental, and spiritual practices which originated in ancient India.');
INSERT INTO hobby VALUES (7,  'Stamp collecting',
                              'Collecting of post stamps and related objects.');
INSERT INTO hobby VALUES (8,  'Astronomy',
                              'Observing astronomical objects such as moons, planets, stars, nebulae, and galaxies.');
INSERT INTO hobby VALUES (9,  'Microscopy',
                              'Observing very small objects using a microscope.');
COMMIT;


-- DELETE FROM person_hobby;
-- COMMIT;
 
INSERT INTO person_hobby VALUES (1, 1, 1);
INSERT INTO person_hobby VALUES (2, 1, 4);
INSERT INTO person_hobby VALUES (3, 1, 5);
INSERT INTO person_hobby VALUES (4, 5, 2);
INSERT INTO person_hobby VALUES (5, 5, 3);
INSERT INTO person_hobby VALUES (6, 7, 8);
INSERT INTO person_hobby VALUES (7, 4, 4);
INSERT INTO person_hobby VALUES (8, 9, 8);
INSERT INTO person_hobby VALUES (9, 9, 9);
COMMIT;

-- Store a new person with id 99.
INSERT INTO person (id, firstname, lastname, date_of_birth,    place_of_birth, ssn,           weight)
VALUES             (99, 'Harriet', 'Flint',  DATE'1970-10-19', 'Dallas',       '078-05-1120', 65);
commit;

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

-- Insert a new row for testing purpose
INSERT INTO person (id, firstname, lastname)  VALUES (51, 'Half man', 'Uncomplete');
COMMIT;
 
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
commit;
