import pandas as pd
import numpy as np
df=pd.read_csv("main.csv")
df.drop(columns=['Unnamed: 0','User_ID'],inplace=True)
df["Gender"] = df["Gender"].map({"male": 1, "female": 0})
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
X_train,X_test,y_train,y_test=train_test_split(df.drop(columns=['calories']),df['calories'],test_size=0.3,random_state=7)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
model = Sequential()
model.add(Dense(64, input_dim=X_train_scaled.shape[1], activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation="linear"))
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train_scaled, y_train, epochs=100, batch_size=32, verbose=0,validation_split=0.2)
mse = model.evaluate(X_test_scaled, y_test)
print("Mean Squared Error:", mse)
y_pred = model.predict(X_test_scaled)
joblib.dump(scaler, 'scaler.joblib')
x_test12 = [["male", 68, 190.0, 94.0, 29.0, 105.0, 40.8]]
x_test12[0][0] = 1 if x_test12[0][0] == "male" else 0
x_test12_scaled = scaler.transform(x_test12)
test_12 = model.predict(x_test12_scaled)
print("Prediction for x_test12:", test_12)
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_pred)
print("R-squared Score:", r2)
model.save('mini_model.keras')
