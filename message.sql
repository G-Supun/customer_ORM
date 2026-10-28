CREATE TABLE classified_messages (
    id SERIAL PRIMARY KEY,
    mobile VARCHAR(15) NOT NULL,
    message TEXT NOT NULL,
    is_transactional BOOLEAN NOT NULL
);