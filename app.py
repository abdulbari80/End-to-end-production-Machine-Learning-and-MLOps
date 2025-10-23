from flask import Flask, request, render_template
from src.mlproject.pipeline.prediction import Prediction

application = Flask(__name__)
app = application

@app.route('/', methods=['GET', 'POST'], endpoint='predict_user_salary')
def predict():
    if request.method == 'POST':
        user_input = Prediction(
            work_year=request.form.get('work_year'),
            experience_level=request.form.get('experience_level'),
            employment_type=request.form.get('employment_type'),
            remote_ratio=request.form.get('remote_ratio'),
            company_size=request.form.get('company_size'),
            job_category=request.form.get('job_category'),
            employee_residence=request.form.get('employee_residence'),
            company_location=request.form.get('company_location')
        )
        result = user_input.get_prediction()
        if result < 6021:
            return render_template('index.html', results=f"Too low prediction.\nPlz check input combination.")  
        else:
            result = int(round(result/1000, 0))
            return render_template('index.html', results=f"Folk, you deserve US$ {result}-K a year!")

    # GET request
    return render_template('index.html', results=None)


if __name__ == "__main__":
    # Debug true is good for dev, turn off in prod
    app.run(host="0.0.0.0", port=5000, debug=True)
