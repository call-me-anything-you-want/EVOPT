import numpy
PENALTY_COEF = 100

def Cantilever_Beam(x):
    func_value = 0.0624 * x.sum()
    penalty_coef = numpy.array([61, 37, 19, 7, 1])
    penalty = (penalty_coef / (x ** 3)).sum() - 1
    return func_value, [penalty]

def get_Cantilever_Beam_args(dimension):
    assert dimension == 5 or dimension is None, "Cantilever Beam only supports dimension of 5."
    return {
        "dimension": 5,
        "bounds": [[0.01, 100]] * 5,
        "MAX_NFE": 12000
    }

def I_Shaped_Beam(x):
    func_value = 5000 / (x[2] * (x[1] - 2 * x[3]) ** 3 / 12 + (x[0] * x[3] ** 3 / 6) + 2 * x[0] * x[3] * (x[1] - x[3] / 2) ** 2)
    penalty_1 = 2 * x[0] * x[2] + x[2] * (x[1] - 2 * x[3]) - 300
    penalty_2 = 18 * x[1] * 1e4 / (x[2] * (x[1] - 2 * x[3]) ** 3 + 2 * x[0] * x[2] * (4 * x[3] ** 2 + 3 * x[1] * (x[1] - 2 * x[3]))) + 15 * x[0] * 1e3 / ((x[1] - 2 * x[3]) * x[2] ** 2 + 2 * x[2] * x[0] ** 3) - 56
    return func_value, [penalty_1, penalty_2]

def get_I_Shaped_Beam_args(dimension):
    assert dimension == 4 or dimension is None, "I Shaped Beam only supports dimension of 4."
    return {
        "dimension": 4,
        "bounds": [
            [10, 50],
            [10, 80],
            [0.9, 5],
            [0.9, 5]
        ],
        "MAX_NFE": 3600
    }

def Tubular_Column(x):
    # original article not clear
    P = 2000
    l = 100
    sigma_y = 500
    E = 0.85 * 1e6
    func_value = 9.8 * x[0] * x[1] + 2 * x[0]
    penalty_1 = P / (numpy.pi * x[0] * x[1] * sigma_y) - 1
    penalty_2 = 8 * P * l ** 2 / (numpy.pi ** 3 * E * x[0] * x[1] * (x[0] ** 2 + x[1] ** 2)) - 1
    penalty_3 = 2 / x[0] - 1
    penalty_4 = x[0] / 14 - 1
    penalty_5 = 0.2 / x[1] - 1
    penalty_6 = x[1] / 8 - 1
    return func_value, [penalty_1, penalty_2, penalty_3, penalty_4, penalty_5, penalty_6]

def get_Tubular_Column_args(dimension):
    assert dimension == 2 or dimension is None, "Tubular Column only supports dimension of 2."
    return {
        "dimension": 2,
        "bounds": [
            [2, 14],
            [0.2, 0.8]
        ],
        "MAX_NFE": 1250
    }

def Piston_Lever(x):
    theta = numpy.pi / 4
    Q = 1e4
    L = 240
    M_max = 1.8 * 1e6
    P = 1500
    R = numpy.abs(- x[3] * (x[3] * numpy.sin(theta) + x[0]) + x[0] * (x[1] - x[3] * numpy.cos(theta))) / numpy.sqrt((x[3] - x[1]) ** 2 + x[0] ** 2)
    F = numpy.pi * P * x[2] ** 2 / 4
    L_1 = numpy.sqrt((x[3] - x[1]) ** 2 + x[0] ** 2)
    L_2 = numpy.sqrt((x[3] * numpy.sin(theta) + x[0]) ** 2 + (x[1] - x[3] * numpy.cos(theta)) ** 2)
    func_value = 1 / 4 * numpy.pi * x[2] ** 2 * (L_2 - L_1)
    penalty_1 = Q * L * numpy.cos(theta) - R * F
    penalty_2 = Q * (L - x[3]) - M_max
    penalty_3 = 1.2 * (L_2 - L_1) - L_1
    penalty_4 = x[2] / 2 - x[1]
    return func_value, [penalty_1, penalty_2, penalty_3, penalty_4]

def get_Piston_Lever_args(dimension):
    assert dimension == 4 or dimension is None, "Piston Lever only supports dimension of 4."
    return {
        "dimension": 4,
        "bounds": [
            [0.05, 500],
            [0.05, 500],
            [0.05, 120],
            [0.05, 500],
        ],
        "MAX_NFE": 5000
    }

def Corrugated_Bulkhead(x):
    func_value = 5.885 * x[3] * (x[0] + x[2]) / (x[0] * numpy.sqrt(numpy.abs(x[2] ** 2 - x[1] ** 2)))
    penalty_1 = - x[3] * x[1] * (0.4 * x[0] + x[2] / 6) + 8.94 * (x[0] + numpy.sqrt(numpy.abs(x[2] ** 2 - x[1] ** 2)))
    penalty_2 = - x[3] * x[1] ** 2 * (0.2 * x[0] + x[2] / 12) + 2.2 * (8.94 * (x[0] + numpy.sqrt(numpy.abs(x[2] ** 2 - x[1] ** 2)))) ** (4 / 3)
    penalty_3 = - x[3] + 0.0156 * x[0] + 0.15
    penalty_4 = - x[3] + 0.0156 * x[2] + 0.15
    penalty_5 = - x[3] + 1.05
    penalty_6 = - x[2] + x[1]
    return func_value, [penalty_1, penalty_2, penalty_3, penalty_4, penalty_5, penalty_6]

def get_Corrugated_Bulkhead_args(dimension):
    assert dimension == 4 or dimension is None, "Corrugated Bulkhead only supports dimension of 4."
    return {
        "dimension": 4,
        "bounds": [
            [0, 100],
            [0, 100],
            [0, 100],
            [0, 5],
        ],
        "MAX_NFE": 3125
    }

def Tension_Compression_Spring(x):
    # original article not clear
    func_value = (x[2] + 2) * x[1] * x[0] ** 2
    penalty_1 = 1 - x[1] ** 3 * x[2] / (71785 * x[0] ** 4)
    penalty_2 = (4 * x[1] ** 2 - x[0] * x[1]) / (12566 * (x[1] * x[0] ** 3 - x[0] ** 4)) + 1 / (5108 * x[0] ** 2) - 1
    penalty_3 = 1 - 140.45 * x[0] / (x[1] ** 2 * x[2])
    penalty_4 = (x[0] + x[1]) / 1.5 - 0.26
    return func_value, [penalty_1, penalty_2, penalty_3, penalty_4]

def get_Tension_Compression_Spring_args(dimension):
    assert dimension == 3 or dimension is None, "Tension Compression only supports dimension of 3."
    return {
        "dimension": 3,
        "bounds": [
            [0.05, 2],
            [0.25, 1.3],
            [2, 15],
        ],
        "MAX_NFE": 9000
    }
