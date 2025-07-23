from datetime import timedelta
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error   
import matplotlib.pyplot as plt

stock = 'AAPL'
data = yf.download(stock, start='2020-01-01', end='2024-05-15')

data['Prev Close'] = data['Close'].shift(1)
data['High-Low'] = data['High'] - data['Low']
data['Open-Close'] = data['Open'] - data['Close']
data['Volume'] = data['Volume']
data['MA10'] = data['Close'].rolling(window=10).mean()
data['MA50'] = data['Close'].rolling(window=50).mean()
data = data.dropna()

# Prepare features and target variable
X = ['Prev Close', 'High-Low', 'Open-Close', 'Volume', 'MA10', 'MA50']
Y = ['Close']

# Split the data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(data[X], data[Y], test_size=0.2, random_state=121123)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=123)
model.fit(X_train, Y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(Y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Plot the predictions against actual values
plt.figure(figsize=(14, 7))
plt.scatter(Y_test.index, Y_test, label='Actual Prices', color='blue')
plt.scatter(Y_test.index, y_pred, label='Predicted Prices', color='red')
plt.legend()
plt.show()

######## PRICE ON 5/16
#Get the last row of data for prediction
last_date = data.index[-1]
future_dates = [last_date + timedelta(days=i) for i in range(1, 6)]
future_data = pd.DataFrame(index=future_dates, columns=X)

# Fill future_data with the last known values to initialize future predictions
last_row = data.iloc[-1]
ticker = stock  # 'AAPL'
for date in future_dates:
    future_data.loc[date, 'Prev Close'] = float(last_row['Close'].squeeze())
    future_data.loc[date, 'High-Low'] = float(last_row['High'].squeeze()) - float(last_row['Low'].squeeze())
    future_data.loc[date, 'Open-Close'] = float(last_row['Open'].squeeze()) - float(last_row['Close'].squeeze())
    future_data.loc[date, 'Volume'] = float(last_row['Volume'].squeeze())
    future_data.loc[date, 'MA10'] = float(data['Close'].rolling(window=10).mean().iloc[-1])
    future_data.loc[date, 'MA50'] = float(data['Close'].rolling(window=50).mean().iloc[-1])
future_predictions = model.predict(future_data)
print("Future predicted prices:")
for date, price in zip(future_dates, future_predictions):
    print(f"{date.date()}: {price}")