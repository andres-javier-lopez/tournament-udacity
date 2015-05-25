-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

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
SELECT players.id, players.name, count(matches.id_winner) as won_matches
FROM players LEFT JOIN matches ON players.id = matches.id_winner
GROUP BY players.id
ORDER BY won_matches;
