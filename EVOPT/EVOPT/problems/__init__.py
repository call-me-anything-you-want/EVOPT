from . import cec_2014
from . import engineering_problems
from EVOPT import solution

PENALTY_COEF = 100
AVAILABLE_PROBLEM_LIST = [
    p for p in dir(cec_2014) if not p.startswith("_") and not p.startswith("get") and p[0].isupper() and not p.isupper()
] + [
    p for p in dir(engineering_problems) if not p.startswith("_") and not p.startswith("get") and p[0].isupper() and not p.isupper()
]

class evaluate_function:
    def __init__(self, func_name):
        self.func_name = func_name

    def __call__(self, x, index = None):
        if hasattr(cec_2014, self.func_name):
            return solution.Solution(
                x,
                getattr(cec_2014, self.func_name)(x),
                index
            )
        elif hasattr(engineering_problems, self.func_name):
            func_value, penalty = getattr(engineering_problems, self.func_name)(x)
            return solution.Constraint_Solution(
                x,
                func_value + PENALTY_COEF * sum([max(p, 0) for p in penalty]),
                index,
                func_value,
                penalty
            )

def get_problem_args(func_name, dimension):
    if hasattr(cec_2014, func_name):
        return getattr(cec_2014, f"get_{func_name}_args")(dimension)
    elif hasattr(engineering_problems, func_name):
        return getattr(engineering_problems, f"get_{func_name}_args")(dimension)