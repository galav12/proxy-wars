'''
corr.py
This program implements correlation analysis between sensitive variables and other variables in a dataset 

Key Features:
    - Supports three different correlation methods: Pearson, Spearman, and Kendall.
    - Formats correlation values to three decimal places and handles NaN values.
    - Computes correlation values for the sensitive variables with respect to all other variables in the dataset.
'''


import pandas as pd
import numpy as np

'''
Computes correlation between sensitive variables and other variables in the dataset using the Correlation Analysis algorithm.
Parameters:
    sensitive_variables: list of variables to analyze for redundancy.
    data: a dataframe containing the dataset to be analyzed.
Returns:
    A dictionary where the keys are sensitive variables and the values are dictionaries of correlation values with respect to other variables.
'''
def compute_corr(sensitive_variables, data):
    
    # Check if sensitive variables and data are provided
    if(sensitive_variables is None):
        raise ValueError("Sensitive Variables needed for Correlation Analysis")
    if(data is None):
        raise ValueError("Data needed for Correlation Analysis")
    
    # Input data as a DataFrame
    df = pd.DataFrame(data)
    
    # Check if all sensitive variables exist in the data columns
    missing_vars = [var for var in sensitive_variables if var not in df.columns]
    if missing_vars:
        raise ValueError(f"Sensitive variable(s) {missing_vars} not found in the data columns for Correlation Analysis")
    
    # Correlation results for each method
    results = {}
    # Correlation methods to be used
    methods = ['pearson', 'spearman', 'kendall']
    
    # Iterate over each correlation method and compute the correlation matrix
    for method in methods:
        try:
            # Compute the correlation matrix using the specified method
            correlation_matrix = df.corr(method=method)
            # Extract and store correlations for the specified sensitive variables
            results[method] = correlation_matrix[sensitive_variables].to_dict()
            
            # Format the correlation values to 3 decimal places and handle NaN values
            for item in results[method]:
                results[method] = {sens: {col: "NaN" if np.isnan(float(val2)) else round(float(val2), 3) for col, val2 in val.items()} for sens, val in results[method].items()}
        except Exception as e:
            results[method] = str(e)
    
    return results
