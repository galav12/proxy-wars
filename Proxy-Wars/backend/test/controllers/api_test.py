'''
api_test.py
Unit tests for API endpoints in a Flask application.

Tested Endpoints:
    - /upload: Tests for uploading CSV files, including valid and invalid formats.
    - /algorithm: Tests for selecting valid and invalid algorithms.
    - /sensitive-variables: Tests for updating sensitive variables in the analysis.
    - /random: Tests for generating a random sample of the dataset.
    - /results: Tests for retrieving analysis results based on the selected algorithm and dataset.
    - /columns: Tests for retrieving column names from the dataset.
    - /target-variable: Tests for updating the target variable for analysis.
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import pytest
from controllers.api import route_bp
from flask import Flask
from unittest.mock import patch
import io

'''
Resets the global variables in each test case to ensure test isolation.
'''
@pytest.fixture(autouse=True)
def reset_globals():
    from controllers import api
    api.data = None
    api.sampled_data = None
    api.selected_algorithm = None
    api.sensitive_variables = []
    api.columns = []

'''
Sets up a Flask test client for the API routes.
Returns:
    A Flask test client object for making API requests in tests.
'''
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(route_bp)
    return app.test_client()

'''
Uploads a sample CSV dataset to the API via the upload endpoint.
Parameters:
    client: the Flask test client.
'''
def upload_sample_dataset(client):
    csv_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'test_data.csv'))
    with open(csv_file_path, 'rb') as data:
        response = client.post('/upload', content_type='multipart/form-data', data={'file': (data, 'test_data.csv')})
        assert response.status_code == 200

'''
Tests uploading a valid CSV file.
Parameters:
    client: the Flask test client.
'''
def test_upload_valid_file_with_id_column(client):
    csv_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'test_data.csv'))
    with open(csv_file_path, 'rb') as data:
        response = client.post('/upload', content_type='multipart/form-data', data={'file': (data, 'test_data.csv')})
        assert response.status_code == 200

'''
Tests uploading a file in an invalid format.
Parameters:
    client: the Flask test client.
'''
def test_upload_invalid_file_format(client):
    data = io.BytesIO(b"Some content")
    response = client.post('/upload', content_type='multipart/form-data', data={'file': (data, 'test.txt')})
    assert response.status_code == 400
    assert b'Invalid file' in response.data

'''
Tests the upload endpoint when no file is provided in the request.
Parameters:
    client: the Flask test client.
'''
def test_upload_no_file(client):
    response = client.post('/upload', content_type='multipart/form-data')
    assert response.status_code == 400
    assert b'No file uploaded' in response.data

'''
Tests selecting a valid algorithm.
Parameters:
    client: the Flask test client.
'''
def test_select_valid_algorithm(client):
    upload_sample_dataset(client)
    response = client.post('/algorithm', json={'algorithm': 'Correlational Analysis'})
    assert response.status_code == 200
    response = client.post('/algorithm', json={'algorithm': 'FACET'})
    assert response.status_code == 200

'''
Tests selecting an invalid algorithm.
Parameters:
    client: the Flask test client.
'''
def test_select_invalid_algorithm(client):
    upload_sample_dataset(client)
    response = client.post('/algorithm', json={'algorithm': 'Invalid Algorithm'})
    assert response.status_code == 400
    assert b'Invalid algorithm selected' in response.data

'''
Tests selecting no algorithm.
Parameters:
    client: the Flask test client.
'''
def test_no_algorithm_selected(client):
    upload_sample_dataset(client)
    response = client.post('/algorithm', json={})
    assert response.status_code == 400
    assert b'No algorithm selected' in response.data

'''
Tests selecting an algorithm when no dataset has been uploaded.
Parameters:
    client: the Flask test client.
'''
def test_algorithm_no_dataset(client):
    response = client.post('/algorithm', json={'algorithm': 'Correlational Analysis'})
    assert response.status_code == 400
    assert b'No dataset available' in response.data
    response = client.post('/algorithm', json={'algorithm': 'FACET'})
    assert response.status_code == 400
    assert b'No dataset available' in response.data

'''
Tests setting sensitive variables.
Parameters:
    client: the Flask test client.
