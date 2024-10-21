import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib


def train_model():
    # Load historical stock data from your database or CSV
    data = pd.read_csv('historical_stock_data.csv')  # Adjust this path as needed

    # Using close prices as target variable, add other features if necessary
    X = data[['open_price', 'high_price', 'low_price', 'volume']]
    y = data['close_price']

    # Split into training and test data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save the model to a file
    joblib.dump(model, 'predictions/linear_regression_model.pkl')

    return model

