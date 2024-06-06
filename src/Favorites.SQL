CREATE TABLE IF NOT EXISTS favorites(
    Poster_ID CHAR(4),
    username CHAR(20),
    CONSTRAINT nuser PRIMARY KEY (Poster_ID, username)
);