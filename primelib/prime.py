#!/usr/bin/env pypy
#
# Euler : Implementation for prime
# 
# <Module Summary statement>
#

__version__ = "0.1"
__author__ = 'Tony Flury : anthony.flury@btinternet.com'
__created__ = '27 Dec 2014'

"""
# Euler : Implementation of prime

Summary : 
    <A sieving prime number class>
Use Case : 
    As a <actor> I want <outcome> So that <justification>

Testable Statements :
    Can I test a prime number is real
    Can I identify all the prime factors of an integer
    Can I identify the nth prime number
"""
from itertools import product


class PrimeSieve():
    def __init__(self, size):
        """A prime number class based on the Sieve of Eratosthenes
        :param size: The size of the sieve
        :return Nothing
        :raise Nothing
        """
        self._sieve = self._primes = []
        self.resize(size)

    def _set_sieve(self):
        """ Private method to initialise the sieve
            pre-conditions :
                self._sieve is a list of known fixed size - filled with non-zeros -
                algorithm doesn't care what the value is.
            post-conditions : 
                self._sieve is a list of the same size with every entry set to zero if that index is a non-prime.
        """
        self._sieve[1] = 0  # 1 is never a prime

        # Traverse the rest of the sieve
        for i in xrange(2, len(self._sieve) - 1):
            # If the entry in the sieve isn't zero - traverse through the sieve from this point and
            # set every multiple to zero.
            if self._sieve[i] != 0:
                for n in xrange(i * 2, len(self._sieve), i):
                    self._sieve[n] = 0

    def resize(self, new_size):
        """Resize the Sieve to extend (or decrease) the range

        :param new_size: The new upper limit of the sieve
        :return: Nothing
        :raises Nothing
        """
        # Create the initial sieve - this might be more efficient to use a constant rather
        # that a variable to set up the sieve.
        self._sieve = [i for i in xrange(new_size + 1)]
        self._set_sieve()

        # Create a smaller list of primes based on the sieve.
        self._primes = [i for i in self._sieve if i != 0]

    def is_prime(self, x):
        """Return True if x is a prime within the defined Sieve limit

        :param x: The Integer to be tested
        :return: True if the Integer is a prime within the pre-defined range
        :raise: ValueError if the Integer is outside the range.
                IndexError if a -ve or floating point number is provided.
        """
        if (x >= len(self._sieve)) or (x < 1):
            raise ValueError("{1} is outside defined range (1 to {0})".format(len(self._sieve) - 1, x))

        if float(int(x)) != x:
            raise ValueError("{1} is not an integer in the defined range (1 to {0})".format(len(self._sieve) - 1, x))

        else:
            return self._sieve[x] != 0

    def nth_prime(self, n):
        """Return the nth prime - counting from 1
           :raises IndexError if the index is outside the list of primes generated
        """
        if n < 1:
            raise ValueError("Unable to get the {0}th prime".format(n))
        try:
            return self._primes[n - 1]
        except IndexError:
            raise ValueError("Only {0} primes in sieve - can't identify {1}th prime".format(len(self._primes), n))

    def __len__(self):
        """The number of primes identified in the Sieve"""
        return len(self._primes)

    def primes(self):
        for i in self._primes:
            yield i

    def factors(self, x):
        """Returns a 2-tuple of lists giving the prime factors and their exponents for the given value
           In the return value [factor],[exponent], exponent[n] is the exponent of factor[n]
        :param x: the Integer to be factorised
        :return: a 2-tuple of lists ([factor],[exponent]) giving all prime factors of the given Integer
        :raises IndexError if the value is too big to be factorised using the pre-defined Sieve
        """
        if x < 1:
            raise ValueError("Cannot factorise a value <1")

        if x > max(self._primes) ** 2:
            raise IndexError("Outside initialised range {0}".format(len(self._sieve) - 1))

        factors = []
        exponents = []

        if x in self._primes:
            return [x], [1]

        rem = x

        for i in self._primes:

            if x % i == 0:
                exp = 0
                while rem % i == 0:
                    exp, rem = exp + 1, rem / i
                factors.append(i)
                exponents.append(exp)

            if rem == 1:
                return factors, exponents

        return factors, exponents

    def divisors(self, n):
        """Generate a list of all proper divisors of n - i.e. all integers which divide n which are <n

        :param n: The integer for which to find divisors
        :return: The list of proper divisors of n which are less than n
        """
        fac, exp = self.factors(n)

        # Combine the factorial and exponents list into a single list of all combinations
        # The logic here is complex and not easily described

        p = [j for j in product(*[[i for i in product([f], range(0, e + 1))] for f, e in zip(fac, exp)])]

        # Calculate the combinations for factors and exponents
        factors = [reduce(lambda d, v: d * v, [t[0] ** t[1] for t in e], 1) for e in p]
        return sorted([i for i in factors if i < n])

