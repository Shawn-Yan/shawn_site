-- To create the database:
-- sqlite3 db.SQLite3


-- To create the table:
-- sqlite3 db.SQLite3 < schema.sql

DROP TABLE IF EXISTS authors;
CREATE TABLE authors(
    id INTEGER PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    name VARCHAR(100)
);

DROP TABLE IF EXISTS article;
CREATE TABLE article(
    id INT PRIMARY KEY,
    author_id INT REFERENCES authors(id),
    slug VARCHAR(100) UNIQUE,
    title VARCHAR(512),
    markdown MEDIUMTEXT,
    html MEDIUMTEXT,
    published DATETIME,
    updated TIMESTAMP
);