'''
def test_set_sensitive_variables(client):
    upload_sample_dataset(client)
    response = client.post('/sensitive-variables', json={'variables': ['Age']})
    assert response.status_code == 200
    assert b'Sensitive variables updated' in response.data

'''
Tests setting invalid sensitive variables.
Parameters:
    client: the Flask test client.
'''
def test_set_invalid_sensitive_variables(client):
    response = client.post('/sensitive-variables', json={'variables': ['Age']})
    assert response.status_code == 400
    assert b'No dataset available' in response.data
    
    upload_sample_dataset(client)
    response = client.post('/sensitive-variables', json={})
    assert response.status_code == 400
    assert b'No sensitive variables selected' in response.data
   
    response = client.post('/sensitive-variables', json={'variables': ['non_existent_column']})
    assert response.status_code == 400
    assert b'Sensitive variable non_existent_column not found in columns' in response.data

'''
Tests setting a target variable.
Parameters:
    client: the Flask test client.
'''
def test_set_target_variables(client):
    upload_sample_dataset(client)
    response = client.post('/target-variable', json={'target': 'Graduated'})
    assert response.status_code == 200
    assert b'Target variable updated' in response.data

'''
Tests setting an invalid target variable.
Parameters:
    client: the Flask test client.
'''
def test_set_invalid_target_variables(client):
    response = client.post('/target-variable', json={'target': 'Graduated'})

    assert response.status_code == 400
    assert b'No dataset available' in response.data
    
    upload_sample_dataset(client)
    response = client.post('/target-variable', json={})
    assert response.status_code == 400
    assert b'No target variable selected' in response.data
   
    response = client.post('/target-variable', json={'target': 'non_existent_column'})
    assert response.status_code == 400
    assert b'Target variable non_existent_column not found in columns' in response.data

'''
Tests performing random sampling on a dataset.
Parameters:
    client: the Flask test client.
'''
def test_random_sample_valid(client):
    upload_sample_dataset(client)
    response = client.post('/random', json={'percentage': 50, 'seed': 1})
    assert response.status_code == 200
    assert b'sample' in response.data

'''
Tests performing random sampling with an invalid percentage.
Parameters:
    client: the Flask test client.
'''
def test_random_sample_invalid_percentage_low(client):
    upload_sample_dataset(client)
    response = client.post('/random', json={'percentage': -10, 'seed': 1})
    assert response.status_code == 400
    assert b'Invalid Percentage' in response.data
    
    response = client.post('/random', json={'percentage': 110, 'seed': 1})
    assert response.status_code == 400
    assert b'Invalid Percentage' in response.data 

'''
Tests performing random sampling without a dataset.
Parameters:
    client: the Flask test client.
'''
def test_random_sample_no_dataset(client):
    response = client.post('/random', json={'percentage': 50, 'seed': 1})
    assert response.status_code == 400
    assert b'No dataset available' in response.data

'''
Tests retrieving columns when no dataset is uploaded.
Parameters:
    client: the Flask test client.
'''
def test_get_columns_no_dataset(client):
    response = client.get('/columns')
    assert response.status_code == 400
    assert b'No dataset available' in response.data

'''
Tests retrieving columns with a valid uploaded dataset.
Parameters:
    client: the Flask test client object.
'''
def test_get_columns_with_dataset(client):
    upload_sample_dataset(client)
    response = client.get('/columns')
    assert response.status_code == 200
    assert b'columns' in response.data

'''
Tests getting results when no dataset is uploaded.
Parameters:
    client: the Flask test client.
'''
def test_get_results_no_dataset(client):
    response = client.get('/results')
    assert response.status_code == 400
    assert b'No dataset available' in response.data

'''
Tests getting results when sensitive variables are not set.
Parameters:
    client: the Flask test client object used to send the request.
'''
def test_get_results_no_sensitive_vars(client):
    upload_sample_dataset(client)
    client.post('/random', json={'percentage': 50, 'seed': 1})
    response = client.get('/results')
    assert response.status_code == 400
    assert b'Sensitive variables not set' in response.data

'''
Tests getting results when an algorithm is not set.
Parameters:
    client: the Flask test client.
'''
def test_get_results_no_algorithm(client):
    upload_sample_dataset(client)
    client.post('/random', json={'percentage': 50, 'seed': 1})
    client.post('/sensitive-variables', json={'variables': ['Age']})
    response = client.get('/results')
    assert response.status_code == 500

'''
Tests getting results with valid setup and data.
Parameters:
    client: the Flask test client.
