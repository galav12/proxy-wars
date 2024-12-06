import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import pytest
from controllers.api import route_bp
from flask import Flask
import time
import pandas as pd

# Reset the global variables in each test case
@pytest.fixture(autouse=True)
def reset_globals():
    from controllers import api
    api.data = None
    api.sampled_data = None
    api.selected_algorithm = None
    api.sensitive_variables = []
    api.columns = []

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(route_bp)
    return app.test_client()

# Helper function to upload a modified CSV dataset with one column removed
def upload_modified_dataset(client, dataset_path, drop_column=None):
    df = pd.read_csv(dataset_path)
    if drop_column:
        df = df.drop(columns=[drop_column])
    
    modified_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'modified_test_data.csv'))
    df.to_csv(modified_csv, index=False)
    
    with open(modified_csv, 'rb') as data:
        response = client.post('/upload', content_type='multipart/form-data', data={'file': (data, os.path.basename(modified_csv))})
        assert response.status_code == 200

# Test to run on multiple samples, datasets, and removed columns
def test_get_results_on_modified_datasets(client):
    # List of datasets
    datasets = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'titanic_train.csv')),
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'titanic_test.csv')),
    ]

    # Percentages to sample
    percentages = [100]

    # List to store results
    results = []

    # Loop through datasets and removed columns
    for dataset in datasets:
        df = pd.read_csv(dataset)
        columns = df.columns.tolist()
        dataset_name = os.path.basename(dataset)

        for percentage in percentages:
            # Loop through each column, remove it, and measure results time
            for drop_column in columns:
                target_var = 'Pclass'
                sensitive_var = 'Age'
                if drop_column == sensitive_var or drop_column == target_var:
                    continue
                # Upload dataset with one column removed
                upload_modified_dataset(client, dataset, drop_column)

                # Perform sampling
                response = client.post('/random', json={'percentage': percentage, 'seed': 1})
                assert response.status_code == 200

                # Select sensitive variables
                response = client.post('/sensitive-variables', json={'variables': [sensitive_var]})
                assert response.status_code == 200

                # Select algorithm
                response = client.post('/algorithm', json={'algorithm': 'FACET'})
                assert response.status_code == 200

                # Select target variable
                
                response = client.post('/target-variable', json={'target': target_var})
                assert response.status_code == 200

                # Measure time for results
                start_time = time.time()
                response = client.get('/results')
                end_time = time.time()

                # Assert that the result is valid
                assert response.status_code == 200
                assert b'FACET analysis completed' in response.data

                # Calculate time taken
                time_taken = end_time - start_time

                # Append the result
                results.append({
                    'Dataset': dataset_name,
                    'Removed Column': drop_column,
                    '% of Dataset': percentage,
                    'Runtime': time_taken
                })
                
    dataset = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'census.csv'))
    df = pd.read_csv(dataset)
    columns = df.columns.tolist()
    dataset_name = os.path.basename(dataset)

    for percentage in percentages:
        # Loop through each column, remove it, and measure results time
        for drop_column in columns:
            target_var = 'Class'
            sensitive_var = 'Age'
            if drop_column == sensitive_var or drop_column == target_var:
                continue
            # Upload dataset with one column removed
            upload_modified_dataset(client, dataset, drop_column)

            # Perform sampling
            response = client.post('/random', json={'percentage': percentage, 'seed': 1})
            assert response.status_code == 200

            # Select sensitive variables
            response = client.post('/sensitive-variables', json={'variables': [sensitive_var]})
            assert response.status_code == 200

            # Select algorithm
            response = client.post('/algorithm', json={'algorithm': 'FACET'})
            assert response.status_code == 200

            # Select target variable                
            response = client.post('/target-variable', json={'target': target_var})
            assert response.status_code == 200

            # Measure time for results
            start_time = time.time()
            response = client.get('/results')
            end_time = time.time()

            # Assert that the result is valid
            assert response.status_code == 200
            assert b'FACET analysis completed' in response.data

            # Calculate time taken
            time_taken = end_time - start_time

            # Append the result
            results.append({
                'Dataset': dataset_name,
                'Removed Column': drop_column,
                '% of Dataset': percentage,
                'Runtime': time_taken
            })

    os.remove(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'modified_test_data.csv')))
    # Export results to CSV
    df_results = pd.DataFrame(results)
    output_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'facet_cols_runtime.csv'))
    df_results.to_csv(output_csv, index=False)
