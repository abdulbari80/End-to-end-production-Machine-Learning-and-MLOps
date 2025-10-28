## AI/ ML/ Data Professionals' Salary Prediction

**Data Collection & Preparation:** This is an end-to-end machine learning project following MLOps principles. The dataset is chosen from Kaggle. Though the data is fairly clean, the year of salaries(target variable) ranges from 2019 to 2023. Hence, the salary figures are projected to the current year 2025 with the global/ US annaul inflation rates to keep the salary figures updated. After relevant EDA, the dataset is split among training, validation and test sets. Scikit Learn's Column Transformer class is applied to process categorical data for training model with ML algorithms. 

**Model Training & Hyperparameter Tuning:** Then, a couple of supervised learning algorithms from different categories, such as linear method (Ridge, Lasso, Elastic Net), SVM and ensemble techniques (Random Forest, AdaBoost, Gradient Boost) etc. are applied to train several models. Besides, Scikit Learn's GridSearchCV class is also applied to tune hyperparameters. 

**Model Evaluation & Performance Tracking:** Model performances are evaluated with airmarked test dataset, model, parameters and results are logged with MLflow. The best performing model is singled out for production.

**App and UI:** Python;s Flask API along with html and css files are developed for building web app with cool UI and UX. 

**Deployment:** GitHub Action CI/CD is used to build and push docker image to Azure Cotainer Register. Finally, Azure Web App is created and deployed to bring ML to life. Again, continuous development is activated to automate deployment of the upcoming versions.
