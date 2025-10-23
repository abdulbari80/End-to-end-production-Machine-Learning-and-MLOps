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

    def evaluate_model(self):
        try: 
            test_arr = joblib.load(self.config.test_data_path)
            X_test = test_arr[:, :-1]
            y_test = test_arr[:,-1]
            results = joblib.load(self.config.grid_result_path)
            # update grid result with 3 parameters predicted on test dataset
            for element in results:
                mae = round(mean_absolute_error(y_test, element[1][0].predict(X_test)), 1)
                element[1][1][0] = mae
                rmse = round(root_mean_squared_error(y_test, element[1][0].predict(X_test)), 1)
                element[1][1].append(rmse)
                test_r2 = round(r2_score(y_test, element[1][0].predict(X_test)), 3)
                element[1][1].append(test_r2)
            
            # Re-rank models based on test results for MAE score
            test_results = sorted(results, key=lambda x: x[1][1][0])
            # save best model for deploymnet
            top_model = test_results[0][1][0]
            joblib.dump(top_model, os.path.join(self.config.root_dir, self.config.model_name))
            logging.info(f"Champion Model: {top_model} saved to {self.config.root_dir}")
            return results
        
        except BoxValueError as e:
            logging.error("Error: {e}")

    def run_mlflow(self):
        try: 
            results = self.evaluate_model()
            param_mlflow= {}
            for element in results:
                model = element[1][0]
                params_all = model.get_params()
                params_reset = element[1][2]
                param_mlflow[element[0]] = {k: params_all[k] for k in 
                                            params_reset if k in params_all}
            

            #from mlflow.models import infer_signature
            mlflow.set_experiment("DS Salaries")
            mlflow.set_tracking_uri(uri=self.config.mlflow_uri)

            for element in results:
                with mlflow.start_run(run_name=f"{element[0]}_v3"):
                    mlflow.log_params(param_mlflow[element[0]])
                    mlflow.log_metric('mae', element[1][1][0])
                    mlflow.log_metric('rmse', element[1][1][1])
                    mlflow.log_metric('r2_score', element[1][1][2])
                    if 'XGB' in element[0]: 
                        mlflow.xgboost.log_model(element[1][0], f"{element[0]}_v3")
                    else:                                           
                        mlflow.sklearn.log_model(element[1][0], f"{element[0]}_v3")
                # Register the champion model wity MLflow
                model_name = "ElasticNetv_3"
                run_id = "9b715296519a40d6ae96bded389ab97b"
                model_uri = f"runs:/{run_id}/{model_name}"
                results = mlflow.register_model(model_uri=model_uri, 
                                                name="ElasticNet")
        except BoxValueError as e:
            logging.error(f"Error: {e}")

