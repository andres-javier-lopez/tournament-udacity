-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE tournament;
-- Creating the database
CREATE DATABASE tournament;
\c tournament

-- Players that participate in the tournament
-- Attributes:
--  id: unique identifier for a player
--  name: name of the player
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50)
);

-- Matches played on the tournament
-- Attributes
--  id_player1: first player participating on the match
--  id_player2: second player participatin on the match
--  id_winner: player who won the match
CREATE TABLE matches (
    id_player1 INTEGER NOT NULL REFERENCES players(id),
    id_player2 INTEGER NOT NULL REFERENCES players(id),
    id_winner INTEGER REFERENCES players(id),
    PRIMARY KEY (id_player1, id_player2)
);

-- View with the player standings
CREATE VIEW standings AS
SELECT players.id, players.name, won.won_matches, played.played_matches
FROM players
LEFT JOIN (SELECT players.id, count(matches.id_winner) as won_matches FROM players
LEFT JOIN matches ON players.id = matches.id_winner GROUP BY players.id) as won
ON won.id = players.id
LEFT JOIN (SELECT players.id, count(*) as played_matches FROM matches, players 
WHERE id_player1 = players.id OR id_player2 = players.id GROUP BY players.id) 
AS played ON players.id = played.id 
ORDER BY won_matches DESC;

-- Testing the database
-- INSERT INTO players (name) VALUES ('uno'), ('dos'), ('tres'), ('cuatro');
-- INSERT INTO matches VALUES (1,2,1), (3,4,3), (1,3,1), (2,4,2);
-- SELECT * FROM standings;
