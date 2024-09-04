import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import yfinance as yf
from sklearn.preprocessing import QuantileTransformer
import statistics
import pickle
import os
import math

def calculate_rsi(df, column='Close', period = 14):
    delta = df[column].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Prepare the data
aapl_df = yf.download('AAPL', start = '2019-01-01', end = '2023-02-03', progress = False)

# Add Moving Average and RSI features
aapl_df['MA20'] = aapl_df['Close'].rolling(window=20).mean()
aapl_df['RSI'] = calculate_rsi(aapl_df)

# Drop NaN values generated by rolling mean and RSI calculation
aapl_df = aapl_df.dropna()

# Create sequences
data_X = []
data_y = []

for j in range(len(aapl_df) - 60):
    features = np.column_stack([
        aapl_df['Close'].iloc[j : j + 60].values,
        aapl_df['MA20'].iloc[j : j + 60].values,
        aapl_df['RSI'].iloc[j : j + 60].values
    ])
    data_X.append(features)
    data_y.append(aapl_df['Close'].iloc[j + 60])

data_X = np.array(data_X)
data_y = np.array(data_y)

# Check the data shapes before splitting
print(f"Original data_X shape: {data_X.shape}")
print(f"Original data_y shape: {data_y.shape}")

# Define split index
train_size = 800  # Ensure this is less than the total number of samples
test_size = len(data_X) - train_size

# Split data
data_X_train = data_X[:train_size]
data_X_test = data_X[train_size:]
data_y_train = data_y[:train_size]
data_y_test = data_y[train_size:]

# Check the shapes after splitting for debugging
print(f"Training data_X shape: {data_X_train.shape}")
print(f"Testing data_X shape: {data_X_test.shape}")
print(f"Training data_y shape: {data_y_train.shape}")
print(f"Testing data_y shape: {data_y_test.shape}")

# Reshape for scaler
data_X_train_flattened = data_X_train.reshape(-1, 3)  # Three features: Close, MA20, RSI
data_X_test_flattened = data_X_test.reshape(-1, 3)

scaler = QuantileTransformer(output_distribution = 'normal')
scaler.fit(data_X_train_flattened)  # Fit only on training data

# Transform data
data_X_train_scaled = scaler.transform(data_X_train_flattened).reshape(data_X_train.shape)
data_X_test_scaled = scaler.transform(data_X_test_flattened).reshape(data_X_test.shape)

scaler_y = QuantileTransformer(output_distribution = 'normal')

data_y_train = data_y_train.reshape(-1, 1)
data_y_test = data_y_test.reshape(-1, 1)
scaler_y.fit(data_y_train)
data_y_train_scaled = scaler_y.transform(data_y_train)
data_y_test_scaled = scaler_y.transform(data_y_test)

# Pickle it to unscale the data later
if os.path.exists('neural_net_trader/scalers.pkl'):
    # Load existing data
    with open('neural_net_trader/scalers.pkl', 'rb') as f:
        scalers = pickle.load(f)
else:
    # If file doesn't exist, start with an empty dictionary
    scalers = {}


# Add or update the new scalers
scalers.update({'scaler_aapl': scaler, 'scaler_y_aapl': scaler_y})

# Save the updated dictionary back to the file
with open('scalers.pkl', 'wb') as f:
    pickle.dump(scalers, f)

# Build the model with two LSTM layers
model = Sequential()
model.add(LSTM(50, input_shape=(60, 3), return_sequences = True))  # Adjust input_shape to (60, 3)
model.add(LSTM(50, return_sequences = False)) # Second Layer
model.add(Dense(1))  # Output layer
model.compile(optimizer = 'adam', loss = 'mean_squared_error')

model.summary()
    
# Train the model
history = model.fit(
    data_X_train_scaled,
    data_y_train_scaled,
    epochs = 50,
    batch_size = 32,
)

# Save the model
model.save('lstm_aapl_deep.h5')

# Evaluate the model
loss = model.evaluate(data_X_test_scaled, data_y_test_scaled)
print(f'Test Loss: {loss}')

# Make predictions
predictions_scaled = model.predict(data_X_test_scaled)
predictions_unscaled = scaler_y.inverse_transform(predictions_scaled)
print(predictions_unscaled)

# Print actual vs predictions for debugging
for j in range(len(data_y_test)):
    print(f"Actual: {data_y_test[j][0]}, Predicted: {predictions_unscaled[j][0]}")

# Simulate trading
data_y_test_manip = []

for j in range(len(data_y_test)):
    data_y_test_manip.append(data_y_test[j][0])

# The price deviation required to cause an action (buy or sell)
tolerance = 1

money = 10000
num_shares = 0
    
# for j in range(len(data_y_test) - 1):
    # if predictions_unscaled[j + 1][0] - data_y_test[j][0] >= risk_tolerance and money >= 1 * data_y_test[j][0]:
        # money -= 1 * data_y_test[j][0]
        # num_shares += 1
    # elif predictions_unscaled[j + 1][0] - data_y_test[j][0] <= -risk_tolerance and num_shares >= 1:
        # money += 1 * data_y_test[j][0]
        # num_shares -= 1

for j in range(len(data_y_test) - 1):
    if predictions_unscaled[j + 1][0] - data_y_test[j][0] >= tolerance and money >= data_y_test[j][0]:
        money += num_shares * data_y_test[j][0]
        num_shares = math.floor(money / data_y_test[j][0])
        money -= num_shares * data_y_test[j][0]
    else:
        if predictions_unscaled[j + 1][0] - data_y_test[j][0] <= -tolerance:
            money += num_shares * data_y_test[j][0]
            num_shares = 0

# Performance Report
print("Stock: Apple")
print(f"Number of shares: {num_shares}")
print(f"Starting money: $10000")
print(f"Ending money: ${money + (num_shares * data_y_test[-1][0])}")
print(f"Days: {len(data_y_test)}")
print(f"Tolerance level: {tolerance}")   