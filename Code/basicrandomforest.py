# -*- coding: utf-8 -*-
"""BasicRandomForest.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aAKM95-9nrqSX3HFIGMWJqo3w60PmlQB

Import Libraries
"""

# basic imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# specific imports
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

"""Import Dataset"""

# Assign data to variable
dataset = pd.read_csv('combinedData.csv')

# Take a small look at the dataframe produced
print(dataset.head())

"""Preprocess Data (normalize it!)"""

# Convert the date strings into datetime objects
converted_dates = []

for date in dataset.columns:
  datetime_object = datetime.strptime(date, '%B %Y')
  converted_dates.append(datetime_object.timestamp())

dates_array = np.array(converted_dates)

"""Encode Catagorical data"""

# Initialize the encoder to work with
label_encoder = LabelEncoder()

print(dataset.iloc[0])

# Fit the data needed to the encoder for later use
label_encoder.fit(dataset.iloc[0])

dataset.iloc[1] = label_encoder.transform(dataset.iloc[0])

"""Split data into X and y sets"""

# define X and y variables
X = dates_array
y = dataset.iloc[0].values

# varify the split data
print(f"X dataset example: {X[0]}")
print(f"y dataset example: {y[0]}")

"""Break data into Training and Test sets"""

# Split into 4 specific variables
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = X_train.reshape(-1, 1)
X_test = X_test.reshape(-1, 1)

"""Instatiate the model"""

# plant the seeds to grow a forest
forest_model = RandomForestRegressor(n_estimators=50, random_state=0)

"""Train the model"""

# call your model and passin the training datasets
forest_model.fit(X_train, y_train)

"""Make the predictions you want it to output"""

# pass in X_test to predict a y value
y_predict = forest_model.predict(X_test)

print(y_predict)

"""Check the model"""

# pass in your y test data and check it against your y predicted data
mse = mean_squared_error(y_test, y_predict)

# share with the world!
print(f"mean Squared Error: {mse}")

"""Make a pretty graph!"""

# Plot the actual vs predicted values
plt.scatter(y_test, y_predict)
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.title('First Learning Graph')

# Adjust layout for better appearance
plt.tight_layout()

# Save the plot to a dynamic SVG file
plt.savefig('firstGraph.svg', format='svg', bbox_inches='tight')

plt.show()