"""Test suites corresponding to the all the 2009 QSNMC competition."""

from sciunit import TestSuite

import ..tests as tests

##########
# Suites #
##########

a = TestSuite(tests.year2009.a.tests)
b = TestSuite(tests.year2009.b.tests)
c = TestSuite(tests.year2009.c.tests)
d = TestSuite(tests.year2009.d.tests)

