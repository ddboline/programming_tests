CREATE TABLE podcasts(
    castid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    castname TEXT NOT NULL,
    feedurl TEXT NOT NULL UNIQUE,
    pcenabled INTEGER NOT NULL DEFAULT 1,
    lastupdate INTEGER,
    lastattempt INTEGER,
    failedattempts INTEGER NOT NULL DEFAULT 0)
CREATE TABLE "episodes" (
    castid INTEGER NOT NULL,
    episodeid INTEGER NOT NULL,
    title TEXT NOT NULL,
    epurl TEXT NOT NULL,
    enctype TEXT NOT NULL,
    status TEXT NOT NULL,
    eplength INTEGER NOT NULL DEFAULT 0,
    epfirstattempt INTEGER,
    eplastattempt INTEGER,
    epfailedattempts INTEGER NOT NULL DEFAULT 0,
    epguid TEXT,
    UNIQUE(castid, epurl),
    UNIQUE(castid, episodeid),
    UNIQUE(castid, epguid))
