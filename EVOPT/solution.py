class Solution:
    def __init__(self, x = None, f_x = None, index = None):
        self.x = x
        self.f_x = f_x
        self.index = index

    def __eq__(self, other):
        return all(self.x == other.x)

    def __hash__(self):
        return hash(tuple(self.x.tolist()))

    def __add__(self, other):
        assert self.x.shape == other.x.shape
        assert (self.index is None) != (other.index is None)
        return Solution(
            self.x + other.x,
            None,
            self.index if self.index is not None else other.index
        )

    def __sub__(self, other):
        assert self.x.shape == other.x.shape
        return Solution(
            self.x - other.x,
            None,
            None
        )

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Solution(
                other * self.x,
                None,
                self.index
            )

    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Solution(
                other * self.x,
                None,
                self.index
            )

    def __str__(self):
        return f"idx: {self.index}; x: {self.x.tolist() if self.x is not None else None}; f(x): {self.f_x.item() if self.f_x is not None else None}"

class Constraint_Solution(Solution):
    def __init__(self, x = None, f_x = None, index = None, func_value = None, penalty = None):
        self.x = x
        self.f_x = f_x
        self.index = index
        self.func_value = func_value
        self.penalty = penalty
    
    def __str__(self):
        return f"idx: {self.index}; x: {self.x.tolist() if self.x is not None else None}; f(x): {self.f_x.item() if self.f_x is not None else None}; original f(x): {self.func_value.item() if self.func_value is not None else None}; penalty: {self.penalty if self.penalty is not None else None}"
