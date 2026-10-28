CREATE TABLE messages (
    mid SERIAL PRIMARY KEY,
    mobile VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    is_transactional BOOLEAN NOT NULL
);

CREATE INDEX idx_mobile ON messages (mobile);
CREATE INDEX idx_is_transactional ON messages (is_transactional);