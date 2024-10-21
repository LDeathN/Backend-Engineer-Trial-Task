from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_backtesting_results, get_prediction_data
from django.http import FileResponse
from .utils import generate_pdf_report


class ReportView(APIView):
    def get(self, request):
        symbol = request.query_params.get('symbol')
        backtest_results = get_backtesting_results(symbol)
        predictions = get_prediction_data(symbol)

        report = {
            'symbol': symbol,
            'backtest_results': {
                'total_return': backtest_results.total_return,
                'max_drawdown': backtest_results.max_drawdown,
                'number_of_trades': backtest_results.number_of_trades
            },
            'predictions': [
                {
                    'date': prediction.date,
                    'actual_price': prediction.actual_price,
                    'predicted_price': prediction.predicted_price
                }
                for prediction in predictions
            ]
        }
        return Response(report)


class DownloadReportView(APIView):
    def get(self, request):
        symbol = request.query_params.get('symbol')
        backtest_results = get_backtesting_results(symbol)
        predictions = get_prediction_data(symbol)
        pdf_file = generate_pdf_report(symbol, backtest_results, predictions)
        response = FileResponse(open(pdf_file, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{symbol}_report.pdf"'
        return response

