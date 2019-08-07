CREATE TABLE title_basics(
   titleId varchar(255) PRIMARY KEY,
   titleType varchar(255),
   primaryTitle varchar(255) NOT NULL,
   originalTitle varchar(255) NOT NULL,
   isAdult BOOLEAN NOT NULL,
   startYear SMALLINT NOT NULL CHECK (birthYear<=9999 AND birthYear>1800),
   endYear SMALLINT NOT NULL CHECK (birthYear<=9999 AND birthYear>1800),
   runtime int NOT NULL
);

CREATE TABLE title_akas(
   titleId varchar(255),
   ordering int,
   title varchar(255) NOT NULL,
   region varchar(255),
   language varchar(255),
   attributesId varchar(255) NOT NULL,
   isOriginalTitle BOOLEAN NOT NULL,
   FOREIGN KEY (titleId) REFERENCES title_basics(titleId),
   PRIMARY KEY (titleId, ordering)
);

CREATE TABLE title_types(
   titleId varchar(255),
   type varchar(255),
   FOREIGN KEY (titleId) REFERENCES title_akas(titleId),
   PRIMARY KEY (titleId, type)
);

CREATE TABLE title_attributes(
   titleId varchar(255),
   attribute varchar(255),
   FOREIGN KEY (titleId) REFERENCES title_akas(titleId),
   PRIMARY KEY (titleId, attribute)
);

CREATE TABLE title_genre(
   titleId varchar(255),
   genre varchar(255),
   FOREIGN KEY (titleId) REFERENCES title_basics(titleId),
   PRIMARY KEY (titleId, genre)
);

CREATE TABLE crew_names(
   nameId varchar(255) PRIMARY KEY,
   name varchar(255),
   birthYear SMALLINT NOT NULL CHECK (birthYear<=9999 AND birthYear>1800),
   deathYear SMALLINT CHECK (birthYear<=9999 AND birthYear>1800)
);

CREATE TABLE crew_professions(
   nameId varchar(255),
   profession varchar(255),
   FOREIGN KEY (nameId) REFERENCES crew_names(nameId),
   PRIMARY KEY (nameId, profession)
);

CREATE TABLE crew_known_for(
   nameId varchar(255),
   titleKnown varchar(255),
   FOREIGN KEY (nameId) REFERENCES crew_names(nameId),
   FOREIGN KEY (titleKnown) REFERENCES title_basics(titleId),
   PRIMARY KEY (nameId, titleKnown)
);

CREATE TABLE title_directors(
   titleId varchar(255),
   director varchar(255),
   FOREIGN KEY (titleId) REFERENCES title_basics(titleId),
   FOREIGN KEY (director) REFERENCES crew_names(nameId),
   PRIMARY KEY (titleId, director)
);

CREATE TABLE title_writers(
   titleId varchar(255),
   writer varchar(255),
   FOREIGN KEY (titleId) REFERENCES title_basics(titleId),
   FOREIGN KEY (director) REFERENCES crew_names(nameId),
   PRIMARY KEY (titleId, writer)
);

CREATE TABLE title_episodes(
   titleId varchar(255),
   seasonNumber int CHECK(seasonNumber>0) NOT NULL,
   episodeNumber int CHECK(episodeNumber>0) NOT NULL,
   FOREIGN KEY (titleId) REFERENCES title_basics(titleId),
   PRIMARY KEY (titleId, episodeNumber)
);

CREATE TABLE title_principals(
   titleId varchar(255),
   ordering int,
   nameId varchar(255),
   category varchar(255),
   job varchar(255),
   characters varchar(255),
   FOREIGN KEY (titleId) REFERENCES title_basics(titleId),
   FOREIGN KEY (nameId) REFERENCES crew_names(nameId),
   PRIMARY KEY (titleId, ordering)
);

CREATE TABLE title_ratings(
   titleId varchar(255),
   averageRating float,
   numVotes int NOT NULL DEFAULT 0
);

CREATE TABLE user_info(
   titleId varchar(255),
   owned BOOLEAN NOT NULL,
   lastWatched DATE,
   ownedFormat varchar(255) NOT NULL,
   FOREIGN KEY (titleId) REFERENCES title_basics(titleId)
   PRIMARY KEY (titleId)
);
