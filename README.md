CircusPoker
===========

A Texas-holdem pokerimplementation written in Python 3.x using a simple text based user interface. It is an
online debugging tool, you see all the cards and control all actions.

Note: it's the first version that seems to work in most cases, but there are cases that will fail.
There is currently no compilation of known issues.

Using CircusPoker
-----------------

Start the program with python circuspoker.py.
A card is described with two characters, its value and its suite.
Value is a number or T for 10, J for jack, Q for queen, K for king, and A for ace.
Suite is c for club, d for diamond, h for heart, s for spade.

+ means player to act, - means dealer.

There are four commands, fold, call, check, and raise.

If you do a raise, you are then asked to enter the amount that you raise to. If someone has raised
300, and you want to raise another 300, you enter an amount of 600.

The cards belonging to a player is removed when the player folds.

There is no information in the game about who wins the pot, the chips left is directly updated.

When there is only one player left, Game over is written. No information who won the game is presented.

The implementation
------------------

The implementation implements a lot of logic in pure functions in isolated files.

The tests for each pure function is incomplete, and does not use any testing framework,
that will be fixed in a later version.

There are no smoke tests for the complete poker engine, that will also be added in a later version.

Some code refactoring to remove duplicated code etc would be nice. The code does not follow PEP8 yet.

There is no code documentation.
