import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense, LSTM


number_of_days_of_data = 365 # Number of days of data to use to predict the next day's stock price(high for long term investment, low for short term investment)
def download_stock_data(ticker):
    stock = yf.Ticker(ticker) # Get the stock data
    data = stock.history(period="2y")   # Get the historical prices for this ticker, can set start and end dates if needed to be precise
    return data

ticker = input("Enter the stock you want to find: ")

df = download_stock_data(ticker) # Download the stock data

if df.empty: # Check if the data is empty
    print("No data found for the specified date range.")
else:
    print(df)

    scaler = MinMaxScaler(feature_range=(0, 1)) # Scale the data to be between 0 and 1
    scaled_data = scaler.fit_transform(df["Close"].values.reshape(-1, 1)) # fit and trasnforms data

    x_train = [] # Create the training data
    y_train = [] # Create the targets
    for i in range(number_of_days_of_data, len(scaled_data)): 
        x_train.append(scaled_data[i - number_of_days_of_data:i, 0])
        y_train.append(scaled_data[i, 0])
    x_train, y_train = np.array(x_train), np.array(y_train) # Convert the data to a numpy array

    print("x_train shape before reshaping:", x_train.shape) # Print the data shape
    print("y_train shape:", y_train.shape)               # print the target shape

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1)) # Reshape the data

    model = Sequential() # Build the LSTM model
    model.add(LSTM(units=200, return_sequences=True, input_shape=(x_train.shape[1], 1))) # 200 is the number of neurons in the layer
    model.add(LSTM(units=200, return_sequences=False)) # 200 is the number of neurons in the layers
    model.add(Dense(units=100)) # 100 is the number of neurons in the layer
    model.add(Dense(units=4)) # 4 is the number of neurons in the layer

    model.compile(optimizer="adam", loss="mean_squared_error") # Compile the model
    model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2) # Train the model

# Get the last 60 days of stock price data and scale it
last_60_days = df["Close"][-number_of_days_of_data:].values.reshape(-1, 1)
last_60_days_scaled = scaler.transform(last_60_days)

# Reshape the input data to match the model's input shape
x_test = np.reshape(last_60_days_scaled, (1, last_60_days_scaled.shape[0], 1))

# Use the model to predict the next day's stock price
predicted_price = model.predict(x_test)
print(predicted_price)
# Rescale the predicted value back to the original price scale
predicted_price_unscaled = scaler.inverse_transform(predicted_price)

print(f"Predicted stock price for the next day: {predicted_price_unscaled[0][0]}")

# Decide whether to invest in the stock based on the predicted value
if predicted_price_unscaled[0][0] > df["Close"][-1]:
    print("The stock price is predicted to increase. Consider investing.")
else:
    print("The stock price is predicted to decrease. Consider not investing.")

