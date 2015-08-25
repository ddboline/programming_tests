#!/usr/bin/python

from sqlalchemy import create_engine

engine = create_engine('sqlite:///test.db', echo=False)
con = engine.connect()

con.execute("""
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
""")

insert_statements = """
INSERT INTO person VALUES (1,  'Larry',  'Goldstein', DATE('1970-11-20'), 'Dallas',        '078-05-1120', 95);
INSERT INTO person VALUES (2,  'Tom',    'Burton',    DATE('1977-01-22'), 'Birmingham',    '078-05-1121', 75);
INSERT INTO person VALUES (3,  'Lisa',   'Hamilton',  DATE('1975-12-23'), 'Richland',      '078-05-1122', 56);
INSERT INTO person VALUES (4,  'Kim',    'Goldstein', DATE('2011-06-01'), 'Shanghai',      '078-05-1123', 11);
INSERT INTO person VALUES (5,  'James',  'de Winter', DATE('1975-12-23'), 'San Francisco', '078-05-1124', 75);
INSERT INTO person VALUES (6,  'Elias',  'Baker',     DATE('1939-10-03'), 'San Francisco', '078-05-1125', 55);
INSERT INTO person VALUES (7,  'Yorgos', 'Stefanos',  DATE('1975-12-23'), 'Athens',        '078-05-1126', 64);
INSERT INTO person VALUES (8,  'John',   'de Winter', DATE('1977-01-22'), 'San Francisco', '078-05-1127', 77);
INSERT INTO person VALUES (9,  'Richie', 'Rich',      DATE('1975-12-23'), 'Richland',      '078-05-1128', 90);
INSERT INTO person VALUES (10, 'Victor', 'de Winter', DATE('1979-02-28'), 'San Francisco', '078-05-1129', 78);
"""

for line in insert_statements.split('\n'):
    con.execute(line)

result = con.execute('select * from person;')
for line in result:
    print(line)

insert_statement = """
INSERT INTO person (id,  firstname,       lastname,    date_of_birth,     place_of_birth, ssn,           weight)
VALUES             (92,  'Larry, no. 92', 'Goldstein', DATE('1970-11-20'), 'Dallas',        '078-05-1120', 95),
                   (93,  'Larry, no. 93', 'Goldstein', DATE('1970-11-20'), 'Dallas',        '078-05-1120', 95),
                   (94,  'Larry, no. 94', 'Goldstein', DATE('1970-11-20'), 'Dallas',        '078-05-1120', 95);
"""

con.execute(insert_statement)

result = con.execute('select * from person;')
for line in result:
    print(line)
