import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from sklearn.metrics import r2_score

# Load the dataset
df = pd.read_csv("main.csv")
df.drop(columns=['Unnamed: 0', 'User_ID'], inplace=True)
df["Gender"] = df["Gender"].map({"male": 1, "female": 0})

# Split data into features and target
X = df.drop(columns=['calories'])
y = df['calories']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=7)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define and train the model
model = Sequential([
    Dense(64, input_dim=X_train_scaled.shape[1], activation='relu'),
    Dense(32, activation='relu'),
    Dense(1, activation='linear')
])
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train_scaled, y_train, epochs=100, batch_size=32, verbose=0, validation_split=0.2)

# Evaluate the model on test set
mse = model.evaluate(X_test_scaled, y_test)
print("Mean Squared Error:", mse)

# Save the model
# Save the model in native Keras format
model.save('mini_model1.keras')

# Load the model
loaded_model = load_model('mini_model.keras')


# Predict using the loaded model
y_pred = loaded_model.predict(X_test_scaled)

# Evaluate the predictions
r2 = r2_score(y_test, y_pred)
print("R-squared Score:", r2)
