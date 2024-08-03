from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
from sklearn.preprocessing import StandardScaler
import joblib
from tensorflow.keras.models import load_model
import requests

app = Flask(__name__)
CORS(app) 

model = load_model('mini_model.keras')

# Define a function to preprocess input data
def preprocess_data(data):
    # Map gender values to 0 and 1
    data["Gender"] = data["Gender"].map({"male": 1, "female": 0})
    return data

# Node.js server URL
NODE_SERVER_URL = 'http://localhost:3001'

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Extract input data from the JSON request
            input_data = request.json
            gender = input_data['gender']
            age = float(input_data['age'])
            height = float(input_data['height'])
            weight = float(input_data['weight'])
            duration = float(input_data['duration'])
            heart_rate = float(input_data['heartbeat'])
            body_temp = float(input_data['bodytemp'])

            # Preprocess the input data
            input_df = pd.DataFrame([[gender, age, height, weight, duration, heart_rate, body_temp]],
                                    columns=['Gender', 'Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp'])
            input_df = preprocess_data(input_df)

            # Load the scaler used during training
            scaler = joblib.load('scaler.joblib')

            # Scale the input data
            scaled_input = scaler.transform(input_df)

            # Make prediction
            prediction = model.predict(scaled_input)

            # Convert prediction to a Python float
            predicted_calories = float(prediction[0][0])
            print(predicted_calories)

            # Send predicted calories to the Node.js server
            node_response = requests.post(NODE_SERVER_URL + "/calories", json={"predicted_calories": predicted_calories})
            if node_response.status_code == 200:
                print("Calories prediction sent to Node.js server successfully")
            else:
                print("Failed to send calories prediction to Node.js server")

            # Return predicted calories as JSON response
            return jsonify({'predicted_calories': predicted_calories})

        except Exception as e:
            # Log the error
            print(f"Error occurred: {str(e)}")
            # Return an error response
            return jsonify({'error': 'An error occurred while processing the request'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
