CREATE TABLE IF NOT EXISTS mainmenu(
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
text text NOT NULL,
url text NOT NULL,
time text NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
username text NOT NULL,
email text NOT NULL,
password text NOT NULL,
avatar blob DEFAULT NULL,
time integer NOT NULL
);

