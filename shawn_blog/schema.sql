-- To create the database:
-- sqlite3 db.SQLite3


-- To create the table:
-- sqlite3 db.SQLite3 < schema.sql

DROP TABLE IF EXISTS authors;
CREATE TABLE authors(
    id INT NOT NULL PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL
);


DROP TABLE IF EXISTS article;
CREATE TABLE article(
    id INT NOT NULL  PRIMARY KEY,
    author_id INT NOT NULL REFERENCES authors(id),
    slug VARCHAR(100) NOT NULL UNIQUE,
    title VARCHAR(512) NOT NULL,
    markdown MEDIUMTEXT NOT NULL,
    html MEDIUMTEXT NOT NULL,
    published DATETIME NOT NULL,
    updated TIMESTAMP NOT NULL
);