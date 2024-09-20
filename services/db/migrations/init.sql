CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    published_at TIMESTAMP WITH TIME ZONE NOT NULL,
    content TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    tags TEXT[]
);