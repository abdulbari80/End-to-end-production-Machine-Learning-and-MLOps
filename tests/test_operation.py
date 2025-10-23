import os
import unittest
import joblib
import numpy as np
from src.mlproject.config.configuration import ConfigurationManager

class TestMlProject(unittest.TestCase):

    def setUp(self):
        self.config = ConfigurationManager().get_unit_test_config()

    def test_data_transfromation(self):
        self.assertTrue(os.path.exists(self.config.data_transform_obj_path
                                       ), "No data transformation object")
        self.assertTrue(self.config.data_transform_obj_path.endswith('.joblib'),
                        'Object file extension is not .joblib')
        train_arr = joblib.load(self.config.train_arrary_path)
        self.assertIsInstance(train_arr, np.ndarray, "Training data is numpy ndarray")
        self.assertFalse(np.isnan(train_arr).any(), "Transformed trained data is NaN")
        test_arr = joblib.load(self.config.test_array_path)
        self.assertIsNotNone(test_arr, "Transformed test data is None")
        self.assertEqual(train_arr.shape[1], test_arr.shape[1])
    
    def test_model_training(self):
        result_path = self.config.training_result_path
        result = joblib.load(result_path)
        score = result[0][1][1][0]
        self.assertIsNotNone(result, "The grid result is None")
        self.assertIsInstance(score, float, "Model error score is not a float")
    
    def test_model_evaluation(self):
        model_path = self.config.prod_model_path
        prod_model = joblib.load(model_path)
        self.assertIsNone(prod_model, "The production model is None")
    
if __name__ == '__main__':
    unittest.main()