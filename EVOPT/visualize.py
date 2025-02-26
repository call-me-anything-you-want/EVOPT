from matplotlib import pyplot
import imageio
import os
import numpy
import multiprocessing
from problems import evaluate_function, get_problem_args

def save_one_fig(grid_x, grid_y, z, current_pop, total_pop_num, color_map, fig_save_path):
    pyplot.figure()
    pyplot.contourf(grid_x, grid_y, z, levels=20)
    for solution in current_pop:
        pyplot.scatter(solution.x[0], solution.x[1], color = color_map(solution.index / total_pop_num))
    print(f"Saving figure to {fig_save_path}")
    pyplot.savefig(fig_save_path)
    pyplot.close()

def plot_history_population(func_name, history_population, fig_save_path):
    if not os.path.isdir(fig_save_path):
        os.makedirs(fig_save_path)

    dimension = len(history_population[0][0].x)

    func = evaluate_function(func_name)
    problem_args = get_problem_args(func_name, dimension=dimension)
    assert problem_args["dimension"] == 2
    x = numpy.arange(
        problem_args["bounds"][0][0],
        problem_args["bounds"][0][1],
        (problem_args["bounds"][0][1] - problem_args["bounds"][0][0]) / 1e3,
    )
    y = numpy.arange(
        problem_args["bounds"][1][0],
        problem_args["bounds"][1][1],
        (problem_args["bounds"][1][1] - problem_args["bounds"][1][0]) / 1e3,
    )
    grid_x, grid_y = numpy.meshgrid(x, y)
    z = numpy.zeros_like(grid_x)
    for i in range(z.shape[0]):
        for j in range(z.shape[1]):
            z[i][j] = func(numpy.array([grid_x[i][j], grid_y[i][j]])).f_x

    color_map = pyplot.get_cmap("rainbow")
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        async_results = [
            pool.apply_async(
                save_one_fig,
                (grid_x, grid_y, z, pop, len(history_population[0]), color_map, f"{fig_save_path}/{idx}.jpg")
            )
            for idx, pop in enumerate(history_population)
        ]
        for r in async_results:
            r.get()
    pool.close()
    pool.join()

def save_gif(fig_save_path, fig_num, gif_name):
    print("saving gif")
    frames = []
    for idx in range(fig_num):
        im = imageio.v2.imread(f"{fig_save_path}/{idx}.jpg")
        frames.append(im)
    imageio.mimsave(
        f"{fig_save_path}/{gif_name}.gif",
        frames,
        duration = 1,
    )

def save_best_solution_and_history_population(best_solution, history_populations, save_path):
    print("saving best solution and history population")
    save_dir = os.path.dirname(save_path)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    with open(save_path, "a+") as f:
        f.write(f"best solution: {best_solution}\n")
        for pop in history_populations:
            f.write("=======================\n")
            for solution in pop:
                f.write(f"{solution}\n")
