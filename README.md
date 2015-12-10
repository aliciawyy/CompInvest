Computational Investment Tools
==============================

This repository stores some computational investment tools writen in Python based on [QSToolKits](http://wiki.quantsoftware.org/index.php?title=QuantSoftware_ToolKit).

It mainly includes tools of

* Portfolio analyzer and optimizer
* Market similator for backtesting
* Event profiler

The code is on refactoring ... 10 Dec 2015

All the unit tests will be ranged in the repository tests, and a .git/hooks/pre-commit will be set
to run all the tests which are not tagged as "slow" before each commit.