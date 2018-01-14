import numpy
from collections import defaultdict

"""
Create a function that prints a random number between 1 and 5 to stdout (or console). The probability distribution of the numbers should be as follows:

1 - 50%
2 - 25%
3 - 15%
4 - 5%
5 - 5%


numpy.random.choice(numpy.arange(1, 6), p=[0.5, 0.25, 0.15, 0.05, 0.05])

# good verification

random_number= defaultdict(int)
for i in (range(100)):
    random_number[numpy.random.choice(numpy.arange(1, 6), p=[0.5, 0.25, 0.15, 0.05, 0.05])] += 1
print random_number

"""
def random_number():
    rn=numpy.random.choice(numpy.arange(1, 6), p=[0.5, 0.25, 0.15, 0.05, 0.05])
    print rn

random_number()