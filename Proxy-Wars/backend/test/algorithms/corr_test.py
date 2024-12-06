'''
test_corr_algorithm.py
Unit tests for the `compute_corr` function, which performs correlation analysis between sensitive 
variables and other variables in a dataset.

Key Features:
    - Tests three correlation methods: Pearson, Spearman, and Kendall.
    - Validates the function’s ability to handle missing, non-numeric, and invalid sensitive variables.
    - Ensures that the correlation results are accurate and raises appropriate exceptions for erroneous inputs.
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import unittest
import pandas as pd
from algorithms.corr import compute_corr

'''
This class contains unit tests for the compute_corr function which calculates 
correlation coefficients (Pearson, Spearman, Kendall) between sensitive variables 
and all other variables in a dataset.
'''

class TestComputeCorr(unittest.TestCase):

    '''
    Set up for tests. Defines the test data and variable names before running the test cases.
    '''
    def setUp(self):
        # Sample data to be used in tests
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'test_data.csv'))
        self.data = pd.read_csv(file_path)
        
        # Storing the list of all columns except 'id'
        self.all_columns = self.data.columns.tolist()
        self.all_columns.remove('id')
    
    '''
    Tests the results of the correlation analysis with one sensitive variable
    '''
    def test_salary_correlation(self):
        # Compute the correlation results
        result = compute_corr(['Salary'], self.data)
        # Define the expected results for comparison
        expected_pearson = {
            'id': 0.229,
            'Age': 0.231,
            'Speed': 0.419,
            'Height': 0.221,
            'Weight': 0.169,
            'IQ': 0.711,
            'Gender': 0.265,
            'Salary': 1.0,
            'Religious': 0.357,
            'Graduated': 0.011
        }
    
        expected_spearman = {
            'id': 0.644,
            'Age': 0.644,
            'Speed': 0.666,
            'Height': 0.639,
            'Weight': 0.653,
            'IQ': 0.93,
            'Gender': 0.167,
            'Salary': 1.0,
            'Religious': 0.177,
            'Graduated': 0.643
        }
    
        expected_kendall = {
            'id': 0.459,
            'Age': 0.459,
            'Speed': 0.506,
            'Height': 0.47,
            'Weight': 0.484,
            'IQ': 0.815,
            'Gender': 0.143,
            'Salary': 1.0,
            'Religious': 0.152,
            'Graduated': 0.552
        }

        # Validate the results for Pearson correlation
        self.assertIn('pearson', result)
        self.assertIn('Salary', result['pearson'])
        for column, expected_value in expected_pearson.items():
            actual_value = result['pearson']['Salary'][column]
            self.assertEqual(actual_value, expected_value,
                                   msg=f"Pearson correlation for '{column}' does not match. Expected: {expected_value}, Actual: {actual_value}")
    
        # Validate the results for Spearman correlation
        self.assertIn('spearman', result)
        self.assertIn('Salary', result['spearman'])
        for column, expected_value in expected_spearman.items():
            actual_value = result['spearman']['Salary'][column]
            self.assertEqual(actual_value, expected_value,
                                   msg=f"Spearman correlation for '{column}' does not match. Expected: {expected_value}, Actual: {actual_value}")

        # Validate the results for Kendall correlation
        self.assertIn('kendall', result)
        self.assertIn('Salary', result['kendall'])
        for column, expected_value in expected_kendall.items():
            actual_value = result['kendall']['Salary'][column]
            self.assertEqual(actual_value, expected_value,
                                   msg=f"Kendall correlation for '{column}' does not match. Expected: {expected_value}, Actual: {actual_value}")
    
    '''
    Tests the results of the correlation analysis with more than one sensitive variable
    '''
    def test_salary_graduated_correlation(self):
        # Compute the correlation results
        result = compute_corr(['Salary', 'Graduated'], self.data)

        # Define the expected results for comparison
        expected_pearson = {
            'Salary': {
                'id': 0.229,
                'Age': 0.231,
                'Speed': 0.419,
                'Height': 0.221,
                'Weight': 0.169,
                'IQ': 0.711,
                'Gender': 0.265,
                'Salary': 1.0,
                'Religious': 0.357,
                'Graduated': 0.011,
            },
            'Graduated': {
                'id': 0.319,
                'Age': 0.349,
                'Speed': 0.462,
                'Height': 0.35,
                'Weight': 0.367,
                'IQ': 0.465,
                'Gender': 0.209,
                'Salary': 0.011,
                'Religious': 0.012,
                'Graduated': 1.0,
            }
        }

        expected_spearman = {
            'Salary': {
                'id': 0.644,
                'Age': 0.644,
                'Speed': 0.666,
                'Height': 0.639,
                'Weight': 0.653,
                'IQ': 0.93,
                'Gender': 0.167,
                'Salary': 1.0,
                'Religious': 0.177,
                'Graduated': 0.643,
            },
            'Graduated': {
                'id': 0.319,
                'Age': 0.319,
                'Speed': 0.44,
                'Height': 0.379,
                'Weight': 0.359,
                'IQ': 0.568,
                'Gender': 0.209,
                'Salary': 0.643,
                'Religious': 0.012,
                'Graduated': 1.0,
            }
        }

        expected_kendall = {
            'Salary': {
                'id': 0.459,
                'Age': 0.459,
                'Speed': 0.506,
                'Height': 0.47,
                'Weight': 0.484,
                'IQ': 0.815,
                'Gender': 0.143,
                'Salary': 1.0,
                'Religious': 0.152,
                'Graduated': 0.552,
            },
            'Graduated': {
                'id': 0.267,
                'Age': 0.267,
                'Speed': 0.375,
                'Height': 0.32,
                'Weight': 0.3,
                'IQ': 0.478,
                'Gender': 0.209,
                'Salary': 0.552,
                'Religious': 0.012,
                'Graduated': 1.0,
            }
        }

        # Validate the results for Pearson correlation
        self.assertIn('pearson', result)
        self.assertIn('Salary', result['pearson'])
        self.assertIn('Graduated', result['pearson'])

        # Check Pearson correlation results for 'Salary'
        for column, expected_value in expected_pearson['Salary'].items():
            actual_value = result['pearson']['Salary'][column]
            self.assertEqual(actual_value, expected_value, 
                msg=f"Pearson correlation for 'Salary' with '{column}' does not match. Expected: {expected_value}, Actual: {actual_value}")

        # Check Pearson correlation results for 'Graduated'
        for column, expected_value in expected_pearson['Graduated'].items():
            actual_value = result['pearson']['Graduated'][column]
            self.assertEqual(actual_value, expected_value,
                msg=f"Pearson correlation for 'Graduated' with '{column}' does not match. Expected: {expected_value}, Actual: {actual_value}")

        # Validate the results for Spearman correlation
        self.assertIn('spearman', result)
        self.assertIn('Salary', result['spearman'])
        self.assertIn('Graduated', result['spearman'])

        # Check Spearman correlation results for 'Salary'
        for column, expected_value in expected_spearman['Salary'].items():
            actual_value = result['spearman']['Salary'][column]
            self.assertEqual(actual_value, expected_value,
                msg=f"Spearman correlation for 'Salary' with '{column}' does not match. Expected: {expected_value}, Actual: {actual_value}")

        # Check Spearman correlation results for 'Graduated'
        for column, expected_value in expected_spearman['Graduated'].items():
            actual_value = result['spearman']['Graduated'][column]
            self.assertEqual(actual_value, expected_value,
                msg=f"Spearman correlation for 'Graduated' with '{column}' does not match. Expected: {expected_value}, Actual: {actual_value}")

        # Validate the results for Kendall correlation
        self.assertIn('kendall', result)
        self.assertIn('Salary', result['kendall'])
        self.assertIn('Graduated', result['kendall'])

        # Check Kendall correlation results for 'Salary'
        for column, expected_value in expected_kendall['Salary'].items():
            actual_value = result['kendall']['Salary'][column]
            self.assertEqual(actual_value, expected_value,
                msg=f"Kendall correlation for 'Salary' with '{column}' does not match. Expected: {expected_value}, Actual: {actual_value}")

        # Check Kendall correlation results for 'Graduated'
        for column, expected_value in expected_kendall['Graduated'].items():
            actual_value = result['kendall']['Graduated'][column]
            self.assertEqual(actual_value, expected_value,
                msg=f"Kendall correlation for 'Graduated' with '{column}' does not match. Expected: {expected_value}, Actual: {actual_value}")


    '''
    Tests the results in the case of an invalid dataset
    '''
    def test_invalid_data(self):
        # Test with empty data
        empty_data = pd.DataFrame()
        with self.assertRaises(ValueError, msg="Data needed for Correlation Analysis"):
            compute_corr(['Salary'], empty_data)
        
        # Test with non-numeric data
        invalid_data = pd.DataFrame({
            'Letters': ['a', 'b', 'c']
        })
        result = compute_corr(['Letters'], invalid_data)
        self.assertIn('pearson', result)
        self.assertIsInstance(result['pearson'], str, 
            msg="Expected the result to be an exception message for 'pearson' correlation due to non-numeric data")
        self.assertIn('spearman', result)
        self.assertIsInstance(result['spearman'], str, 
            msg="Expected the result to be an exception message for 'spearman' correlation due to non-numeric data")
        self.assertIn('kendall', result)
        self.assertIsInstance(result['kendall'], str, 
            msg="Expected the result to be an exception message for 'kendall' correlation due to non-numeric data")

    '''
    Tests the results in the case of invalid sensitive column
    '''
    def test_invalid_sensitive_col(self):
        with self.assertRaises(ValueError, msg="Sensitive Variables needed for Correlation Analysis"):
            compute_corr(None, self.data)
        invalid_sensitive_var = ['non_existent_column']
        with self.assertRaises(ValueError, msg="Sensitive variable(s) ['non_existent_column'] not found in the data columns for Correlation Analysis"):
            compute_corr(invalid_sensitive_var, self.data)

if __name__ == '__main__':
    unittest.main()
