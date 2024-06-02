import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
# Step 2: Load the Dataset (Here we create a synthetic time series)
np.random.seed(42)
time = np.arange(100)
data = np.sin(time / 3) + np.random.normal(size=time.shape) * 0.5  # Example time series data

# Convert to a pandas DataFrame
df = pd.DataFrame(data, columns=['value'])

# Step 3: Split the Dataset into Training and Testing Sets
train_size = int(len(df) * 0.8)
train, test = df[:train_size], df[train_size:]

# Step 4: Define the Moving Average Model
def moving_average(series, window_size):
    return series.rolling(window=window_size).mean()

# Step 5: Define a Custom Estimator for GridSearchCV
class MovingAverageModel(BaseEstimator, RegressorMixin):
    def __init__(self, window_size=5):
        self.window_size = window_size

    def fit(self, X, y=None):
        self.history = list(X['value'])
        return self

    def predict(self, X):
        predictions = []
        history = self.history[:]
        for i in range(len(X)):
            yhat = np.mean(history[-self.window_size:])
            predictions.append(yhat)
            history.append(X['value'].iloc[i])
        return np.array(predictions)

# Prepare the training data for GridSearchCV
X_train = train[['value']]
y_train = train['value']

# Step 6: Use GridSearchCV to Find the Best Window Size
param_grid = {'window_size': np.arange(2, 15)}
tscv = TimeSeriesSplit(n_splits=5)
grid_search = GridSearchCV(MovingAverageModel(), param_grid, cv=tscv, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

print(f"Best window size: {grid_search.best_params_['window_size']}")
print(f"Best score (neg_mean_squared_error): {grid_search.best_score_}")

# Step 7: Evaluate the Best Model
best_window_size = grid_search.best_params_['window_size']
best_model = MovingAverageModel(window_size=best_window_size)
best_model.fit(X_train)
predictions = best_model.predict(test[['value']])

mse = mean_squared_error(test['value'], predictions)
print(f'Mean Squared Error: {mse:.2f}')

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(train['value'], label='Train')
plt.plot(test['value'].reset_index(drop=True), label='Test')
plt.plot(pd.Series(predictions, index=test.index), label='Predictions')
plt.title('Moving Average Model Predictions with Optimal Window Size')
plt.legend()
plt.show()
