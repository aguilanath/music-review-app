DROP DATABASE IF EXISTS music_reviews;
CREATE DATABASE music_reviews;
USE music_reviews;

CREATE TABLE Artists (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    genre VARCHAR(50),
    country VARCHAR(50)
);

CREATE TABLE Albums (
    album_id INT AUTO_INCREMENT PRIMARY KEY,
    artist_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    release_year YEAR,
    genre VARCHAR(50),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id) ON DELETE CASCADE
);

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user VARCHAR(50) NOT NULL,
    passwordHash VARCHAR(255) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE Reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    album_id INT NOT NULL,
    rating TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 10),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (album_id) REFERENCES Albums(album_id) ON DELETE CASCADE
);

-- Indexes for report filtering performance
CREATE INDEX idx_reviews_created_at ON Reviews(created_at);
CREATE INDEX idx_reviews_rating ON Reviews(rating);
CREATE INDEX idx_albums_genre ON Albums(genre);
CREATE INDEX idx_albums_artist_id ON Albums(artist_id);
