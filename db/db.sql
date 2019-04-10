DROP TABLE IF EXISTS tb_user;
DROP TABLE IF EXISTS tb_whisky;
DROP TABLE IF EXISTS tb_distillery;

CREATE TABLE IF NOT EXISTS tb_whisky (
	id SERIAL PRIMARY KEY, 
	name VARCHAR(255),
	distillery INTEGER,
	age INTEGER,
	abv FLOAT,
	owner INTEGER,
	notes TEXT
	);

CREATE TABLE IF NOT EXISTS tb_distillery (
	id SERIAL PRIMARY KEY, 
	name VARCHAR(255),
	region VARCHAR(255),
	country VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS tb_user (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);