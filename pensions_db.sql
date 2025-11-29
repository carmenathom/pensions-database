CREATE TYPE user_role AS ENUM ('Admin', 'Curator', 'EndUser');

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role user_role NOT NULL,
    name VARCHAR(100),
    last_activity TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE Document (
    document_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    doc_type VARCHAR(50),
    source TEXT,
    added_by INT NOT NULL REFERENCES Users(user_id),
    added_at TIMESTAMP DEFAULT NOW(),
    processed BOOLEAN DEFAULT FALSE
);

CREATE TABLE QueryLog (
    query_id SERIAL PRIMARY KEY,
    query_text TEXT NOT NULL,
    issued_by INT NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
    issued_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE QueryLogDocuments (
    query_id INT REFERENCES QueryLog(query_id),
    document_id INT REFERENCES Document(document_id),
    PRIMARY KEY (query_id, document_id)
);