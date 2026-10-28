CREATE TABLE customer_salary(
	sid SERIAL PRIMARY KEY,
	cid INT,
	salary NUMERIC(10,2) NOT NULL,

	CONSTRAINT fk_customer
		FOREIGN KEY(cid)
		REFERENCES customers(cid)
);