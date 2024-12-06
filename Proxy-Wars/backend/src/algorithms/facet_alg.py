'''
facet_alg.py
This program implements the FACET algorithm to compute redundancy between sensitive variables and other variables 
in a dataset using a Random Forest model. The process involves building predictive models to evaluate how much 
information in other variables overlaps with the sensitive variables.

Key functionalities:
- Defines a configurable Random Forest regressor pipeline with hyperparameter tuning.
- Utilizes cross-validation with repeated K-fold to optimize the model parameters using GridSearchCV.
- Computes a redundancy matrix that quantifies the redundancy between sensitive variables and other features.
'''
import pandas as pd
import numpy as np
from sklearndf.pipeline import RegressorPipelineDF
from sklearndf.regression import RandomForestRegressorDF
from sklearn.model_selection import RepeatedKFold, GridSearchCV
from facet.data import Sample
from facet.selection import LearnerSelector, ParameterSpace
from facet.inspection import LearnerInspector

# Configurable variables
# Number of estimators for Random Forest
REGRESSOR_ESTIMATOR_COUNT = 50
# Number of folds for cross-validation
KFOLD_SPLITS = 3
# Number of times cross-validation is repeated
KFOLD_REPEATS = 5
# Number of parallel jobs for the learner selector
LEARNER_SELECTOR_JOBS = -1
# Minimum samples required at leaf node
REGRESSOR_MIN_SAMPLES_LEAF = [11, 15]
# Maximum depth of trees in the Random Forest
REGRESSOR_MAX_DEPTH = [5, 6]
# Seed for reproducibility
RANDOM_STATE = 0

'''
Function to compute redundancy between sensitive variables and other variables in the dataset using the FACET algorithm.
Parameters:
    sensitive_variables: list of variables to analyze for redundancy.
    data: a dataframe containing the dataset to be analyzed.
    target_var: the target variable for building the prediction model.
    random_seed: the random seed for computation (default is 0 for reproducibility).
Returns:
    A dictionary where the keys are sensitive variables and the values are dictionaries of redundancy values with respect to other variables.
'''
def compute_facet(sensitive_variables, data, target_var, random_seed=RANDOM_STATE):

    random_seed = 0 if random_seed < 0 else random_seed

    # Check if sensitive variables and data are provided
    if(sensitive_variables is None):
        raise ValueError("Sensitive Variables needed for FACET")
    if(data is None):
        raise ValueError("Data needed for FACET")
    
    # Input data as a DataFrame
    df = pd.DataFrame(data)
    
    # Check if all sensitive variables and target variable exist in the data columns
    missing_vars = [var for var in sensitive_variables if var not in df.columns]
    if missing_vars:
        raise ValueError(f"Sensitive variable(s) {missing_vars} not found in the data columns for FACET")
    if(target_var is None):
        raise ValueError("Target Variable(s) needed for FACET")
    if target_var not in df.columns:
        raise ValueError(f"Target variable(s) {target_var} not found in the data columns for FACET")

    # Create a sample from the data
    data_sample = Sample(observations=data, target_name=target_var)


    # Define a pipeline for the Random Forest regressor
    rnd_forest_reg = RegressorPipelineDF(
        regressor=RandomForestRegressorDF(n_estimators=REGRESSOR_ESTIMATOR_COUNT, random_state=random_seed)
    )
    
    min_samples_leaf = [round(len(df) * .05),round(len(df) * .06),round(len(df) * .07) ]
    maxDepth = []
    if (len(df) < 1000):
        maxDepth = [5, 10, 15]
    elif (len(df) < 10000):
        maxDepth = [20, 25, 30]
    else:
        maxDepth = [50,60,70]
    
    # Define the parameter space for hyperparameter tuning
    rnd_forest_ps = ParameterSpace(rnd_forest_reg)
    rnd_forest_ps.regressor.min_samples_leaf = min_samples_leaf
    rnd_forest_ps.regressor.max_depth = maxDepth

    # Configure cross-validation
    rkf_cv = RepeatedKFold(n_splits=KFOLD_SPLITS, n_repeats=KFOLD_REPEATS, random_state=random_seed)

    # Select the best model using GridSearchCV over the defined parameter space
    selector = LearnerSelector(
        searcher_type=GridSearchCV,
        parameter_space=rnd_forest_ps,
        cv=rkf_cv,
        n_jobs=LEARNER_SELECTOR_JOBS,
        scoring="r2"
    ).fit(data_sample)

    # Compute the feature redundancy matrix from model (time-consuming)
    inspector = LearnerInspector(model=selector.best_estimator_, n_jobs=-3).fit(data_sample)
    redundancy_matrix = inspector.feature_redundancy_matrix()
    redundancy_df = redundancy_matrix.to_frame()

    # Extract redundancy values for sensitive variables and format them to 5 decimal places, handling NaN values
    result = redundancy_df[sensitive_variables].to_dict()
    for item in result:

        # result[item] = {col:"NaN" if pd.isna(val) else f"{round(float(val*100),5)}%" for col,val in result[item].items()}
        result[item] = {col:"NaN" if pd.isna(float(val)) else round(float(val*100),5) for col,val in result[item].items()}
    
    return result

#test dataset takes about one minute to run in the default configuration
'''
# declaring url with data
data_url = 'https://web.stanford.edu/~hastie/Papers/LARS/diabetes.data'

#importing data from url
diabetes_df = pd.read_csv(data_url, delimiter='\t').rename(
    # renaming columns for better readability
    columns={
        'S1': 'TC', # total serum cholesterol
        'S2': 'LDL', # low-density lipoproteins
        'S3': 'HDL', # high-density lipoproteins
        'S4': 'TCH', # total cholesterol/ HDL
        'S5': 'LTG', # lamotrigine level
        'S6': 'GLU', # blood sugar level
        'Y': 'Disease_progression' # measure of progress since 1yr of baseline
    }
)
'''
