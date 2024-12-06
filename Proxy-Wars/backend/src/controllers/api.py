'''
api.py
This file defines API endpoints for a Flask application to handle the analysis of datasets using various algorithms.

Endpoints:
    - /upload: Uploads a CSV file and processes the dataset.
    - /algorithm: Selects an algorithm for analysis.
    - /sensitive-variables: Updates the sensitive variables for analysis.
    - /random: Generates a random sample of the dataset.
    - /results: Performs analysis based on the selected algorithm.
    - /columns: Retrieves the column names from the dataset.
    - /target-variable: Updates the target variable for the analysis.
'''


from flask import Flask, request, jsonify, Blueprint
import pandas as pd
import numpy as np
import pandasql as ps

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'algorithms')))

from corr import compute_corr
from facet_alg import compute_facet
from arm import compute_arm

# Initialize a Flask Blueprint for the API routes
route_bp = Blueprint('api',__name__)

# The uploaded dataset
data = None

# A random sample of the dataset
sampled_data = None

# The selected algorithm (Correlation, FACET, ARM)
selected_algorithm = None

# The sensitive variables chosen by the user
sensitive_variables = []

# The target variable for the analysis
target_variable = None

# The columns of the dataset
columns = []
# Random seed for reproducibility
seed = 0  

'''
Uploads a CSV file and processes it to create a dataset.
Returns:
    A JSON response indicating the status of the upload. If successful, the dataset is stored globally, 
    and the columns are extracted.
'''
@route_bp.route('/upload', methods=['POST'])
def upload():
    global data
    
    # Check if a file is uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']

    # Check if the uploaded file is a valid CSV
    if file and file.filename.endswith('.csv'):
        # Read the CSV file into a pandas DataFrame
        data = pd.read_csv(file)
        # Remove the first column if it contains 'id'
        if 'id' in data.columns[0].lower():
            data = data.drop(columns=[data.columns[0]])
        # Retain only numerical columns
        data = data.select_dtypes([np.number])
        data = data.apply(pd.to_numeric, errors='coerce')
        
        # Store the columns of the dataset
        global columns
        columns = list(data.columns)
        
        if columns is None:
            return jsonify({'error': 'No columns in dataset'}), 400
        
        return jsonify({'status': 'File uploaded successfully'}), 200

    # Invalid file format
    return jsonify({'error': 'Invalid file'}), 400


'''
Selects an algorithm for analysis from the provided options.
Returns:
    A JSON response indicating the status of the algorithm selection. If successful, the selected 
    algorithm is stored globally.
'''
@route_bp.route('/algorithm', methods=['POST'])
def algorithm():
    global data

    # Ensure dataset is uploaded before selecting an algorithm
    if data is None:
        return jsonify({'error': 'No dataset available'}), 400
    
    global selected_algorithm
    # Get the selected algorithm from the request
    request_data = request.get_json()
    selected_algorithm = request_data.get('algorithm')

    # Check if an algorithm was selected
    if selected_algorithm is None:
        return jsonify({'error': 'No algorithm selected'}), 400
    
    # Validate the algorithm choice
    algorithms_list = ['Correlational Analysis', 'FACET', 'Association Rule Mining']
    if selected_algorithm not in algorithms_list:
        return jsonify({'error': 'Invalid algorithm selected'}), 400
    
    return jsonify({'status': 'Algorithm selected'}), 200


'''
Updates the sensitive variables to analyze based on user input.
Parameters:
    variables: list of sensitive variables selected by the user for analysis.
Returns:
    A JSON response indicating the status of the update. If successful, the selected sensitive variables 
    are stored globally.
'''
@route_bp.route('/sensitive-variables', methods=['POST'])
def sens_vars():
    global data
    
    # Ensure dataset is uploaded before selecting sensitive variables
    if data is None:
        return jsonify({'error': 'No dataset available'}), 400

    global sensitive_variables
    # Get the list of sensitive variables from the request
    request_data = request.get_json()
    sensitive_variables = request_data.get('variables', [])

    # Ensure sensitive variables were provided
    if not sensitive_variables:
        return jsonify({'error': 'No sensitive variables selected'}), 400
    
    # Check if the selected sensitive variables exist in the dataset columns
    for var in sensitive_variables:
        if not(var in columns):
            return jsonify({'error': f'Sensitive variable {var} not found in columns'}), 400

    return jsonify({'status': 'Sensitive variables updated'}), 200


