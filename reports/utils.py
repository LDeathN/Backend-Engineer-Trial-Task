from .models import BacktestResult, StockPrediction
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def get_backtesting_results(symbol):
    results = BacktestResult.objects.filter(symbol=symbol).last()
    return results


def get_prediction_data(symbol):
    predictions = StockPrediction.objects.filter(symbol=symbol).order_by('date')
    return predictions


def plot_predictions(predictions, symbol):
    dates = [pred.date for pred in predictions]
    actual_prices = [pred.actual_price for pred in predictions]
    predicted_prices = [pred.predicted_price for pred in predictions]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, actual_prices, label='Actual Price', color='blue')
    plt.plot(dates, predicted_prices, label='Predicted Price', color='orange')
    plt.title(f'Actual vs Predicted Stock Prices for {symbol}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    plt.savefig('stock_price_comparison.png')
    plt.close()


def generate_pdf_report(symbol, backtest_results, predictions):
    pdf_file = f'{symbol}_report.pdf'
    c = canvas.Canvas(pdf_file, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, f"Performance Report for {symbol}")

    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Total Return: {backtest_results.total_return:.2f}%")
    c.drawString(100, 700, f"Max Drawdown: {backtest_results.max_drawdown:.2f}%")
    c.drawString(100, 680, f"Number of Trades: {backtest_results.number_of_trades}")
    c.drawImage('stock_price_comparison.png', 100, 450, width=400, height=200)
    c.setFont("Helvetica", 10)
    c.drawString(100, 100, "Generated using Django and ReportLab")
    c.save()
    return pdf_file
