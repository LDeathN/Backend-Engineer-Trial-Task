from django.db import models


class BacktestResult(models.Model):
    symbol = models.CharField(max_length=10)  # e.g., 'AAPL', 'GOOGL'
    total_return = models.FloatField()  # Total return percentage
    max_drawdown = models.FloatField()  # Maximum drawdown percentage
    number_of_trades = models.IntegerField()  # Number of trades executed
    created_at = models.DateTimeField(auto_now_add=True)  # Date when the backtest was performed

    def __str__(self):
        return f"{self.symbol} Backtest Result"


class StockPrediction(models.Model):
    symbol = models.CharField(max_length=10)  # e.g., 'AAPL', 'GOOGL'
    date = models.DateField()  # Date of the prediction
    actual_price = models.FloatField()  # Actual price on that date
    predicted_price = models.FloatField()  # Predicted price on that date

    class Meta:
        unique_together = ('symbol', 'date')  # Ensures no duplicate predictions for the same date

    def __str__(self):
        return f"{self.symbol} Prediction on {self.date}"
