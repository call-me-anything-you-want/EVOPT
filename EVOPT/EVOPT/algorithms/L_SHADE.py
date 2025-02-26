import copy
import random
import numpy
import math
import multiprocessing

def generate_new_individual(func, problem_args, algorithm_args, current_population, i, M_CR, M_F, A):
    # generate parameters: CR, F, p
    r_i = random.randint(0, algorithm_args["H"] - 1)
    if M_CR[r_i] == algorithm_args["CR_terminal_value"]:
        CR_i = 0
    else:
        CR_i = numpy.random.normal(M_CR[r_i], 0.1)
        CR_i = max(CR_i, 0)
        CR_i = min(CR_i, 1)
    while True:
        F_i = numpy.random.standard_cauchy() * 0.1 + M_F[r_i]
        if F_i > 1:
            F_i = 1
            break
        elif F_i > 0:
            break
    # p_i = random.uniform(algorithm_args["p_min"], 0.2)
    p_i = algorithm_args["p"]

    # mutate
    sorted_current_population = sorted(
        current_population,
        key = lambda x: x.f_x,
    )
    x_pbest = random.choice(
        sorted_current_population[:math.ceil(p_i * len(current_population))]
    )
    r_1 = random.choice(list(range(0, i)) + list(range(i+1, len(current_population))))
    x_r1 = current_population[r_1]
    x_r2 = random.choice(
        [current_population[j] for j in range(len(current_population)) if j != r_1 and j != i]
        +
        [a for a in A if a not in sorted_current_population]
    )
    v_i = current_population[i] + F_i * (x_pbest - current_population[i]) + F_i * (x_r1 - x_r2)
    # if the mutant vector v is out of bounds, we need to project it back
    for j in range(problem_args["dimension"]):
        if v_i.x[j] < problem_args["bounds"][j][0]:
            v_i.x[j] = (problem_args["bounds"][j][0] + current_population[i].x[j]) / 2
        elif v_i.x[j] > problem_args["bounds"][j][1]:
            v_i.x[j] = (problem_args["bounds"][j][1] + current_population[i].x[j]) / 2

    # crossover
    j_rand = random.randint(0, problem_args["dimension"] - 1)
    trial_vector_x = numpy.array([
        v_i.x[j]
        if (random.random() <= CR_i or j == j_rand)
        else current_population[i].x[j]
        for j in range(problem_args["dimension"])
    ])
    current_trial_vector = func(trial_vector_x, index = current_population[i].index)

    # update population
    if current_trial_vector.f_x <= current_population[i].f_x:
        new_individual = current_trial_vector
    else:
        new_individual = current_population[i]

    # update A, S_CR and S_F
    new_A = None
    new_S_CR = None
    new_S_F = None
    new_S_weight = None
    if current_trial_vector.f_x < current_population[i].f_x:
        new_A = current_population[i]
        new_S_CR = CR_i
        new_S_F = F_i
        new_S_weight = abs(current_trial_vector.f_x - current_population[i].f_x)

    # NFE, new_individual (add to new_population), new_A, new_S_CR, new_S_F, new_S_weight
    return 1, new_individual, new_A, new_S_CR, new_S_F, new_S_weight

def L_SHADE(func, problem_args, algorithm_args):
    '''
    Input:
        func: a function that takes a vector as input and a Solution as output. It's the target that we are minimizing
        problem_args: a dict. It should contain the following key value pairs:
            "dimension": an int indicating the dimension of the problem
            "bounds": a list of list/tuple. It should be of size D * 2, with its ith entry indicating the bound of the ith dimension
            "MAX_NFE": the maximum number of function evaluation
        algorithm_args: a dict. It should contain the following key value pairs:
            "N_init": an int indicating the initial number of the population
            "r_arc": a float controlling the max size of A. |A| <= r_arc * N
            "H": an int indicating the size of M_CR and M_F
            "p": a float indicating the value of p, which effects the choice of pbest
            "CR_terminal_value": a special float for items in M_CR. Refer to the article for its meaning
            "N_min": an int indicating the minimum number of the population
    Output:
        optimal_solution: a Solution that is the best found so far.
        history_population: a list of list of Solutions, indicating the development of the population
    '''
    # initialization
    NFE = 0
    history_populations = []
    current_population = []
    dimension = problem_args["dimension"]
    for idx in range(algorithm_args["N_init"]):
        bound_array = numpy.array(problem_args["bounds"])
        random_x = numpy.random.uniform(
            bound_array[:dimension, 0],
            bound_array[:dimension, 1]
        )
        current_population.append(
            func(
                random_x,
                index = idx
            )
        )
        NFE += 1
    history_populations.append(copy.deepcopy(current_population))
    M_CR = [0.5] * algorithm_args["H"]
    M_F = [0.5] * algorithm_args["H"]
    A = set()
    k = 0

    # main loop
    while NFE < problem_args["MAX_NFE"]:
        print(f"{NFE} / {problem_args['MAX_NFE']}")
        print(f"best value: {min([a.f_x for a in current_population]).item()}")

        S_CR = []
        S_F = []
        S_weight = []

        # generate trial vectors and new population
        new_population = []

        results = []
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            async_results = [
                pool.apply_async(
                    generate_new_individual,
                    (func, problem_args, algorithm_args, current_population, i, M_CR, M_F, A)
                )
                for i in range(len(current_population))
            ]

            for async_result in async_results:
                results.append(async_result.get())
        pool.close()
        pool.join()

        for result in results:
            new_NFE, new_individual, new_A, new_S_CR, new_S_F, new_S_weight = result
            NFE += new_NFE
            new_population.append(new_individual)
            if new_A is not None:
                A.add(new_A)
            if new_S_CR is not None:
                S_CR.append(new_S_CR)
            if new_S_F is not None:
                S_F.append(new_S_F)
            if new_S_weight is not None:
                S_weight.append(new_S_weight)

        assert len(new_population) == len(set([a.index for a in new_population]))
        # update current population and save population to history
        current_population = new_population
        history_populations.append(copy.deepcopy(current_population))

        # clean A
        while len(A) > round(len(current_population) * algorithm_args["r_arc"]):
            A.remove(random.choice(list(A)))

        # update M_CR and M_F
        if len(S_CR) > 0 and len(S_F) > 0:
            S_weight_sum = sum(S_weight)
            S_weight = [w / S_weight_sum for w in S_weight]
            if M_CR[k] == algorithm_args["CR_terminal_value"] or max(S_CR) == 0:
                new_CR = algorithm_args["CR_terminal_value"]
            else:
                new_CR = sum([S_CR[i] * S_weight[i] for i in range(len(S_CR))])
            new_F = sum([S_F[i] * S_F[i] * S_weight[i] for i in range(len(S_F))]) / sum([S_F[i] * S_weight[i] for i in range(len(S_F))])
            M_CR[k] = new_CR
            M_F[k] = new_F
            k = (k + 1) % algorithm_args["H"]

        # LPSR
        new_population_num = round((algorithm_args["N_min"] - algorithm_args["N_init"]) / problem_args["MAX_NFE"] * NFE + algorithm_args["N_init"])
        while len(current_population) > new_population_num:
            current_population.remove(max(current_population, key = lambda x: x.f_x))

    return min(current_population, key = lambda x: x.f_x), history_populations

def get_L_SHADE_args(dimension):
    algorithm_args = {
        "N_init": round(dimension * 20),
        "r_arc": 2.0,
        "H": 5,
        "N_min": 4,
        "p": 0.1,
        "CR_terminal_value": 0
    }
    return algorithm_args
