USE music_reviews;

-- Artists
INSERT INTO Artists (name, genre, country) VALUES
('Kendrick Lamar', 'Hip-Hop', 'USA'),
('Taylor Swift', 'Pop', 'USA'),
('Arctic Monkeys', 'Indie Rock', 'UK'),
('Beyoncé', 'R&B', 'USA'),
('Radiohead', 'Alternative', 'UK'),
('Frank Ocean', 'R&B', 'USA'),
('Billie Eilish', 'Pop', 'USA'),
('Tyler the Creator', 'Hip-Hop', 'USA');

-- Albums
INSERT INTO Albums (artist_id, title, release_year, genre) VALUES
(1, 'To Pimp a Butterfly', 2015, 'Hip-Hop'),
(1, 'DAMN.', 2017, 'Hip-Hop'),
(2, 'Folklore', 2020, 'Indie Pop'),
(2, 'Midnights', 2022, 'Pop'),
(3, 'AM', 2013, 'Indie Rock'),
(3, 'Tranquility Base Hotel & Casino', 2018, 'Indie Rock'),
(4, 'Lemonade', 2016, 'R&B'),
(5, 'OK Computer', 1997, 'Alternative'),
(5, 'Kid A', 2000, 'Alternative'),
(6, 'Blonde', 2016, 'R&B'),
(7, 'When We All Fall Asleep, Where Do We Go?', 2019, 'Pop'),
(8, 'IGOR', 2019, 'Hip-Hop');

-- Users
INSERT INTO Users (name, username, email) VALUES
('Alice Johnson', 'alice', 'alice@example.com'),
('Bob Smith', 'bob', 'bob@example.com'),
('Carol White', 'carol', 'carol@example.com'),
('David Lee', 'david', 'david@example.com'),
('Emma Davis', 'emma', 'emma@example.com');

-- Reviews
INSERT INTO Reviews (user_id, album_id, rating, comment, created_at) VALUES
(1, 1, 10, 'An absolute masterpiece. Kendrick at his finest.', '2024-01-15 10:00:00'),
(2, 1, 9, 'Lyrically stunning. Changed the game.', '2024-01-20 14:30:00'),
(3, 2, 8, 'DAMN. is a banger from start to finish.', '2024-02-05 09:00:00'),
(1, 3, 9, 'Folklore is hauntingly beautiful.', '2024-02-10 11:00:00'),
(4, 4, 7, 'Midnights has some great tracks but feels uneven.', '2024-03-01 16:00:00'),
(5, 5, 9, 'AM is one of the best rock albums of the decade.', '2024-03-15 13:00:00'),
(2, 7, 10, 'Lemonade is a visual and sonic masterpiece.', '2024-04-01 10:00:00'),
(3, 8, 10, 'OK Computer defined a generation.', '2024-04-10 15:00:00'),
(4, 9, 9, 'Kid A is ahead of its time even today.', '2024-05-01 12:00:00'),
(5, 10, 10, 'Blonde is a once-in-a-generation album.', '2024-05-15 11:00:00'),
(1, 11, 8, 'Billie delivered something truly unique.', '2024-06-01 09:30:00'),
(2, 12, 9, 'IGOR is Tyler at his most creative.', '2024-06-20 14:00:00'),
(3, 3, 8, 'Folklore grew on me with every listen.', '2024-07-01 10:00:00'),
(4, 1, 10, 'To Pimp a Butterfly is timeless.', '2024-07-15 16:30:00'),
(5, 5, 8, 'AM never gets old.', '2024-08-01 11:00:00');
