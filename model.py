import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# Load the dataset
df = pd.read_csv('household_power_consumption.txt', sep=';',
                 parse_dates={'datetime': ['Date', 'Time']}, infer_datetime_format=True,
                 low_memory=False, na_values=['nan', '?'])

# Handle missing values
df.fillna(method='ffill', inplace=True)

# Extract and convert features
df['global_active_power'] = df['Global_active_power'].astype(float)
df['voltage'] = df['Voltage'].astype(float)
df['global_intensity'] = df['Global_intensity'].astype(float)

# Drop rows with NaN values
df.dropna(subset=['global_active_power', 'voltage', 'global_intensity'], inplace=True)

# Create polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X = df[['voltage', 'global_intensity']]
X_poly = poly.fit_transform(X)
y = df['global_active_power']

# Train the polynomial regression model
model = LinearRegression()
model.fit(X_poly, y)


def predict_power(avg_voltage, avg_intensity):
    future_data = np.array([[avg_voltage, avg_intensity]])
    future_data_poly = poly.transform(future_data)
    predicted_power = model.predict(future_data_poly)
    return predicted_power[0]


def get_future_data(date, interval, avg_voltage, avg_intensity):
    start_date = datetime.strptime(date, '%Y-%m-%d')

    if interval == 'next_day':
        days = 1
    elif interval == 'next_week':
        days = 7
    elif interval == 'next_month':
        days = 30
    else:
        raise ValueError("Invalid interval. Must be 'next_day', 'next_week', or 'next_month'.")

    dates = [start_date + timedelta(days=i) for i in range(days)]
    predictions = []

    for single_date in dates:
        base_prediction = predict_power(avg_voltage, avg_intensity)
        variability = np.random.normal(loc=0, scale=0.1)  # Adding a normal distribution noise
        predicted_power = base_prediction + variability
        predictions.append({
            'date': single_date.strftime('%Y-%m-%d'),
            'predicted_power': predicted_power
        })

    return predictions
