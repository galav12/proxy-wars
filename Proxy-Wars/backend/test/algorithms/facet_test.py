'''
facet_test.py
Unit tests for the FACET algorithm.

Key functionalities:
- Defines test cases to validate the expected output for valid inputs.
- Ensures that appropriate errors are raised for missing or invalid data.
- Tests edge cases such as empty datasets, non-numeric data, and missing sensitive/target variables.
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import unittest
import pandas as pd
from algorithms.facet_alg import compute_facet

'''
This class contains unit tests for the compute_corr function which calculates 
redundancy values between sensitive variables and all other variables in a dataset.
'''
class TestComputeFacet(unittest.TestCase):

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
    Tests the results of the FACET algorithm with one sensitive variable
    '''
    def test_valid_input(self):
        sensitive_variables = ['Graduated']
        target_var = 'Salary'
        result = compute_facet(sensitive_variables, self.data, target_var)
        expected_result = {
            'Graduated': {
                'Religious': 0.0,
                'IQ': 0.0,
                'Height': 0.0,
                'id': 0.0,
                'Age': 0.0,
                'Speed': 0.0,
                'Weight': 0.0,
                'Gender': 0.0,
                'Graduated': 'NaN'
            }
        }
        self.assertIsInstance(result, dict)
        self.assertTrue(all(var in result for var in sensitive_variables))
        self.assertEqual(result, expected_result)
    
    '''
    Tests the results in the case of an invalid dataset
    '''
    def test_invalid_data(self):
        # Test with empty data
        empty_data = pd.DataFrame()
        sensitive_variables = ['Graduated']
        target_var = 'Salary'
        with self.assertRaises(ValueError, msg="Data needed for FACET"):
            compute_facet(sensitive_variables, empty_data, target_var)
        # Test with non-numeric data
        invalid_data = pd.DataFrame({
            'Letters': ['a', 'b', 'c']  # Non-numeric data that will cause an exception
        })
        with self.assertRaises(ValueError, msg="Cannot have number of splits n_splits=5 greater than the number of samples: n_samples=3."):
            compute_facet(['Letters'], invalid_data, 'Letters')

    '''
    Tests the results in the case of invalid sensitive column
    '''
    def test_invalid_sensitive_col(self):
        invalid_sensitive_var = ['non_existent_column']
        target_var = 'Salary'
        with self.assertRaises(ValueError, msg="Sensitive Variables needed for FACET"):
            compute_facet(None, self.data, target_var)
        with self.assertRaises(ValueError, msg="Sensitive variable(s) ['non_existent_column'] not found in the data columns for FACET"):
            compute_facet(invalid_sensitive_var, self.data, target_var)

    '''
    Tests the results in the case of an empty dataset
    '''
    def test_invalid_target_col(self):
        sensitive_variables = ['Graduated']
        invalid_target_var = 'non_existent_column'
        with self.assertRaises(ValueError, msg="Target Variable(s) needed for FACET"):
            compute_facet(sensitive_variables, self.data, None)
        with self.assertRaises(ValueError, msg="Target variable(s) non_existent_column not found in the data columns for FACET"):
            compute_facet(sensitive_variables, self.data, invalid_target_var)

if __name__ == '__main__':
    unittest.main()