'''
def test_get_results_valid(client):
    upload_sample_dataset(client)
    response = client.post('/random', json={'percentage': 50, 'seed': 1})
    assert response.status_code == 200
    response = client.post('/sensitive-variables', json={'variables': ['Age']})
    assert response.status_code == 200
    response = client.post('/algorithm', json={'algorithm': 'Correlational Analysis'})
    assert response.status_code == 200
    response = client.get('/results')
    assert response.status_code == 200
    assert b'Correlation analysis completed' in response.data

    response = client.post('/algorithm', json={'algorithm': 'FACET'})
    assert response.status_code == 200
    response = client.post('/target-variable', json={'target': 'Graduated'})
    assert response.status_code == 200
    response = client.get('/results')
    assert response.status_code == 200
    assert b'FACET analysis completed' in response.data

'''
Tests getting results with an exception
Parameters:
    client: the Flask test client.
'''
def test_get_results_exception(client):
    upload_sample_dataset(client)
    response = client.post('/random', json={'percentage': 50, 'seed': 1})
    assert response.status_code == 200
    response = client.post('/sensitive-variables', json={'variables': ['Age']})
    assert response.status_code == 200
    response = client.post('/algorithm', json={'algorithm': 'Correlational Analysis'})
    assert response.status_code == 200
    
    # Mock `compute_corr` to raise an exception
    with patch('controllers.api.compute_corr', side_effect=Exception('Test Exception')):
        response = client.get('/results')
        assert response.status_code == 500
        assert b'Test Exception' in response.data

    response = client.post('/algorithm', json={'algorithm': 'FACET'})
    assert response.status_code == 200

    # Mock `compute_facet` to raise an exception
    with patch('controllers.api.compute_facet', side_effect=Exception('Test Exception')):
        response = client.get('/results')
        assert response.status_code == 500
        assert b'Test Exception' in response.data

"""Test getting results with valid SQL filter."""
def test_sql_filter_valid(client):
    # Upload a sample dataset
    upload_sample_dataset(client)
    # Set SQL filter
    sql_filter = "Age > 30"
    # Send POST request to filter endpoint
    response = client.post('/filter', json={'query': sql_filter})
    assert response.status_code == 200
    # Get the filtered data and make sure the values match our filter
    filtered_data = response.get_json().get('filtered_data')
    assert all(item['Age'] > 30 for item in filtered_data)

"""Test getting results with valid SQL filter with 4 conditions."""
def test_sql_filter_valid_advanced(client):
    # Upload a sample dataset
    upload_sample_dataset(client)
    # Set SQL filter
    sql_filter = "Age > 20 and Gender = 1 and Religious = 0 and Age < 50"
    # Send POST request to filter endpoint
    response = client.post('/filter', json={'query': sql_filter})
    assert response.status_code == 200
    # Get the filtered data and make sure the values match our filter
    filtered_data = response.get_json().get('filtered_data')
    assert all(item['Age'] > 20 for item in filtered_data)
    assert all(item['Gender'] == 1 for item in filtered_data)
    assert all(item['Religious'] == 0 for item in filtered_data)
    assert all(item['Age'] < 50 for item in filtered_data)

"""Test getting results with invalid SQL filter."""
def test_sql_filter_invalid(client):
    # Upload a sample dataset
    upload_sample_dataset(client)
    # Set SQL filter
    sql_filter = ""
    # Send POST request to filter endpoint
    response = client.post('/filter', json={'query': sql_filter})
    # Make sure we get an error code
    assert response.status_code == 400

"""Test getting results with valid SQL filter but no matching rows."""
def test_sql_filter_no_match(client):
    # Upload a sample dataset
    upload_sample_dataset(client)
    # Set SQL filter
    sql_filter = "Age > 1000 and Gender = 0"
    # Send POST request to filter endpoint
    response = client.post('/filter', json={'query': sql_filter})
    # Make sure we get an error code
    assert response.status_code == 400

"""Test getting results with no dataset."""
def test_sql_filter_no_data(client):
    # Set SQL filter
    sql_filter = "Age > 30"
    # Send POST request to filter endpoint
    response = client.post('/filter', json={'query': sql_filter})
    # Make sure we get an error code
    assert response.status_code == 400