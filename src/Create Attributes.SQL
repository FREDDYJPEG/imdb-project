CREATE TABLE IF NOT EXISTS imdb_top_1000(
    Poster_ID CHAR(4),
    Series_Title CHAR(100),
    Released_Year INT,
    Certificate CHAR(20),
    Runtime CHAR(20),
    Genre CHAR(50),
    IMDB_Rating FLOAT,
    Overview CHAR(1000),
    Meta_score INT,
    Director CHAR(100),
    Star1 CHAR(100),
    Star2 CHAR(100),
    Star3 CHAR(100),
    Star4 CHAR(100),
    No_of_Votes INT,
    Gross CHAR(20),
    Local_Poster_Path CHAR(255),
    CONSTRAINT imdb_pk PRIMARY KEY (Poster_ID)
);

COPY imdb_top_1000(Series_Title, Released_Year, Certificate, Runtime, Genre, IMDB_Rating, Overview, Meta_score, Director, Star1, Star2, Star3, Star4, No_of_Votes, Gross, Local_Poster_Path, Poster_ID)
FROM '/Users/frede/Downloads/modified_imdb_top_1000.csv'
DELIMITER ','
CSV HEADER;

