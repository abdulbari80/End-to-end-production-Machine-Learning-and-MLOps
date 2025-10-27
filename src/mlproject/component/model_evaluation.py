import joblib
import os
from sklearn.metrics import (r2_score, mean_absolute_error, 
                             root_mean_squared_error)

import joblib
import mlflow
import mlflow.sklearn
import mlflow.xgboost
from src.mlproject.entity.config_entity import ModelEvaluationConfig
from src.mlproject import logging
from box.exceptions import BoxValueError

class ModelEvaluation():
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def evaluate_models(self) -> list:
        try: 
            test_arr = joblib.load(self.config.test_data_path)
            X_test = test_arr[:, :-1]
            y_test = test_arr[:,-1]
            results = joblib.load(self.config.grid_result_path)
            # update grid result with 3 parameters predicted on test dataset
            for name, value in results.items():
            
                model = value['model']
                y_pred = model.predict(X_test)
                mae = int(round(mean_absolute_error(y_test, y_pred), 0))
                rmse = int(round(root_mean_squared_error(y_test, y_pred), 0))
                test_r2 = round(r2_score(y_test, y_pred), 4)
                test_scores = {
                    'mae' : mae,
                    'rmse' : rmse,
                    'test_r2': test_r2}
                results[name]['test_scores'] = test_scores
            # sort models based on test MAE score
            sorted_results = sorted(results.items(), 
                                  key=lambda x: x[1]['test_scores']['mae'], 
                                  reverse=False)
            # store results metric
            result_metrics = dict(sorted_results)
            eval_config = os.path.join(self.config.root_dir, self.config.resuslt_metrics)
            joblib.dump(result_metrics, eval_config)
            
            return sorted_results
        
        except BoxValueError as e:
             logging.error(f"Error: {e}")

    def find_prod_model(self):
        try:
            top_model = self.evaluate_models()[0]
            # save best model for deploymnet
            champ_model = top_model[1]['model']
            scores = top_model[1]['test_scores']
            champ_config = os.path.join(self.config.root_dir, self.config.champ_model)
            joblib.dump(champ_model, champ_config)
            logging.info(f"Champion Model: {top_model[0]} saved to {self.config.root_dir}")
            logging.info(f"Champion model mae:{scores['mae']}, \
                         rmse: {scores['rmse']}, r2: {scores['test_r2']:.3f}")
        
        except BoxValueError as e:
            logging.error("Error: {e}")

    def run_mlflow(self, top_n=3):
        try:
            logging.info("MLflow experiment starts") 
            top_n_models = self.evaluate_models()[:top_n]
            
            mlflow.set_experiment("ds-salary-prediction")
            mlflow.set_tracking_uri(uri=self.config.mlflow_uri)

            for element in top_n_models:
                with mlflow.start_run(run_name=f"{element[0]}_v6"):
                    mlflow.log_params(element[1]['best_params'])
                    mlflow.log_metric('mae', element[1]['test_scores']['mae'])
                    mlflow.log_metric('rmse', element[1]['test_scores']['rmse'])
                    mlflow.log_metric('r2_score', element[1]['test_scores']['test_r2'])
                    if 'xgb' in element[0]: 
                        mlflow.xgboost.log_model(element[1]['model'], f"{element[0]}_v6")
                    else:                                           
                        mlflow.sklearn.log_model(element[1]['model'], f"{element[0]}_v6")
                
                # Register the champion model with MLflow
                
                model_name = "cat_v6"
                run_id = "f44f5fcbfd1c40f982a57ab89cfb73b4"
                model_uri = f"runs:/{run_id}/{model_name}"
                results = mlflow.register_model(model_uri=model_uri, 
                                                name="CatBoost")
                
        except BoxValueError as e:
            logging.error(f"Error: {e}")

