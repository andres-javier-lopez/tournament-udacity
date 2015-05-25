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
        
def getQueryResult(sql):
    conn = connect()
    c = conn.cursor()
    try:
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

def countPlayers():
    """Returns the number of players currently registered."""
    result = getQueryResult("SELECT count(*) FROM players;")
    # The count value is the first (and only) column of the 
    # first (and only) row
    return result[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    try:
        # Using query parameters to prevent SQL injection
        c.execute("INSERT INTO players (name) values(%s)", (name,))
        conn.commit()
    finally:
        # Always close the connection
        conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """


