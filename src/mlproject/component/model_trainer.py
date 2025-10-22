import joblib
import os
from datetime import datetime
from src.mlproject.entity.config_entity import ModelTrainerConfig
from src.mlproject import logging
from box.exceptions import BoxValueError

from catboost import CatBoostRegressor
from sklearn.ensemble import (RandomForestRegressor,
                              AdaBoostRegressor,
                              GradientBoostingRegressor)
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet 
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

class ModelTrainer:
    def __init__(self, config:ModelTrainerConfig):
        self.config=config

    def train_model_grid_search(self, models:dict, params:dict, *, cv=3) -> dict:
        try:
            data_arr = joblib.load(self.config.train_array_path)
            X_train = data_arr[:,:-1]
            y_trian = data_arr[:,-1]
            grid_result = {}
            logging.info("GridSearchCV starts to iterate over each model")
            total_sec = 0
            # Iterate over selected models to find optimal parameter combination
            for name, model in models.items():
                start_time = datetime.now()
                # List initiated to sort models with respective r2 score
                result = []
                gsc = GridSearchCV(model, 
                                   params[name], 
                                   cv=cv, 
                                   scoring='r2',
                                   refit=True,
                                   n_jobs=-1)
                gsc.fit(X_train, y_trian)
                result.append(gsc.best_estimator_)
                score = []
                score.append(gsc.best_score_)
                result.append(score)
                result.append(list(params[name].keys()))
                grid_result[name] = result
                end_time = datetime.now()
                duration = end_time - start_time
                dur_in_sec = int(duration.total_seconds())
                total_sec += dur_in_sec
                dur_in_min = dur_in_sec // 60
                dur_in_sec = dur_in_sec % 60
                logging.info(f"{name} trained in {dur_in_min}m: {dur_in_sec}s")
            total_min = total_sec // 60
            total_sec = total_sec % 60
            logging.info(f"Total training time: {total_min}m: {total_sec}s")
            return grid_result
        
        except BoxValueError as e:
            logging.error(f"Error: {e}")

    def find_top_models(self, top_n=3):
        try:
            models = {
                'Linear Regression': LinearRegression(),
                'Ridge': Ridge(),
                'Lasso': Lasso(max_iter=15000),
                'ElasticNet': ElasticNet(max_iter=15000),
                'Random Forest': RandomForestRegressor(),
                'Gradient Boosting': GradientBoostingRegressor(),
                'XGBoosting': XGBRegressor(),
                'AdaBoost': AdaBoostRegressor(),
                'CatBoost': CatBoostRegressor(verbose=False),
            }

            params = {
                'Linear Regression': {},
                'Ridge': {
                    'alpha': [1, 5, 10, 15, 20]
                },
                'Lasso': {
                    'alpha': [10, 15, 20, 25, 30]
                },
                'ElasticNet': {
                    'alpha': [0.001, 0.01, 0.1, 1, 2],
                    'l1_ratio': [0.6, 0.5, 0.4, 0.30]
                },
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
                }
            }
            
            results = self.train_model_grid_search(models, params,cv=3)
            logging.info(">>>>> Grid search finished!")
            # Select top three models based on mean_absolute_error
            top_3_model = sorted(results.items(), 
                                 key=lambda item:item[1][1][0], reverse=True)[:top_n]
            ## to locate source of error
            logging.info(">>>>> top models sorted!!!")
            joblib.dump(top_3_model, os.path.join(self.config.root_dir,
                                              self.config.grid_result))
            logging.info("Top three models are saved in the artifacts!")
            best_model = top_3_model[1]
            joblib.dump(best_model, os.path.join(self.config.root_dir, 
                                                 self.config.model_name))
            logging.info("Best model saved in the artifacts!")
            logging.info(f"Best model: {best_model[0]}, mae: {best_model[1][1]}")

        except BoxValueError as e:
            logging.error(f"Error: {e}")
