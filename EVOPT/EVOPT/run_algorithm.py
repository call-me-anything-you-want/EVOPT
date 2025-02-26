from algorithms import get_algorithm_args, get_algorithm
from problems import evaluate_function, get_problem_args
from visualize import *
import tqdm
import argparse
import itertools

def test(x):
    return sum(xx ** 2 for xx in x)
test_args = {
    "dimension": 2,
    "bounds": [[-5, 5]] * 10,
    "MAX_NFE": 1000
    # "MAX_NFE": 100
}

def run_algorithm(algorithm_name, func_name, dimension = None):
    func = evaluate_function(func_name)
    problem_args = get_problem_args(func_name, dimension)

    algorithm = get_algorithm(algorithm_name)
    algorithm_args = get_algorithm_args(algorithm_name, problem_args["dimension"])

    best_solution, history_population = algorithm(func, problem_args, algorithm_args)
    print(f"Value of the best solution: {best_solution.f_x}")
    print(f"Position of the best solution: {best_solution.x}")
    return best_solution, history_population

if __name__ == "__main__":
    import algorithms
    available_algorithm_names = [a for a in dir(algorithms) if not a.startswith("_") and not a.startswith("get")]
    import problems
    available_problem_names = problems.AVAILABLE_PROBLEM_LIST
    parser = argparse.ArgumentParser(description="Run Algorithms on Given Problems")
    parser.add_argument(
        "-a",
        "--algorithm",
        type = str,
        nargs = "+",
        choices = available_algorithm_names,
        help = f"The algorithms that are currently supported are {available_algorithm_names}",
        required = True
    )
    parser.add_argument(
        "-p",
        "--problem",
        type = str,
        nargs = "+",
        choices = available_problem_names,
        help = f"The problems that are currently supported are {available_problem_names}",
        required = True
    )
    parser.add_argument(
        "-d",
        "--dimension",
        type = int,
        help = "The dimension of the problem. Please note that some problems have fixed dimension, in which case you should not explicitly use this argument.",
        default = None,
        required = False
    )
    parser.add_argument(
        "-v",
        "--visualize",
        type = bool,
        help = "Whether to visualize the result. Only supported for dimension of 2",
        required = False,
        default = False
    )
    args = parser.parse_args()

    algorithm_names = args.algorithm
    problem_names = args.problem
    dimension = args.dimension
    visualize = args.visualize

    if visualize:
        assert dimension == 2, "Visualize is only supported for 2 dimensional cases."

    for algorithm_name, problem_name in tqdm.tqdm(list(itertools.product(algorithm_names, problem_names))):
        print(f"Solving problem: {problem_name}")
        best_solution, history_populations = run_algorithm(algorithm_name, problem_name, dimension)
        save_path = f"./result/{algorithm_name}/{problem_name}.txt"
        save_best_solution_and_history_population(
            best_solution,
            history_populations,
            save_path
        )
        if visualize:
            save_path = f"./result/{algorithm_name}/{problem_name}_figs/"
            plot_history_population(problem_name, history_populations, save_path)
            save_gif(save_path, len(history_populations), f"{problem_name}_{algorithm_name}")