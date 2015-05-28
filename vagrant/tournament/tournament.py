#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def query(sql):
    """Executes a query on the database. Doesn't return any result."""
    conn = connect()
    c = conn.cursor()
    try:
        c.execute(sql)
        conn.commit()
    finally:
        # Always close the connection
        conn.close()


def getQueryResult(sql, vars=None):
    conn = connect()
    c = conn.cursor()
    try:
        if vars:
            c.execute(sql, vars)
        else:
            c.execute(sql)
        result = c.fetchall()
        return result
    finally:
        # Always close the connection
        conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    query("DELETE FROM matches;")


def deletePlayers():
    """Remove all the player records from the database."""
    query("DELETE FROM players;")


def deleteTournaments():
    """Remove all the tournaments from the database."""
    query("DELETE FROM tournaments;")


def countPlayers():
    """Returns the number of players currently registered."""
    result = getQueryResult("SELECT count(*) FROM players;")
    # The count value is the first (and only) column of the
    # first (and only) row
    return result[0][0]


def registerTournament(name):
    """Adds a tournament to the database.

    Each tournament has its own set of players and matches.

    Args:
        name: Name of the tournament.
    """
    conn = connect()
    c = conn.cursor()
    try:
        # Using query parameters to prevent SQL injection
        c.execute(("INSERT INTO tournaments (name) "
                   "values (%s) RETURNING id"), (name,))
        conn.commit()
        return c.fetchone()[0]
    finally:
        # Always close the connection
        conn.close()


def registerPlayer(id_tournament, name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
        id_tournament: id of the current tournament.
        name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    try:
        # Using query parameters to prevent SQL injection
        c.execute("INSERT INTO players (id_tournament, name) values(%s, %s)", (
            id_tournament, name
        ))
        conn.commit()
    finally:
        # Always close the connection
        conn.close()


def playerStandings(id_tournament):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Args:
        id_tournament: Id of the tournament which you want to get the
        standings.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    result = getQueryResult(
        ("SELECT id, name, won_matches, played_matches "
         "FROM standings WHERE id_tournament = %s;"),
        (id_tournament,)
    )
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO matches VALUES (%s, %s, %s)", (
            winner, loser, winner
        ))
        conn.commit()
    finally:
        conn.close()


def swissPairings(id_tournament):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
        id_tournament: The id of the current tournament.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings(id_tournament)

    i = 0
    pairing = []
    while i < len(standings):
        pairing.append((standings[i][0], standings[i][1],
                        standings[i + 1][0], standings[i + 1][1]))
        i = i + 2

    return pairing
