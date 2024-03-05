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
from sklearn.model_selection import RandomizedSearchCV

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

"""Setup hyperparameters"""

# Define the parameter distribution
param_dist = {
    'n_estimators': [50, 100, 150, 200]
}

"""Instatiate the model"""

# plant the seeds to grow a forest
forest_model = RandomForestRegressor(random_state=0)

# Initiate the random search
random_search = RandomizedSearchCV(
    estimator = forest_model,  # use the model we created above
    param_distributions = param_dist,  # use the params we defined above
    n_iter = 10,  # Go over it 10 times
    cv = 5,  # Cross validation iterations
    scoring = 'neg_mean_squared_error',  # score output for performance
    random_state = 0
    )

"""Train the model"""

# Not tuned fit
forest_model.fit(X_train, y_train)

# call your model and pass in the training datasets
random_search.fit(X_train, y_train)  # Use the random_search now instead of forest object

"""Make the predictions you want it to output"""

# pass in X_test to predict a y value on forest model
y_predict = forest_model.predict(X_test)

print(f"Not Tuned: {y_predict}")

# Predict on the tuned model
tuned_pred = random_search.predict(X_test)

print(f"Tuned Predicition: {tuned_pred}")

"""Check the model"""

# pass in your y test data and check it against your y predicted data
mse = mean_squared_error(y_test, y_predict)
selected_params = random_search.best_params_

# share with the world!
print(f"Initial Mean Squared Error: {mse}")
print(f"Best Parameters to use: {selected_params}")

"""Re-Initialize Random Forest using the slected Params"""

# Instatiate another forest model with the selected parameters
final_forest = RandomForestRegressor(
    selected_params['n_estimators'],
    random_state=0
)

# Fit data to the new model
final_forest.fit(X_train, y_train)
final_pred = final_forest.predict(X_test)

final_mse = mean_squared_error(y_test, final_pred)

# Show hyper tuned MSE
print(f"Hyper Tuned Mean Squared Error: {final_mse}")

"""Make a pretty graph!"""

# Fit a linear regression line to the data
# For the non-tuned actual vs predicted values
coefficients_non_tuned = np.polyfit(y_test, y_predict, 1)

# For the hyperparameter-tuned actual vs predicted values
coefficients_tuned = np.polyfit(y_test, final_pred, 1)

# Generate the regression lines
line_non_tuned = np.polyval(coefficients_non_tuned, y_test)
line_tuned = np.polyval(coefficients_tuned, y_test)

# Plot the non-tuned actual vs predicted values
plt.scatter(y_test, y_predict)
plt.plot(
    y_test,
    line_non_tuned,
    color='red',
    label='Regression Line'
    )
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.title('First Learning Graph')

# Adjust layout for better appearance
plt.tight_layout()

# Save the plot to a dynamic SVG file
plt.savefig('firstGraph.svg', format='svg', bbox_inches='tight')

plt.show()


# plot hyperparamer tuned actual vs predicted
plt.scatter(y_test, final_pred)
plt.plot(
    y_test,
    line_tuned,
    color='red',
    label='Regression Line'
    )
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.title('Hyper Parameter Tuned Graph')

# Adjust layout
plt.tight_layout()

# Save and show
plt.savefig('TunedGraph.svg', format='svg', bbox_inches='tight')

plt.show()