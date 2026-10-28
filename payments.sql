CREATE TABLE customer_payments(
	pid SERIAL PRIMARY KEY,
	cid INT,
	amount NUMERIC(10,2) NOT NULL,
	payment_type VARCHAR(20),

	CONSTRAINT fk_customer
		FOREIGN KEY(cid)
		REFERENCES customers(cid)
);