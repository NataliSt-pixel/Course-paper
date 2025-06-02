CREATE TABLE Genres (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE Artists (
    artist_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);


CREATE TABLE ArtistGenres (
    artist_genre_id SERIAL PRIMARY KEY,
    artist_id INTEGER NOT NULL REFERENCES Artists(artist_id),
    genre_id INTEGER NOT NULL REFERENCES Genres(genre_id),
    UNIQUE (artist_id, genre_id)
);


CREATE TABLE Albums (
    album_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    release_year INTEGER
);


CREATE TABLE AlbumArtists (
    album_artist_id SERIAL PRIMARY KEY,
    album_id INTEGER NOT NULL REFERENCES Albums(album_id),
    artist_id INTEGER NOT NULL REFERENCES Artists(artist_id),
    UNIQUE (album_id, artist_id)
);


CREATE TABLE Tracks (
    track_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    duration INTEGER NOT NULL,  -- в секундах
    album_id INTEGER NOT NULL REFERENCES Albums(album_id)
);


CREATE TABLE Compilations (
    compilation_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    release_year INTEGER
);


CREATE TABLE TrackCompilations (
    track_comp_id SERIAL PRIMARY KEY,
    track_id INTEGER NOT NULL REFERENCES Tracks(track_id),
    compilation_id INTEGER NOT NULL REFERENCES Compilations(compilation_id),
    UNIQUE (track_id, compilation_id)
);
