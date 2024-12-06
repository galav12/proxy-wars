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

# Helper function to upload a sample CSV dataset
def upload_sample_dataset(client, dataset_path):
    with open(dataset_path, 'rb') as data:
        response = client.post('/upload', content_type='multipart/form-data', data={'file': (data, os.path.basename(dataset_path))})
        assert response.status_code == 200

# Test to run on multiple samples and datasets and measure time
def test_get_results_on_datasets(client):
    # List of datasets
    datasets = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'titanic_test.csv')),
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'titanic_train.csv')),
    ]

    # Percentages to sample
    percentages = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    # List to store results
    results = []

    # Loop through datasets and percentages
    for dataset in datasets:
        dataset_name = os.path.basename(dataset)
        for percentage in percentages:
            # Upload dataset
            upload_sample_dataset(client, dataset)

            # Perform sampling
            response = client.post('/random', json={'percentage': percentage, 'seed': 1})
            assert response.status_code == 200

            # Select sensitive variables
            response = client.post('/sensitive-variables', json={'variables': ['Age']})
            assert response.status_code == 200

            # Select algorithm
            response = client.post('/algorithm', json={'algorithm': 'FACET'})
            assert response.status_code == 200

            # Select target variable
            response = client.post('/target-variable', json={'target': 'Pclass'})
            assert response.status_code == 200

            # Measure time for results
            start_time = time.time()
            response = client.get('/results')
            end_time = time.time()
            
            # Assert that the result is valid
            print(response.data)
            assert response.status_code == 200
            assert b'FACET analysis completed' in response.data

            # Calculate time taken
            time_taken = end_time - start_time

            # Append the result
            results.append({
                'Dataset': dataset_name,
                '% of dataset': percentage,
                'Runtime': time_taken
            })

    dataset = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'census.csv'))
    dataset_name = os.path.basename(dataset)
    for percentage in percentages:
        # Upload dataset
        upload_sample_dataset(client, dataset)

        # Perform sampling
        response = client.post('/random', json={'percentage': percentage, 'seed': 1})
        assert response.status_code == 200

        # Select sensitive variables
        response = client.post('/sensitive-variables', json={'variables': ['Age']})
        assert response.status_code == 200

        # Select algorithm
        response = client.post('/algorithm', json={'algorithm': 'FACET'})
        assert response.status_code == 200

        # Select target variable
        response = client.post('/target-variable', json={'target': 'Class'})
        assert response.status_code == 200

        # Measure time for results
        start_time = time.time()
        response = client.get('/results')
        end_time = time.time()
            
        # Assert that the result is valid
        print(response.data)
        assert response.status_code == 200
        assert b'FACET analysis completed' in response.data

        # Calculate time taken
        time_taken = end_time - start_time

        # Append the result
        results.append({
            'Dataset': dataset_name,
            '% of dataset': percentage,
            'Runtime': time_taken
        })


    # Export results to CSV
    df = pd.DataFrame(results)
    output_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'facet_sampling_runtimes.csv'))
    df.to_csv(output_csv, index=False)
