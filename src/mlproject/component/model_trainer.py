import joblib
import os
from src.mlproject.entity.config_entity import ModelTrainerConfig
from src.mlproject import logging
from box.exceptions import BoxValueError

from catboost import CatBoostRegressor
from sklearn.ensemble import (RandomForestRegressor,
                              AdaBoostRegressor,
                              GradientBoostingRegressor)
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression   
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

class ModelTrainer:
    def __init__(self, config:ModelTrainerConfig):
        self.config=config

    def evaluate_model(self, models:dict, params:dict, cv=3) -> dict:
        try:
            data_arr = joblib.load(self.config.train_array_path)
            train_arr, validation_arr = train_test_split(data_arr, test_size=0.2, 
                                                         random_state=42)
            X_train = train_arr[:,:-1]
            y_trian = train_arr[:,-1]
            X_valid= validation_arr[:,:-1]
            y_valid = validation_arr[:,-1]
            logging.info("Processed data loaded and partitioned")
            grid_report = {}
            logging.info("GridSearchCV starts to iterate over the chosen models")
            # Iterate over selected models to find optimal parameter combination
            iteration = 0
            for name, model in models.items():
                gsc = GridSearchCV(model, params[name], cv=cv)
                gsc.fit(X_train, y_trian)
                model.set_params(**gsc.best_params_)
                model.fit(X_train, y_trian)
                y_pred = model.predict(X_valid)
                grid_report[name] = r2_score(y_valid, y_pred)
                iteration += 1
                logging.info(f"{iteration} iteration(s) completed")
            
            return grid_report
        
        except BoxValueError as e:
            logging.error(f"Error: {e}")

    def find_best_model(self):
        try:
            logging.info('Instantiate models and set hyperparameters')
            models = {
                'Linear Regression': LinearRegression(),
                'Decision Tree': DecisionTreeRegressor(),
                'Random Forest': RandomForestRegressor(),
                'Gradient Boosting': GradientBoostingRegressor(),
                'XGBoosting': XGBRegressor(),
                'AdaBoost': AdaBoostRegressor(),
                'CatBoost': CatBoostRegressor(verbose=False),
                'SVM': SVR() 
            }

            params = {
                'Linear Regression': {},
                'Decision Tree': {},
                'Random Forest': {
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                'Gradient Boosting': {
                    'learning_rate': [0.1, 0.05, 0.01],
                    'n_estimators': [16, 32, 64, 128, 256],
                    'subsample': [0.6, 0.7, 0.8]
                },
                'XGBoosting': {
                    'learning_rate': [0.1, 0.05, 0.01],
                    'n_estimators': [16, 32, 64, 128, 256]
                },
                'AdaBoost': {
                    'learning_rate': [0.1, 0.05,0.01],
                    'n_estimators': [16, 32, 64, 128, 256]
                },
                'CatBoost': {
                    'learning_rate': [0.1, 0.05, 0.01],
                    'depth': [6, 8, 10],
                    'iterations': [30, 50, 100]
                },
                'SVM': {
                     'kernel': ['linear', 'poly', 'rbf'], 
                     'epsilon': [0.1, .05, .01]
                     
                }
            }
            logging.info("Model evaluation starts >>>>>")
            results = self.evaluate_model(models, params, cv=4)
            best_model_name = max(results, key=results.get)
            logging.info("Best model identified!")
            best_model = models[best_model_name]
            best_model_r2 = results[best_model_name]
            joblib.dump(best_model, os.path.join(self.config.root_dir, 
                                                 self.config.model_name
                                                 ))
            logging.info("Best model saved in the artifacts!")
            logging.info(f"Best model: {best_model_name} with R2 score: {best_model_r2}")

        except BoxValueError as e:
            logging.error(f"Error: {e}")
