#!/usr/bin/env python
# coding=utf-8
"""
# primelib : prime number sieve and related functions

Summary :
    A resizable sieve of Erathonese and related mathematical methods
Use Case :
    As a developer I want a reusable prime number library so that I can reduce development time

Testable Statements :
    ...
"""
from primelib.prime import PrimeSieve as Sieve
import unittest
from operator import mul

__author__ = "Tony Flury anthony.flury@btinternet.com"
__created__ = "27 Sep 2016"

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]


def add_methods(*test_methods):
    """
    Class Decorator designed to allow the simple construction of many test cases.

    test_method : a function object which actually creates one or more test cases
    """
    def decorator(klass):
        for method in test_methods:
            for test_input in method():
                setattr(klass, test_input.__name__, test_input)
        return klass

    return decorator


def make_nth_prime_test(idx,val):
    """Make a test case function object to check the nth prime method"""
    def test_nth_prime(self):
        self.assertEqual(self.s.nth_prime(idx+1), val)

    test_nth_prime.__name__ = 'test_nth_prime_{input:03d}'.format(input=idx)
    test_nth_prime.__doc__ = "Testing that the {:03d}th prime matches the same index in the prime list".format(idx)
    return test_nth_prime


def nth_prime_test( ):
    """Create an nth prime test for every prime upto 1000 (168 tests)"""
    for idx, val in enumerate(primes):
        yield make_nth_prime_test(idx,val)


def make_integer_prime_test(i):
    """Build a test case function object to test primarilty of integer is correctly reported"""
    def test_integer_is_prime(self):
        self.assertTrue(self.s.is_prime(i))

    def test_integer_is_not_prime(self):
        self.assertFalse(self.s.is_prime(i))

    if i in primes:
        test_integer_is_prime.__name__ = 'test_{input:03d}_is_prime'.format(input=i)
        test_integer_is_prime.__doc__ = "Testing that {:03d} is correctly marked as a prime".format(i)
        return test_integer_is_prime
    else:
        test_integer_is_not_prime.__name__ = 'test_{input:03d}_is_not_prime'.format(input=i)
        test_integer_is_not_prime.__doc__ = "Testing that {:03d} is correctly marked as not a prime".format(i)
        return test_integer_is_not_prime


def all_integers():
    """Construct function object to test primality of integers upto 1000"""
    for i in range(1,1001):
        yield make_integer_prime_test(i)


def make_factor_test(n):
    """Construct function object to test factorisation of integers upto 1000
       Also checks that the reported prime factors are truely primes
    """
    def test_factors(self):
        factors = self.s.factors(n)
        for f in factors[0]:
            self.assertTrue(f in primes, "{} reported as prime factor for {}".format(f,n))

        v =reduce(mul,[i[0]**i[1] for i in zip(factors[0], factors[1])],1)
        self.assertEqual(n,v,msg="Reported factors for {} : {}".format(n,factors))

    test_factors.__name__ = 'test_{input:03d}_is_correctly_factorised'.format(input=n)
    test_factors.__doc__ = "Testing that {:03d} is correctly factorised".format(n)
    return test_factors


def all_factors():
    """Construct function object to test factorisation of integers upto 1000"""
    for i in range(1,1001):
        yield make_factor_test(i)

@add_methods(nth_prime_test)    # Test that the nth_prime method works
@add_methods(all_integers)      # Test that all integers upto 1000 are correctly identified
@add_methods(all_factors)       # Test that all integers are factorised correctly
class Sieve_Test(unittest.TestCase):
    def setUp(self):
        self.s = Sieve(1000)

if __name__ == '__main__':
    unittest.main(verbosity=2)