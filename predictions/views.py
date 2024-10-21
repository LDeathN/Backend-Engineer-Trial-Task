from django.shortcuts import render

import joblib
from stock_data.models import StockData
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .models import StockPrediction
from rest_framework.views import APIView
from rest_framework.response import Response


def save_predictions(symbol, predictions):
    today = datetime.today()
    for i, predicted_price in enumerate(predictions):
        prediction = StockPrediction(
            symbol=symbol,
            date=today + timedelta(days=i),
            predicted_price=predicted_price
        )
        prediction.save()


def load_model():
    model = joblib.load('predictions/linear_regression_model.pkl')
    return model


def get_stock_data(symbol):
    stock_data = StockData.objects.filter(symbol=symbol).order_by('date')
    data = pd.DataFrame(list(stock_data.values('open_price', 'high_price', 'low_price', 'volume')))
    return data


def prepare_prediction_data(stock_data):
    X = stock_data[['open_price', 'high_price', 'low_price', 'volume']].values
    return X


def predict_future_prices(model, stock_data):
    predictions = []
    X = prepare_prediction_data(stock_data)
    for _ in range(30):  # Predict next 30 days
        predicted_price = model.predict([X[-1]])[0]
        predictions.append(predicted_price)

        # Optionally use the predicted price as input for the next day
        new_data = [predicted_price]  # Extend with open, high, low, volume if needed
        X = np.append(X, [new_data], axis=0)

    return predictions


class StockPredictionView(APIView):
    def post(self, request):
        symbol = request.data.get('symbol')

        # Fetch historical data
        stock_data = get_stock_data(symbol)

        # Load pre-trained model
        model = load_model()

        # Generate predictions
        predictions = predict_future_prices(model, stock_data)

        # Save predictions to the database
        save_predictions(symbol, predictions)

        return Response({'symbol': symbol, 'predictions': predictions})

