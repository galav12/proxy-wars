'''
arm.py
This program implements Association Rule Mining (ARM) for sensitive variables in a dataset 

Key Features:
    - Utilizes the NiaARM algorithm for mining association rules.
    - Applies Differential Evolution for rule optimization.
    - Supports analysis of sensitive variables and computes average statistics for each rule.
'''


from niaarm import NiaARM
from niaarm import Dataset, get_rules
from niapy.algorithms.basic import DifferentialEvolution
from niapy.task import Task, OptimizationType
import pandas as pd

'''
Computes association rule mining (ARM) using the NiaARM algorithm and Differential Evolution optimization.
Parameters:
    sensitive_variables: list of variables to analyze for sensitive relationships.
    df: a dataframe containing the dataset to be analyzed.
    target_var: the target variable for building the prediction model.
    random_seed: the random seed for computation (default is 0 for reproducibility).
Returns:
    A dictionary where the keys are sensitive variables, and the values contain statistics for the association rules found.
'''
def compute_arm(sensitive_variables, df, seed):
    
    # Input data as a DataSet
    data = Dataset(df)

    # Problem for NiaARM
    problem = NiaARM(data.dimension, data.features, data.transactions, metrics=('support', 'confidence'), logging=True)
    # Task for the optimization process
    task = Task(problem=problem, max_iters=30, optimization_type=OptimizationType.MAXIMIZATION)
    # Differential Evolution algorithm for solving the task
    if seed == -1:
        algo = DifferentialEvolution(population_size=50, differential_weight=0.5, crossover_probability=0.9)
    else:
        algo = DifferentialEvolution(population_size=50, differential_weight=0.5, crossover_probability=0.9, seed=seed)
    
    # Best solution for task
    best = algo.run(task=task)

    # Sort the association rules
    problem.rules.sort()

    rules = []
    for rule in problem.rules:
        row = {"antecedent": [f"{a.name}({round(a.min_val,3)},{round(a.max_val,3)})" for a in rule.antecedent], "consequent": [f"{c.name}({round(c.min_val,3)},{round(c.max_val,3)})" for c in rule.consequent], "fitness": round(rule.fitness,5)}
        for metric in ["support", "confidence", "lift"]:
            row[metric] = round(getattr(rule, metric),6)
        rules.append(row)

    return rules
