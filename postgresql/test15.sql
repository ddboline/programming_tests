-- The table holds actual and historical values
CREATE TABLE booking (
  -- identifying columns
  id             DECIMAL      NOT NULL,
  booking_number DECIMAL      NOT NULL,
  version        DECIMAL      NOT NULL,
  -- describing columns
  state          CHAR(10)     NOT NULL,
  enter_ts       TIMESTAMP    NOT NULL,
  enter_by       CHAR(20)     NOT NULL,
  -- ...
  -- select one of the defined columns as the Primary Key
  CONSTRAINT booking_pk PRIMARY KEY (id),
  -- forbid duplicate recordings
  CONSTRAINT booking_unique UNIQUE (booking_number, version)
);
 
-- Add data
INSERT INTO booking VALUES (1, 4711, 1, 'created',   TIMESTAMP'2014-02-02 10:01:01', 'Emily');
INSERT INTO booking VALUES (2, 4711, 2, 'modified',  TIMESTAMP'2014-02-03 11:10:01', 'Emily');
INSERT INTO booking VALUES (3, 4711, 3, 'canceled',  TIMESTAMP'2014-02-10 09:01:01', 'John');
--
INSERT INTO booking VALUES (4, 4712, 1, 'created',   TIMESTAMP'2014-03-10 12:12:12', 'Emily');
INSERT INTO booking VALUES (5, 4712, 2, 'delivered', TIMESTAMP'2014-03-12 06:01:00', 'Charles');
--
INSERT INTO booking VALUES (6, 4713, 1, 'created',   TIMESTAMP'2014-03-11 08:50:02', 'Emily');
INSERT INTO booking VALUES (7, 4713, 2, 'canceled',  TIMESTAMP'2014-03-12 08:40:12', 'Emily');
INSERT INTO booking VALUES (8, 4713, 3, 'reopend',   TIMESTAMP'2014-03-13 10:04:32', 'Jack');
INSERT INTO booking VALUES (9, 4713, 4, 'delivered', TIMESTAMP'2014-03-15 06:40:12', 'Jack');
--
COMMIT;