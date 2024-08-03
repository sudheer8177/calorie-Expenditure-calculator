import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model
import joblib  # Importing joblib module

# Define the input data
input_data = np.array([[0, 26, 146.0, 51.0, 16.0, 90.0, 40.2]])

# Load the scaler from the file
scaler = joblib.load('scaler.joblib')

# Preprocess the input data using the loaded scaler
input_data_scaled = scaler.transform(input_data)

# Load the model with the correct filename
model = load_model('mini_model.keras')  # Corrected the filename

# Print model summary to ensure correct architecture
print(model.summary())

# Predict using the loaded model
calories_prediction = model.predict(input_data_scaled)

# Print the predicted calorie value
print("Predicted Calorie Value:", calories_prediction[0][0])
