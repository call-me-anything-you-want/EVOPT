from .SHADE import SHADE, get_SHADE_args
from .L_SHADE import L_SHADE, get_L_SHADE_args
from .D_SHADE import D_SHADE, get_D_SHADE_args
from .LARC_SHADE import LARC_SHADE, get_LARC_SHADE_args

def get_algorithm(algo_name):
    return eval(algo_name)

def get_algorithm_args(algo_name, dimension):
    return eval(f"get_{algo_name}_args")(dimension)