'''
Creates a random sample of the dataset based on the specified percentage and seed.
Parameters:
    percentage: the percentage of the dataset to sample.
    seed: the random seed for sampling.
Returns:
    A JSON response containing the sampled data.
'''
@route_bp.route('/random', methods=['POST'])
def random_sample():
    global data, sampled_data, seed
    # Ensure dataset is uploaded before sampling
    if data is None:
        return jsonify({'error': 'No dataset available'}), 400
    
    # Get the percentage of data to sample and the seed for random sampling
    request_data = request.get_json()
    percentage = float(request_data.get('percentage'))
    seed = int(request_data.get('seed'))
    
    # Validate the percentage value
    if percentage <= 0 or percentage > 100:
        return jsonify({'error': 'Invalid Percentage'}), 400
    
    # Sample the dataset based on the given percentage
    sampled_data = data
    if percentage < 100:
        sample_fraction = float(percentage) / 100.0
        if seed == -1:
            seed = 0
            sampled_data = data.sample(frac=sample_fraction)
        else:
            sampled_data = data.sample(frac=sample_fraction, random_state=seed)
    
    # Convert the sampled data to JSON and return it
    result = sampled_data.to_dict(orient='records')
    
    return jsonify({'sample': result}), 200


'''
Performs analysis based on the selected algorithm and the sensitive variables.
Returns:
    A JSON response with the results of the analysis.
'''
@route_bp.route('/results', methods=['GET'])
def get_results():
    global sampled_data, sensitive_variables, columns, target_variable, seed

    # Ensure dataset and sensitive variables are available
    if sampled_data is None:
        return jsonify({'error': 'No dataset available'}), 400
    
    try:
        # Correlational Analysis
        if selected_algorithm == 'Correlational Analysis':
            if not sensitive_variables:
                return jsonify({'error': 'Sensitive variables not set'}), 400
            results = compute_corr(sensitive_variables, sampled_data)
            return jsonify({'status': 'Correlation analysis completed', 'results': results}), 200
        
        # FACET Analysis
        if selected_algorithm == 'FACET':
            if target_variable is None:
                return jsonify({'error': 'Target variable not set'}), 400
            
            if not sensitive_variables:
                return jsonify({'error': 'Sensitive variables not set'}), 400
            results = compute_facet(sensitive_variables, sampled_data, target_variable, seed)
            return jsonify({'status': 'FACET analysis completed', 'results': results}), 200
        
        # Association Rule Mining (ARM)
        if selected_algorithm == 'Association Rule Mining':
            results = compute_arm(sensitive_variables, sampled_data, seed)
            return jsonify({'status': 'Association Rule Mining completed', 'results': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


'''
Retrieves the columns from the uploaded dataset.
Returns:
    A JSON response containing the list of columns in the dataset.
'''
@route_bp.route('/columns', methods=['GET'])
def get_columns():
    global data, columns
    # Ensure dataset is uploaded
    if data is None:
        return jsonify({'error': 'No dataset available'}), 400
    if columns is None:
        return jsonify({'error': 'No columns set available'}), 400
    
    return jsonify({'columns': columns}), 200


'''
Updates the target variable based on user input for analysis.
Parameters:
    target: the target variable selected by the user.
Returns:
    A JSON response indicating the status of the update. If successful, the selected target variable 
    is stored globally.
'''
@route_bp.route('/target-variable', methods=['POST'])
def target_var():
    global data
    global target_variable

    # Ensure dataset is uploaded before selecting target variable
    if data is None:
        return jsonify({'error': 'No dataset available'}), 400

    # Get the target variable from the request
    request_data = request.get_json()
    target_variable = request_data.get('target')

    # Ensure a target variable was provided
    if target_variable is None:
        return jsonify({'error': 'No target variable selected'}), 400
    
    # Check if the target variable exists in the dataset columns
    global columns
    if target_variable not in columns:
        return jsonify({'error': f'Target variable {target_variable} not found in columns'}), 400
    
    return jsonify({'status': 'Target variable updated'}), 200

# 8. Limit Dataset by SQL Filter
@route_bp.route('/filter', methods=['POST'])
def sql_filter():

    global data
    global sampled_data
    
    ## No dataset uploaded
    if data is None:
        return jsonify({'error': 'No dataset available'}), 400

    ## Get SQL filter
    request_data = request.get_json()
    sql_filter = request_data.get('query')

    ## Make sure we get the SQL filter
    if not sql_filter:
        return jsonify({'error': 'No SQL Filter provided'}), 400

    ## Apply filter to the data
    sampled_data = ps.sqldf(f"SELECT * FROM data WHERE {sql_filter}", {'data': data})

    ## Make sure there are rows in the filtered data
    if sampled_data.empty:
            return jsonify({'error': 'No rows match the filter'}), 400

    ## Convert filtered data to JSON
    result = sampled_data.to_dict(orient='records')

    return jsonify({'filtered_data': result}), 200
