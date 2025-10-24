import joblib
import pandas as pd
from src.mlproject.config.configuration import ConfigurationManager

class Prediction:
    def __init__(self,
                 experience_level: str,
                 employment_type: str,
                 remote_ratio: str,
                 company_size: str,
                 job_category: str,
                 employee_residence: str,
                 company_location: str
                 ):

        self.experience_level = experience_level
        self.employment_type = employment_type
        self.remote_ratio = remote_ratio
        self.company_size = company_size
        self.job_category = job_category
        self.employee_residence = employee_residence
        self.company_location = company_location

    def get_prediction(self):
        config = ConfigurationManager().get_unit_test_config()
        user_input = {
            'experience_level' : self.experience_level,
            'employment_type' : self.employment_type,
            'remote_ratio' : self.remote_ratio,
            'company_size' : self.company_size,
            'job_category' : self.job_category,
            'employee_residence_top': self.employee_residence,
            'company_location_top': self.company_location
        }
        df_user_input = pd.DataFrame(data=user_input, index=[0])
        
        data_process_pipe_obj = joblib.load(config.data_transform_obj_path)
        user_input_arr = data_process_pipe_obj.transform(df_user_input)
        prod_model = joblib.load(config.prod_model_path)
        pred_result = prod_model.predict(user_input_arr)[0]

        return pred_result
