# -*- coding: utf-8 -*-
"""sleep-duration-detector.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1G4YtA3usJQPhEvswkN00_zrKBfzxMaHP
"""

pip install pandas numpy scikit-learn tensorflow keras

from google.colab import files
uploaded = files.upload()

import pandas as pd

# Load the dataset
df = pd.read_csv('Sleep_health_and_lifestyle_dataset.csv')

# Check the first few rows
df.head()

# Check for missing values
df.isnull().sum()

# Check data types
df.dtypes

# Summary statistics
df.describe()

df = df.dropna()

from sklearn.preprocessing import StandardScaler

# Features that need normalization
num_features = ['Age', 'Physical Activity Level', 'Stress Level', 'Heart Rate', 'Daily Steps']

scaler = StandardScaler()
df[num_features] = scaler.fit_transform(df[num_features])

# One-hot encode categorical features
df = pd.get_dummies(df, columns=['Gender', 'Occupation', 'BMI Category', 'Blood Pressure', 'Sleep Disorder'])

X = df.drop(columns=['Sleep Duration', 'Person ID'])  # Input features
y = df['Sleep Duration']  # Target variable

from sklearn.model_selection import train_test_split

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Create and train the model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predictions
predictions = rf_model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, predictions)
print("Random Forest MAE:", mae)

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Create the model
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1)  # Output layer for regression
])

# Compile the model
model.compile(optimizer='adam', loss='mean_absolute_error')

# Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=16, validation_split=0.2)

# Evaluate the model
loss = model.evaluate(X_test, y_test)
print("Keras Model MAE:", loss)

from sklearn.metrics import mean_absolute_error

# Evaluate the model
mae = mean_absolute_error(y_test, predictions)
print("Mean Absolute Error:", mae)

import matplotlib.pyplot as plt

plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss (MAE)')
plt.legend()
plt.show()

from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, None]
}

grid_search = GridSearchCV(RandomForestRegressor(), param_grid, cv=3, scoring='neg_mean_absolute_error')
grid_search.fit(X_train, y_train)

print(grid_search.best_params_)
print(grid_search.best_score_)

!pip install keras-tuner -q

from tensorflow.keras import layers
from keras_tuner.tuners import RandomSearch


def build_model(hp):
    model = Sequential()
    model.add(Dense(hp.Int('units', min_value=32, max_value=128, step=32), activation='relu', input_shape=(X_train.shape[1],)))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_absolute_error')
    return model

tuner = RandomSearch(build_model, objective='val_loss', max_trials=5, executions_per_trial=3, directory='my_dir')
tuner.search(X_train, y_train, epochs=50, validation_split=0.2)

# Save the trained model
model.save('sleep_prediction_model.h5')

import matplotlib.pyplot as plt

# Plot actual vs predicted values
plt.scatter(y_test, predictions, color='blue', label='Predicted vs Actual')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
plt.xlabel('Actual Sleep Duration')
plt.ylabel('Predicted Sleep Duration')
plt.title('Actual vs Predicted Sleep Duration')
plt.show()

from google.colab import files
model.save('sleep_prediction_model.h5')
files.download('sleep_prediction_model.h5')