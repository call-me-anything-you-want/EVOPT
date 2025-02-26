# EVOPT
EVOPT is a python package designed to run EVOlutionary OPTimization algorithms. We have implemented several algorithms and test functions that can be use out of the box.

## Getting started
To install this package, first you need to download this folder to your computer. Currently, we do not support installing online.

After that, create your new python environment. We suggest using python 3.10. Other versions of python have not been tested.

You can run the following command to create your environment using conda.
```bash
conda create -n EVOPT python=3.10
```

After that, you should activate your environment.
```bash
conda activate EVOPT
```

Next, you need to install this package. Simply run the following command in the same directory as this README file.
```bash
pip install -e .
```

Now you are ready to go.

## How to run the implemented algorithms
We have implemented several algorithms, as listed bellow:
* SHADE
* L-SHADE
* D-SHADE
* LARC-SHADE

You can find them in the EVOPT/EVOPT/algorithms folder.

To use them solve optimization problems, you can run the following command in EVOPT/EVOPT.
```bash
python run_algorithm.py -a L_SHADE -p Ackley
```
This command will start running the algorithm L_SHADE on solving a 30D Ackley function.

To see the full list of supported algorithms, functions and other parameters, run the following command.
```bash
python run_algorithm.py -h
```

The result will be saved in the `result` directory.

## Code Structure
```
.
├── EVOPT
│   ├── algorithms
│   │   ├── __init__.py
│   │   ├── D_SHADE.py
│   │   ├── L_SHADE.py
│   │   ├── LARC_SHADE.py
│   │   └── SHADE.py
│   ├── __init__.py
│   ├── problems
│   │   ├── __init__.py
│   │   ├── cec_2014.py
│   │   └── engineering_problems.py
│   ├── requirements.txt
│   ├── run_algorithm.py
│   ├── run_algorithms.sh
│   ├── solution.py
│   └── visualize.py
├── README.md
└── setup.py
```
Files in `algorithms` folder contains the implemented algorithms.

Files in `problems` folder contains the implemented problems or functions.

`solution.py` contains codes for basic definitions for Solution class. `visualize.py` contain functions for saving result as txt, jpg, gif.

## How to contribute
**If you want to implement your own algorithm or your own problem, please follow the instructions in this section.**

### Implement Algorithm
Your algorithm should be in a seperate python file. In this python file, two functions needs to be implemented:

```python
def xxx(func, problem_args, algorithm_args):
    # this should be the main function of your algorithm.
    # xxx is the name of your algorithm
    # func is the objective function that takes a python list as input and a Solution object as output.
    # problem_args is a dict, containing basic information about the problem, for example, dimensions, bounds, etc.
    # algorithm_args is also a dict, containing arguments specific to your algorithm.
    # this function should return two things:
    # optimal solution, a solution object that contains the best found solution.
    # history population, a list of list containing the history populations

def get_xxx_args(dimension):
    # this function should return a dict that will be used as the third argument of xxx
```

Your problems can be placed in existing files or new files. In that file, you need to implement two python functions as well.
```python
def xxx(x):
    # xxx is your function name. It should take a python list as input and output a float or several floats

def get_xxx_args(dimension):
    # this function should return a dict that will be used as problem_args
    # if you want it to be compatible with the existing algorithms, it should contain three keys:
    - dimension
    - bounds
    - MAX_NFE
```

After your implementation, you need to change the \_\_init\_\_.py in the `algorithms` or `problems` directory to make your implementation being recognizable by `run_algorithm.py`.
