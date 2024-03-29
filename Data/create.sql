CREATE TABLE title_basics(
   titleId varchar(255) PRIMARY KEY,
   titleType varchar(255),
   primaryTitle text NOT NULL,
   originalTitle text NOT NULL,
   isAdult BOOLEAN NOT NULL,
   startYear SMALLINT CHECK (startYear<=9999 AND startYear>1800),
   endYear SMALLINT CHECK (endYear<=9999 AND endYear>1800),
   runtime int
);

CREATE TABLE title_genre(
   titleId varchar(255),
   genre varchar(255),
   FOREIGN KEY (titleId) REFERENCES title_basics(titleId),
   PRIMARY KEY (titleId, genre)
);

CREATE TABLE title_akas(
   titleId varchar(255),
   ordering int,
   title text NOT NULL,
   region varchar(255),
   language varchar(255),
   isOriginalTitle BOOLEAN,
   FOREIGN KEY (titleId) REFERENCES title_basics(titleId),
   PRIMARY KEY (titleId, ordering)
);

CREATE TABLE title_attributes(
   titleId varchar(255),
   ordering int,
   attId int,
   attribute varchar(255),
   FOREIGN KEY (titleId, ordering) REFERENCES title_akas(titleId, ordering),
   PRIMARY KEY (titleId, ordering, attId)
);

CREATE TABLE crew_names(
   nameId varchar(255) PRIMARY KEY,
   name varchar(255),
   birthYear SMALLINT,
   deathYear SMALLINT
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
   FOREIGN KEY (writer) REFERENCES crew_names(nameId),
   PRIMARY KEY (titleId, writer)
);

CREATE TABLE title_episodes(
   episodeId varchar(255),
   titleId varchar(255),
   parentId varchar(255),
   seasonNumber int,
   episodeNumber int,
   FOREIGN KEY (titleId) REFERENCES title_basics(titleId),
   FOREIGN KEY (parentId) REFERENCES title_basics(titleId),
   PRIMARY KEY (episodeId)
);

CREATE TABLE title_principals(
   titleId varchar(255),
   ordering int,
   nameId varchar(255),
   category varchar(255),
   job varchar(255),
   FOREIGN KEY (titleId) REFERENCES title_basics(titleId),
   FOREIGN KEY (nameId) REFERENCES crew_names(nameId),
   PRIMARY KEY (titleId, ordering, nameId)
);

CREATE TABLE title_characters(
   titleId varchar(255),
   ordering int,
   nameId varchar(255),
   charId int,
   character_name varchar(255),
   FOREIGN KEY (titleId, ordering, nameId) REFERENCES title_principals(titleId, ordering, nameId),
   PRIMARY KEY (titleId, ordering, nameId, charId)
);

CREATE TABLE title_ratings(
   titleId varchar(255),
   averageRating float,
   numVotes int DEFAULT 0
);

CREATE TABLE format(
   fid int PRIMARY KEY,
   format varchar(255) NOT NULL
);

CREATE TABLE user_info(
   titleId varchar(255),
   owned BOOLEAN DEFAULT FALSE,
   lastWatched DATE,
   ownedFormat int,
   FOREIGN KEY (titleId) REFERENCES title_basics(titleId),
   FOREIGN KEY (ownedFormat) REFERENCES format(fid),
   PRIMARY KEY (titleId)
);
