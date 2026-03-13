CREATE TABLE books (
id SERIAL PRIMARY KEY,
title TEXT UNIQUE NOT NULL,
author TEXT
);

CREATE TABLE genres (
id SERIAL PRIMARY KEY,
name text UNIQUE NOT NULL
);

CREATE TABLE books_genres (
book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
genre_id INTEGER NOT NULL REFERENCES genres(id) ON DELETE CASCADE,
PRIMARY KEY (book_id, genre_id)
);

CREATE INDEX idx_books_genres_genre_id
ON books_genres (genre_id);