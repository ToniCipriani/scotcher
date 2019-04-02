CREATE TABLE IF NOT EXISTS tb_whisky (
	id SERIAL, 
	name VARCHAR(255),
	distillery VARCHAR(255),
	region VARCHAR(255),
	age INTEGER,
	abv FLOAT,
	notes TEXT
	)
