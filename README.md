Tournament Udacity
=============

This is a backend for managing a swiss pairing tournament.

== Vagrant ==
Project is bundled within vagrant, I won't go into details on how to setup 
vagrant, but to run it you just need the following commands:
`vagrant up`
`vagrant ssh`

== Installing the system ==

The database is writing for PostgreSQL, to install it from the command line
use:
`psql -f vagrant/tournament/tournament.sql`

== Runnig the test suite ==

To run the test suite use the following command:
`python vagrant/tournament/tournament_test.py`

== Using the system ==

To use the application, you can import tournaments.py on your python project 
or you can import it from python interpreter and use it directly.
