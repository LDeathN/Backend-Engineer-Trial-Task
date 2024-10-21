import requests
import logging
from django.core.management.base import BaseCommand
from financial_data.stock_data.models import StockData
from datetime import datetime

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fetch daily stock data from Alpha Vantage"

    def handle(self, *args, **kwargs):
        api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'
        symbol = 'AAPL'
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}'

        response = requests.get(url)
        if response.status_code != 200:
            logger.error("Failed to fetch data: HTTP %s", response.status_code)
            self.stdout.write(self.style.ERROR("Failed to fetch data"))
            return

        data = response.json().get('Time Series (Daily)', {})
        if not data:
            logger.error("No data found in response for symbol: %s", symbol)
            self.stdout.write(self.style.ERROR("No data found in response"))
            return

        for date_str, daily_data in data.items():
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            open_price = float(daily_data['1. open'])
            close_price = float(daily_data['4. close'])
            high_price = float(daily_data['2. high'])
            low_price = float(daily_data['3. low'])
            volume = int(daily_data['6. volume'])

            StockData.objects.update_or_create(
                symbol=symbol,
                date=date,
                defaults={
                    'open_price': open_price,
                    'close_price': close_price,
                    'high_price': high_price,
                    'low_price': low_price,
                    'volume': volume,
                }
            )

        logger.info("Successfully fetched data for %s", symbol)
        self.stdout.write(self.style.SUCCESS(f"Successfully fetched data for {symbol}"))

