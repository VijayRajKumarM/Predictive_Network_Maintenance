import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from autogluon.tabular import TabularPredictor
# Initialize Flask app and configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app, supports_credentials=True)

# Load your trained model (ensure the path is correct)
predictor = TabularPredictor.load("models",require_py_version_match = False)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an empty file
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Read the file into a DataFrame
    try:
        data = pd.read_csv(file)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    # Drop the 'TIMESTAMP' column if it exists
    if 'TIMESTAMP' in data.columns:
        data = data.drop(columns=['TIMESTAMP'])
    
    # Predict using the first row of the CSV file
    try:
        score = predictor.predict(data.iloc[0:1])
        print("score=",score)
        print(type(score)) 
        # Convert the prediction to a list if it's not already
        predicted_value = score.tolist() if not isinstance(score, list) else score
        return jsonify({"predicted_value": predicted_value}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
