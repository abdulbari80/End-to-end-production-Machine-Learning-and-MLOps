from src.mlproject.entity.config_entity import DataTransformationConfig
from sklearn.model_selection import train_test_split
from src.mlproject import logging
import pandas as pd
import os
import joblib
from box.exceptions import BoxValueError

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.api.types import is_numeric_dtype
import matplotlib.pyplot as plt

# Import Statistics libraries
from scipy import stats
from scipy.stats import norm

# Import Scikit-learn for Machine Learning libraries
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from feature_engine.encoding import RareLabelEncoder

# Import country code libraries
import pycountry

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
    
    def broad_job_category(self, job_title):
        bi_analyst = ['BI Data Analyst', 'Business Data Analyst', 'BI Developer', 'BI Analyst', 
                        'Business Intelligence Engineer', 'BI Data Engineer', 'Power BI Developer']
        data_analyst = ['Data Analyst', 'Data Quality Analyst', 'Product Data Analyst', 'Data Analytics Lead' 
                        'Data Lead', 'Finance Data Analyst', 'Insight Analyst', 'Lead Data Analyst',
                        'Financial Data Analyst', 'Staff Data Analyst', 'Compliance Data Analyst',
                        'Data Analytics Engineer', 'Data Operations Analyst', 'Data Analytics Lead',
                        'Data Analytics Specialist', 'Data Analytics Consultant', 
                        'Marketing Data Analyst', 'Principal Data Analyst']
        data_scientist = ['Data Scientist', 'Applied Scientist', 'Research Scientist', 
                          'Lead Data Scientist', '3D Computer Vision Researcher', 
                          'Deep Learning Researcher', 'Staff Data Scientist', 
                          'Data Science Lead', 'Data Science Consultant', 
                          'Product Data Scientist', 'Data Science Tech Lead',
                          'Applied Data Scientist', 'Principal Data Scientist', 
                          'Data Science Engineer', 'Data Modeler']
        ai_engineer = ['AI/Computer Vision Engineer', 'Computer Vision Software Engineer',
                       'AI Scientist', 'AI Programmer', 'AI Developer', 
                       'Computer Vision Engineer', 'Deep Learning Engineer']
        ml_engineer = ['Machine Learning Engineer', 'ML Engineer', 
                       'Lead Machine Learning Engineer', 'Principal Machine Learning Engineer',
                        'Machine Learning Scientist', 'MLOps Engineer', 'NLP Engineer',
                        'Applied Machine Learning Scientist', 
                        'Machine Learning Software Engineer', 
                        'Applied Machine Learning Engineer', 'Machine Learning Developer', 
                        'Machine Learning Infrastructure Engineer']
        data_engr = ['Data Engineer', 'ETL Developer', 'Big Data Engineer', 
                     'Azure Data Engineer', 'Lead Data Engineer', 'Analytics Engineer', 
                     'Data Operations Engineer', 'Cloud Data Engineer', 
                     'Marketing Data Engineer', 'ETL Engineer', 'Principal Data Engineer', 
                     'Software Data Engineer', 'Software Data Engineer',
                     'Cloud Database Engineer', 'Data DevOps Engineer']
        data_arch = ['Data Architect', 'Big Data Architect', 'Data Infrastructure Engineer',
                     'Cloud Data Architect', 'Cloud Data Architect', 'Principal Data Architect']
        executive = ['Data Science Manager', 'Director of Data Science', 'Head of Data Science',
                     'Data Scientist Lead', 'Head of Machine Learning', 'Manager Data Management',
                     'Data Analytics Manager', 'Data Manager']
        data_management = ['Data Specialist', 'Head of Data', 'Data Management Specialist',
                           'Head of Data', 'Data Lead', 'Data Strategist', 'Machine Learning Manager']
        ai_ml_researcher = ['Machine Learning Researcher', 'Machine Learning Research Engineer',
                            'Research Engineer']
            
        if job_title in bi_analyst:
                return "BI Analyst"
        elif job_title in data_scientist:
                return "Data Scientist"
        elif job_title in ml_engineer:
                return "ML Engineer"
        elif job_title in data_engr:
                return "Data Engineer"
        elif job_title in data_arch:
                return "Data Architect"
        elif job_title in executive:
                return "DS/AI Executive"
        elif job_title in data_analyst:
                return "Data Analyst"
        elif job_title in ai_engineer:
                return "AI Engineer"
        elif job_title in data_management:
                return "Data Management"
        elif job_title in ai_ml_researcher:
                return "AI/ML Researcher"
        else:
                return job_title
            
    def country_code_to_name(self, code):
        """This converts ISO 3166 country code to country name"""
        try:
            return pycountry.countries.get(alpha_2=code).name
        except:
            return None  # Use None so it can be safely skipped later if needed
        
    def adjust_salary(self, data:pd.DataFrame):
        """This adjusts previous salaries with the following years' inflation rates"""
        year = data['work_year']
        currency = data['salary_currency']
        salary_usd = data['salary_in_usd']
        # Inflation rates
        us_inflation_rates = {2019: 0.018, 2020: 0.012, 2021: 0.047, 
                            2022: 0.08, 2023: 0.041, 2024: 0.029, 2025: 0.02}
        global_inflation_rates = {2019: 0.019, 2020: 0.019, 2021: 0.035, 
                                2022: 0.057, 2023: 0.049, 2024: 0.058, 2025: 0.036}
        adjsuted_salary = salary_usd
        for y in range(year, 2025):
            if currency == 'USD':
                inflation_rate = us_inflation_rates[y]
            else:
                inflation_rate = global_inflation_rates[y]
            adjsuted_salary *= (1+inflation_rate)
            adjsuted_salary = int(round(adjsuted_salary, 0))

        return adjsuted_salary

    def get_data_transformation(self):
        """This splits dataset into train and test sets
        and return None"""
        df = pd.read_csv(self.config.data_path)
        # Remove duplicate instances
        df.drop_duplicates(inplace=True)
        # abbreviated values are replaced with full form
        df['experience_level'] = df['experience_level'].replace(
            {'SE': 'Senior',
            'EN': 'Entry level',
            'EX': 'Executive level',
            'MI': 'Mid/Intermediate level'}
            )
        # abbreviated values are replaced with full form
        df['employment_type'] = df['employment_type'].replace(
            {
            'FL': 'Freelancer',
            'CT': 'Contractor',
            'FT' : 'Full-time',
            'PT' : 'Part-time'}
            )
        # remote work ratio is converted from numeric to categorical
        df['remote_ratio'] = df['remote_ratio'].replace(
            {'0': 'On site',
             '50': 'Hybride',
             '100': 'Remote'}
            )
        # Company size is mapped to full form
        df['company_size'] = df['company_size'].replace(
            {'L': 'Large',
             'M': 'Medium',
             'S': 'Small'}
             )

        # Apply the function to the 'job_title' column and create a new column 'job_category'
        df['job_category'] = df['job_title'].apply(self.broad_job_category)
        # Two instances with an unusual job category is dropped
        df = df[~(df['job_category'] == 'Autonomous Vehicle Technician')]
        df['job_category'].value_counts()
        # Country codes are mapped to country names
        df['company_location'] = df['company_location'].apply(self.country_code_to_name)
        df['employee_residence'] = df['employee_residence'].apply(self.country_code_to_name)
        
        df['inflation_adj_salary'] = df.apply(self.adjust_salary, axis=1)
        df['work_year'] = df['work_year'].astype('category')

        cols_to_drop = ['job_title', 'salary', 'salary_currency',
                        'salary_in_usd', 'employee_residence_top',
                        'company_location_top']
        cols_df = df.columns.to_list()
        final_cols_to_drop = []
        for col in cols_to_drop:
              if col in cols_df:
                    final_cols_to_drop.append(col)
        df_tr = df.drop(columns = final_cols_to_drop,
                                   axis=1)
        # Many outliers observed in salary variable during EDA
        # Hence, those outliers are removed to enhance prediction accuracy
        q1 = df_tr['inflation_adj_salary'].quantile(0.25)
        q3 = df_tr['inflation_adj_salary'].quantile(0.75)
        iqr = q3 - q1
        df_outlier_free = df_tr[~((df_tr['inflation_adj_salary'] < (q1-1.5*iqr)) | (
            df_tr['inflation_adj_salary'] > (q3+1.5*iqr)))]
        # Processed dataset is saved to artifacts
        df_outlier_free.to_csv(os.path.join(self.config.root_dir, 'processed_data.csv'), index=False)
    
        return df_outlier_free
    
    def get_col_transformer_pipeline(self):
        logging.info('Data transformation starts >>>>>')
        try:
            rare_cat_columns = ['employee_residence', 'company_location']
            cat_columns = ['work_year', 
                           'experience_level', 
                           'employment_type',
                           'remote_ratio', 
                           'company_size', 
                           'job_category']
            rare_cat_pipeline = Pipeline(
                steps=[
                    ('rare_cat_pipeline', SimpleImputer(strategy='most_frequent')),
                    ('rare_label_encoder', RareLabelEncoder(tol=0.01, 
                                                            n_categories=10,
                                                            replace_with='Other'))
                ]
            )
            cat_pipeline = Pipeline(
                steps = [
                    ('cat_pipeline', SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encode', OneHotEncoder(handle_unknown='ignore',
                                                     sparse_output=False))
                        ])

            trans_cols = ColumnTransformer(
                [
                    ('num_pipeline', rare_cat_pipeline, rare_cat_columns),
                    ('cat_pipeline', cat_pipeline, cat_columns)
                ]
            )
            logging.info('Data preprocessing pipeline created.')
            return trans_cols           
        except BoxValueError as e:
            logging.error(f"{e}")

    def initiate_data_transformation(self, test_size:float=0.20):
        """ This saves fitted proprocessing model
        Parameter:
            train_data_path(str): training data file path
            test_data_path(str): testing data file path

        Return:
            (array): train_arr: transformed training array
            (array): test_arr: transformed testing array
            (str): preprocessor_obj_path: saved preprocessor object file path
        """
        try:
            df = self.get_data_transformation()
            df_train, df_test = train_test_split(df,
                                       test_size=test_size,
                                       random_state=42)
            dataset = [(df_train, 'train.csv'),
                       (df_test, 'test.csv')]
            # Save train and test datasets in the artifacts
            for data in dataset:
                data[0].to_csv(os.path.join(self.config.root_dir, data[1]), 
                               index=False)
            target_variable = 'inflation_adj_salary'
            X_train = df_train.drop(columns=[target_variable], axis=1)
            y_train = df_train[target_variable]
            X_test = df_test.drop(columns=[target_variable], axis=1)
            y_test = df_test[target_variable]

            column_transormer_pipeline = self.get_col_transformer_pipeline()
            logging.info("column transformer is intantiated")
            X_train_arr = column_transormer_pipeline.fit_transform(X_train)
            X_test_arr = column_transormer_pipeline.transform(X_test)
            logging.info("Data columns are transformed")
            train_arr = np.c_[X_train_arr, np.array(y_train)]
            test_arr = np.c_[X_test_arr, np.array(y_test)]
            joblib.dump(column_transormer_pipeline, 
                        os.path.join(self.config.root_dir, 
                                     self.config.data_transform_obj_name))
            joblib.dump(train_arr, os.path.join(self.config.root_dir, 
                                                self.config.train_array))
            joblib.dump(test_arr, os.path.join(self.config.root_dir, 
                                               self.config.test_array))
            #return (train_arr, test_arr)
        except BoxValueError as e:
            logging.error(f"{e}")