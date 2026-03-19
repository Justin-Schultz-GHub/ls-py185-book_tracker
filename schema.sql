CREATE TABLE IF NOT EXISTS books (
id SERIAL PRIMARY KEY,
title TEXT UNIQUE NOT NULL,
author TEXT NOT NULL,
synopsis TEXT
);

CREATE TABLE IF NOT EXISTS genres (
id SERIAL PRIMARY KEY,
name text UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS books_genres (
book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
genre_id INTEGER NOT NULL REFERENCES genres(id) ON DELETE CASCADE,
PRIMARY KEY (book_id, genre_id)
);

CREATE INDEX IF NOT EXISTS idx_books_genres_genre_id
ON books_genres (genre_id);

CREATE TABLE IF NOT EXISTS users (
id SERIAL PRIMARY KEY,
username VARCHAR(20) UNIQUE,
password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users_books (
id SERIAL PRIMARY KEY,
user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
UNIQUE (user_id, book_id),
status TEXT NOT NULL CHECK (status in ('Completed', 'Reading', 'Plan to Read', 'Dropped', 'On Hold')),
score TEXT,
memo TEXT
);

INSERT INTO genres (name) VALUES
('Mystery'),
('Fiction'),
('Historical'),
('Fantasy'),
('Sci-Fi'),
('Thriller'),
('Horror'),
('Romance'),
('Adventure')
ON CONFLICT (name) DO NOTHING;

INSERT INTO books (title, author) VALUES
('The Hound of the Baskervilles', 'Arthur Conan Doyle'),
('Gone Girl', 'Gillian Flynn'),
('The Da Vinci Code', 'Dan Brown'),
('Pride and Prejudice', 'Jane Austen'),
('1984', 'George Orwell'),
('Brave New World', 'Aldous Huxley'),
('The Great Gatsby', 'F. Scott Fitzgerald'),
('To Kill a Mockingbird', 'Harper Lee'),
('The Hobbit', 'J.R.R. Tolkien'),
('Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling'),
('The Name of the Wind', 'Patrick Rothfuss'),
('A Game of Thrones', 'George R.R. Martin'),
('The Catcher in the Rye', 'J.D. Salinger'),
('Moby-Dick', 'Herman Melville'),
('The Shining', 'Stephen King'),
('Dracula', 'Bram Stoker'),
('Frankenstein', 'Mary Shelley'),
('The Girl with the Dragon Tattoo', 'Stieg Larsson'),
('The Hunger Games', 'Suzanne Collins'),
('Divergent', 'Veronica Roth'),
('The Adventures of Sherlock Holmes', 'Arthur Conan Doyle'),
('And Then There Were None', 'Agatha Christie'),
('The Silence of the Lambs', 'Thomas Harris'),
('Inferno', 'Dan Brown'),
('Angels & Demons', 'Dan Brown'),
('Jane Eyre', 'Charlotte Brontë'),
('Wuthering Heights', 'Emily Brontë'),
('Les Misérables', 'Victor Hugo'),
('War and Peace', 'Leo Tolstoy'),
('Crime and Punishment', 'Fyodor Dostoevsky'),
('Dr. Jekyll and Mr. Hyde', 'Robert Louis Stevenson'),
('It', 'Stephen King'),
('Pet Sematary', 'Stephen King'),
('Carrie', 'Stephen King'),
('The Chronicles of Narnia', 'C.S. Lewis'),
('Alice''s Adventures in Wonderland', 'Lewis Carroll'),
('The Odyssey', 'Homer'),
('The Iliad', 'Homer'),
('Treasure Island', 'Robert Louis Stevenson'),
('The Count of Monte Cristo', 'Alexandre Dumas'),
('The Alchemist', 'Paulo Coelho'),
('The Fault in Our Stars', 'John Green'),
('Me Before You', 'Jojo Moyes'),
('The Martian', 'Andy Weir'),
('Ender''s Game', 'Orson Scott Card'),
('Ready Player One', 'Ernest Cline'),
('Neuromancer', 'William Gibson'),
('Snow Crash', 'Neal Stephenson'),
('The Road', 'Cormac McCarthy'),
('Life of Pi', 'Yann Martel'),
('The Adventures of Huckleberry Finn', 'Mark Twain'),
('The Picture of Dorian Gray', 'Oscar Wilde'),
('The Time Machine', 'H.G. Wells')
ON CONFLICT (title) DO NOTHING;

UPDATE books SET synopsis = 'Sherlock Holmes investigates a mysterious death tied to a legendary hound on the moors.' WHERE id = 1;
UPDATE books SET synopsis = 'A woman disappears, and suspicion falls on her husband as dark secrets unravel.' WHERE id = 2;
UPDATE books SET synopsis = 'A symbologist uncovers a conspiracy tied to secret societies and religious history.' WHERE id = 3;
UPDATE books SET synopsis = 'A sharp-witted woman navigates love, class, and societal expectations in Regency England.' WHERE id = 4;
UPDATE books SET synopsis = 'A man struggles to survive under a totalitarian regime that controls truth and thought.' WHERE id = 5;
UPDATE books SET synopsis = 'A futuristic society maintains order through control, conditioning, and pleasure.' WHERE id = 6;
UPDATE books SET synopsis = 'A mysterious millionaire pursues a lost love in the glittering world of the 1920s.' WHERE id = 7;
UPDATE books SET synopsis = 'A young girl witnesses racial injustice in the American South.' WHERE id = 8;
UPDATE books SET synopsis = 'A hobbit embarks on an adventure to reclaim a stolen treasure guarded by a dragon.' WHERE id = 9;
UPDATE books SET synopsis = 'A young wizard discovers his magical heritage and attends a school of witchcraft.' WHERE id = 10;
UPDATE books SET synopsis = 'A gifted young man recounts his journey to become a legendary magician.' WHERE id = 11;
UPDATE books SET synopsis = 'Noble families vie for power in a brutal and unpredictable fantasy world.' WHERE id = 12;
UPDATE books SET synopsis = 'A teenage boy reflects on alienation and identity in New York City.' WHERE id = 13;
UPDATE books SET synopsis = 'A sailor becomes obsessed with hunting a great white whale.' WHERE id = 14;
UPDATE books SET synopsis = 'A writer descends into madness while isolated in a haunted hotel.' WHERE id = 15;
UPDATE books SET synopsis = 'A vampire travels from Transylvania to England, spreading terror.' WHERE id = 16;
UPDATE books SET synopsis = 'A scientist creates life, only to be horrified by his own creation.' WHERE id = 17;
UPDATE books SET synopsis = 'A journalist investigates a decades-old disappearance and a powerful family.' WHERE id = 18;
UPDATE books SET synopsis = 'Teenagers are forced to fight to the death in a dystopian society.' WHERE id = 19;
UPDATE books SET synopsis = 'A girl uncovers secrets about her society and her own identity.' WHERE id = 20;
UPDATE books SET synopsis = 'A collection of mysteries solved by the brilliant detective Sherlock Holmes.' WHERE id = 21;
UPDATE books SET synopsis = 'Guests on an island are killed one by one according to a chilling rhyme.' WHERE id = 22;
UPDATE books SET synopsis = 'An FBI trainee hunts a brilliant and terrifying serial killer.' WHERE id = 23;
UPDATE books SET synopsis = 'A deadly plot linked to Dante’s work threatens the world.' WHERE id = 24;
UPDATE books SET synopsis = 'A murder investigation reveals secrets of an ancient religious order.' WHERE id = 25;
UPDATE books SET synopsis = 'An orphaned governess falls in love with her mysterious employer.' WHERE id = 26;
UPDATE books SET synopsis = 'A tragic love story unfolds amid passion and revenge on the moors.' WHERE id = 27;
UPDATE books SET synopsis = 'The lives of several characters intertwine during social upheaval in France.' WHERE id = 28;
UPDATE books SET synopsis = 'Russian society is explored during the Napoleonic Wars.' WHERE id = 29;
UPDATE books SET synopsis = 'A man grapples with guilt after committing a brutal crime.' WHERE id = 30;
UPDATE books SET synopsis = 'A man’s dark alter ego emerges, revealing the duality of human nature.' WHERE id = 31;
UPDATE books SET synopsis = 'A group confronts a shape-shifting evil that preys on their fears.' WHERE id = 32;
UPDATE books SET synopsis = 'A family is haunted by the consequences of tampering with death.' WHERE id = 33;
UPDATE books SET synopsis = 'A bullied girl with telekinetic powers seeks revenge.' WHERE id = 34;
UPDATE books SET synopsis = 'Children discover a magical world filled with adventure and danger.' WHERE id = 35;
UPDATE books SET synopsis = 'A girl falls into a whimsical and nonsensical fantasy world.' WHERE id = 36;
UPDATE books SET synopsis = 'A hero journeys home after the Trojan War, facing many trials.' WHERE id = 37;
UPDATE books SET synopsis = 'The events of the Trojan War unfold with heroes and gods.' WHERE id = 38;
UPDATE books SET synopsis = 'A boy embarks on a pirate adventure in search of buried treasure.' WHERE id = 39;
UPDATE books SET synopsis = 'A man seeks revenge against those who betrayed him.' WHERE id = 40;
UPDATE books SET synopsis = 'A shepherd follows his dreams in search of treasure and meaning.' WHERE id = 41;
UPDATE books SET synopsis = 'Two teenagers fall in love while dealing with serious illness.' WHERE id = 42;
UPDATE books SET synopsis = 'A caregiver forms a life-changing bond with a paralyzed man.' WHERE id = 43;
UPDATE books SET synopsis = 'An astronaut struggles to survive alone on Mars.' WHERE id = 44;
UPDATE books SET synopsis = 'A young genius is trained through war simulations to fight aliens.' WHERE id = 45;
UPDATE books SET synopsis = 'A young man escapes into a virtual reality world full of challenges.' WHERE id = 46;
UPDATE books SET synopsis = 'A hacker navigates a dystopian cyberpunk world of AI and corporations.' WHERE id = 47;
UPDATE books SET synopsis = 'A futuristic world blends virtual reality, culture, and corporate power.' WHERE id = 48;
UPDATE books SET synopsis = 'A father and son struggle to survive in a bleak post-apocalyptic world.' WHERE id = 49;
UPDATE books SET synopsis = 'A boy survives a shipwreck and forms a bond with a tiger.' WHERE id = 50;
UPDATE books SET synopsis = 'A boy travels down the Mississippi River, seeking freedom and adventure.' WHERE id = 51;
UPDATE books SET synopsis = 'A man remains eternally young while his portrait ages and reveals his corruption.' WHERE id = 52;
UPDATE books SET synopsis = 'A scientist travels through time to witness the future of humanity.' WHERE id = 53;

INSERT INTO books_genres (book_id, genre_id) VALUES
(1, 1),
(2, 6),
(3, 6),
(4, 2),
(5, 2),
(6, 2),
(7, 2),
(8, 2),
(9, 4),
(10, 4),
(11, 4),
(12, 4),
(13, 2),
(14, 2),
(15, 7),
(16, 7),
(17, 7),
(18, 1),
(19, 4),
(19, 9),
(20, 4),
(21, 1),
(22, 1),
(23, 6),
(24, 6),
(25, 6),
(26, 2),
(27, 2),
(28, 3),
(29, 3),
(30, 3),
(31, 1),
(31, 7),
(32, 7),
(33, 7),
(34, 7),
(35, 4),
(36, 4),
(37, 3),
(38, 3),
(39, 9),
(40, 3),
(41, 2),
(42, 8),
(43, 8),
(44, 5),
(45, 5),
(46, 5),
(47, 5),
(48, 5),
(49, 2),
(50, 2),
(50, 9),
(51, 9),
(52, 2),
(52, 7),
(53, 5)
ON CONFLICT (book_id, genre_id) DO NOTHING;