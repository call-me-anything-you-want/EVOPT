import numpy
DEFAULT_DIMENSION = 30

import math
def Bent_Cigar(x):
    # Bent Cigar Function
    return x[0] ** 2 + 1e6 * (x[1:] ** 2).sum()

def get_Bent_Cigar_args(dimension):
    if dimension is None:
        dimension = DEFAULT_DIMENSION
    return {
        "dimension": dimension,
        "bounds": [[-100, 100]] * dimension,
        "MAX_NFE": 10000 * dimension
    }

def Ackley(x):
    # ackley's function
    return -20 * numpy.exp(-0.2 * numpy.sqrt(1 / len(x) * (x ** 2).sum())) - numpy.exp(1 / len(x) * numpy.cos(2 * numpy.pi * x).sum()) + 20 + numpy.e

def get_Ackley_args(dimension):
    if dimension is None:
        dimension = DEFAULT_DIMENSION
    return{
        "dimension": dimension,
        "bounds": [[-100, 100]] * dimension,
        "MAX_NFE": 10000 * dimension
    }

def Rastrigin(x):
    # rastrigin's function
    return (x ** 2 - 10 * numpy.cos(2 * numpy.pi * x) + 10).sum()

def get_Rastrigin_args(dimension):
    if dimension is None:
        dimension = DEFAULT_DIMENSION
    return {
        "dimension": dimension,
        "bounds": [[-100, 100]] * dimension,
        "MAX_NFE": 10000 * dimension
    }
