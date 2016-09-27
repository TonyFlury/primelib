.. image:: https://travis-ci.org/TonyFlury/primelib.png?branch=master
    :target: https://travis-ci.org/TonyFlury/primelib/

=======================================================
Primelib : prime number sieve and related functions
=======================================================

A resizable sieve of Eratosthenes and related mathematical methods

Rationale
---------

This library started as a way to bring together a number of different functions, methods, classes and code snippets written by the author to solve a number project Euler problem. The library is intended to meet the following UseCase :

UseCase Statement : As a developer I want a reusable prime number library so that I can reduce development time


Basic Usage
-----------
.. code-block::

    >>> from primelib.prime import PrimeSieve as Sieve
    >>> sieve = Sieve(3000) # Initialise the sieve from 1 to 3000
    >>> sieve.is_prime(23)
    True
    >>> sieve.is_prime(21)
    False
    >>> sieve.nth_prime(5)
    11
    >>> [p for p in sieve.primes() if p<=15]
    [2, 3, 5, 7, 11, 13]
    >>> p.factors(90) # 90 = 2 * 3 * 2 * 5
    ([2,3,5],[1,2,1])
    >>> p.divisors(28)
    [2, 4, 7, 14, 28]

Further Details
---------------

- `Full Documentation <http://primelib.readthedocs.org/en/latest/>`_
- `On PyPi (Python Package Index) <https://pypi.python.org/pypi/primelib>`_
- `Source code on GitHub <http://github.com/TonyFlury/primelib>`_

+---------------------------------------------------------------------------------------------+
|                                            *Bugs*                                           |
+=============================================================================================+
| Every care is taken to try to ensure that this code comes to you bug free.                  |
| If you do find an error - please report the problem on :                                    |
| `GitHub <http://github.com/TonyFlury/primelib>`_                                            |
| or                                                                                          |
| by email to : `Tony Flury <mailto:anthony.flury@btinternet.com?Subject=primelib%20Error>`_  |
+---------------------------------------------------------------------------------------------+