if __name__ == "__main__":

    import sys
    a = PrimeSieve(500000000)
    with open('prime_500000000.txt', 'w') as p:
        for i in a.primes():
            p.write(str(i) + '\n')

    import unittest
    import timeit

    class BasicTests(unittest.TestCase):
        def setUp(self):
            # List fetched from https://primes.utm.edu/lists/small/10000.txt
            with open('10000.txt') as primes_data:
               self.results = [int(p.strip()) for line in primes_data for p in line.split()] 

            self.Primes = PrimeSieve(self.results[-1]+1)  # Test with primes up to the last value.

        def test_01_00_basic_primes_1_to_1000(self):
            for i in range(1, 100):
                self.assertEqual(self.Primes.is_prime(i), i in self.results,
                                 "Test failed for primality of {0}".format(i))
            self.assertEqual(len(self.Primes), len(self.results))

        def test_01_01_basic_primes_1_to_end(self):
            for i in range(1, self.results[-1]+1):
                self.assertEqual(self.Primes.is_prime(i), i in self.results,
                                 "Test failed for primality of {0}".format(i))

        def test_02_01_errors(self):
            # The sieve can only handle numbers from 1 to it's limit. The sieve is not dynamic.
            self.assertRaises(ValueError, self.Primes.is_prime, self.results[-1]+2)
            self.assertRaises(ValueError, self.Primes.is_prime, 0)

            # The sieve only handles integers
            self.assertRaises(ValueError, self.Primes.is_prime, 1.3)

            # Test that nth_prime won't return the 0th prime - counting starts from one.
            self.assertRaises(ValueError, self.Primes.nth_prime, 0)

            # Test that nth_prime won't return a prime beyond the end of the sieve
            self.assertRaises(ValueError, self.Primes.nth_prime, len(self.results) + 1)

        def test_03_01_nth_primes(self):
            for index, p in enumerate(self.results):
                self.assertEqual(self.Primes.nth_prime(index + 1), self.results[index])

        def test_04_01_prime_list(self):
            p_list = [i for i in self.Primes.primes()]
            self.assertSequenceEqual(p_list, self.results)

        def test_05_01_factors(self):
            for num in range(2, self.results[-1]+1):
                # These loops emulate create list of simple factors - fac**exp
                facs, exps = self.Primes.factors(num)
                for fac, exp in zip(facs, exps):
                    for ex in range(1, exp + 1):
                        self.assertEqual(num % (fac ** ex), 0,
                                         "Factor of {0} : {1}, {2} - testing {1}**{3} - not a divisor".format(
                                             num, fac, exp, ex))

        def test_05_02_divisors(self):
            for num in range(2, self.results[-1]+1):
                for d in self.Primes.divisors(num):
                    self.assertEqual(num % d, 0, "Divisor of {0} stated as {1}".format(num, d))

    suite = unittest.TestLoader().loadTestsFromTestCase(BasicTests)
    print(timeit.timeit( 'unittest.TextTestRunner(verbosity=2).run(suite)', number=1,setup="from __main__ import unittest,suite"))
  
    
