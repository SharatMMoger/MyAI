import math

def square_root(number):
    return math.sqrt(number)

def power(base, exponent):
    return base ** exponent

def factorial(number):
    return math.factorial(number)

def gcd(a, b):
    return math.gcd(a, b)

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def percentage(percent, value):
    return (percent / 100) * value 
    
import math

def sine(angle):
    return math.sin(math.radians(angle))

def cosine(angle):
    return math.cos(math.radians(angle))

def tangent(angle):
    return math.tan(math.radians(angle)) 
     
import statistics

def mean(numbers):
    return statistics.mean(numbers)

def median(numbers):
    return statistics.median(numbers)

def mode(numbers):
    return statistics.mode(numbers)

def variance(numbers):
    return statistics.variance(numbers)

def stddev(numbers):
    return statistics.stdev(numbers)
    import math

def npr(n, r):
    return math.perm(n, r)

def ncr(n, r):
    return math.comb(n, r)

def probability(favorable, total):
    return favorable / total
    
def complex_add(a, b):
    return complex(a) + complex(b)

def complex_mul(a, b):
    return complex(a) * complex(b)

def complex_abs(a):
    return abs(complex(a))

def complex_conj(a):
    return complex(a).conjugate()

# Complex Numbers

def complex_add(a, b):
    return complex(a) + complex(b)

def complex_mul(a, b):
    return complex(a) * complex(b)

def complex_abs(a):
    return abs(complex(a))

def complex_conj(a):
    return complex(a).conjugate()
    
# Vectors

def vector_add(v1, v2):
    return [a + b for a, b in zip(v1, v2)]

def dot_product(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))

def magnitude(v):
    return sum(x**2 for x in v) ** 0.5

def unit_vector(v):
    mag = magnitude(v)
    return [x / mag for x in v]

def cross_product(v1, v2):
    return [
        v1[1]*v2[2] - v1[2]*v2[1],
        v1[2]*v2[0] - v1[0]*v2[2],
        v1[0]*v2[1] - v1[1]*v2[0]
    ]

# Coordinate Geometry

def distance(p1, p2):
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) ** 0.5

def midpoint(p1, p2):
    return [
        (p1[0] + p2[0]) / 2,
        (p1[1] + p2[1]) / 2
    ]

def slope(p1, p2):
    return (p2[1] - p1[1]) / (p2[0] - p1[0])