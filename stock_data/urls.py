from django.urls import path
from .views import BacktestingView

urlpatterns = [
    path('api/backtest/', BacktestingView.as_view(), name='backtesting'),
]