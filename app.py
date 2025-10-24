from flask import Flask, request, render_template
import requests
from prediction import Prediction
from dotenv import load_dotenv
import os

load_dotenv()

application = Flask(__name__)
app = application

# 🔐 Placeholders for your actual keys
RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

@app.route('/', methods=['GET', 'POST'], endpoint='predict_user_salary')
def predict():
    if request.method == 'POST':
        # --- Verify reCAPTCHA token ---
        token = request.form.get('g-recaptcha-response')
        verify_url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {'secret': RECAPTCHA_SECRET_KEY, 'response': token}
        response = requests.post(verify_url, data=payload)
        result_json = response.json()

        if not result_json.get('success'):
            return render_template('index.html',
                                   site_key=RECAPTCHA_SITE_KEY,
                                   results="Captcha verification failed. Please try again.")

        # --- Proceed with prediction ---
        user_input = Prediction(
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
            message = "Sorry, mate! It's too low. Plz check input combination."
        else:
            result = int(round(result / 1000, 0))
            message = f"Hey mate, you deserve {result}K!"

        return render_template('index.html', site_key=RECAPTCHA_SITE_KEY, results=message)

    # --- GET request ---
    return render_template('index.html', site_key=RECAPTCHA_SITE_KEY, results=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
