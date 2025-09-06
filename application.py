from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
import time

from src.pipeline.predict_pipeline import CustomData, PredictPipleline

application = Flask(__name__)
app = application

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Prediction route
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        start_time = time.time()

        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score'))
        )

        pred_df = data.get_data_as_data_frame()
        predict_pipeline = PredictPipleline()
        prediction = np.round(predict_pipeline.predict(pred_df), 4)

        end_time = time.time()
        inference_time = round(end_time - start_time, 4)

        # Return JSON with prediction and inference time
        return jsonify({
            "prediction": float(prediction[0]),
            "inference_time": inference_time
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
