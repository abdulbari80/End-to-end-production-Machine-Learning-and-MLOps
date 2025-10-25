from flask import Flask, request, render_template
import requests
from prediction import Prediction
from dotenv import load_dotenv
import os

load_dotenv()

application = Flask(__name__)
app = application

# reCAPTCHA keys
RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")


@app.route("/", methods=["GET", "POST"], endpoint="predict_user_salary")
def predict():
    if request.method == "POST":
        form_data = request.form.to_dict()
        print("📩 Received POST data:", form_data)

        # ✅ Match all field names exactly as in HTML
        experience_level = form_data.get("experience_level", "").strip()
        employment_type = form_data.get("employment_type", "").strip()
        remote_ratio = form_data.get("remote_ratio", "").strip()
        company_size = form_data.get("company_size", "").strip()
        job_category = form_data.get("job_category", "").strip()
        employee_residence_top = form_data.get("employee_residence_top", "").strip()
        company_location_top = form_data.get("company_location_top", "").strip()

        # Validation
        missing_fields = []
        if not experience_level: missing_fields.append("Experience Level")
        if not employment_type: missing_fields.append("Employment Type")
        if not remote_ratio: missing_fields.append("Office Attendance")
        if not company_size: missing_fields.append("Company Size")
        if not job_category: missing_fields.append("Job Role")
        if not employee_residence_top: missing_fields.append("Your Residence")
        if not company_location_top: missing_fields.append("Company Location")

        if missing_fields:
            print(f"⚠️ Missing fields: {missing_fields}")
            return render_template(
                "index.html",
                site_key=RECAPTCHA_SITE_KEY,
                results="Please fill in all fields before asking Maban.",
            )

        # Optional reCAPTCHA
        token = form_data.get("g-recaptcha-response")
        if token:
            verify_url = "https://www.google.com/recaptcha/api/siteverify"
            payload = {"secret": RECAPTCHA_SECRET_KEY, "response": token}
            try:
                response = requests.post(verify_url, data=payload)
                result_json = response.json()
                if not result_json.get("success"):
                    print("❌ reCAPTCHA failed:", result_json)
                    return render_template(
                        "index.html",
                        site_key=RECAPTCHA_SITE_KEY,
                        results="Captcha verification failed. Please try again.",
                    )
            except Exception as e:
                print("⚠️ reCAPTCHA error:", e)

        # 🧠 Prediction
        try:
            predictor = Prediction(
                experience_level=experience_level,
                employment_type=employment_type,
                remote_ratio=remote_ratio,
                company_size=company_size,
                job_category=job_category,
                employee_residence_top=employee_residence_top,
                company_location_top=company_location_top,
            )
            result = predictor.get_prediction()
            print("✅ Model prediction:", result)
        except Exception as e:
            print("❌ Prediction error:", e)
            return render_template(
                "index.html",
                site_key=RECAPTCHA_SITE_KEY,
                results=f"Error during prediction: {e}",
            )

        # 🎯 Format result nicely
        try:
            result_value = float(result)
        except ValueError:
            result_value = 0

        if result_value < 6021:
            message = "Hmm... that seems too low. Please check your input combination."
        else:
            salary_k = int(round(result_value / 1000, 0))
            message = (
                f"<strong style='font-size:1.5em; color:#7B61FF;'>{salary_k}K</strong> US$ a year, mate!"
            )

        return render_template(
            "index.html",
            site_key=RECAPTCHA_SITE_KEY,
            results=message,
        )

    return render_template("index.html", site_key=RECAPTCHA_SITE_KEY, results=None)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
