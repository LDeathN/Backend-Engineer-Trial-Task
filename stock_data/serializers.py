from rest_framework import serializers


class BacktestingParamsSerializer(serializers.Serializer):
    initial_investment = serializers.DecimalField(max_digits=10, decimal_places=2)
    short_window = serializers.IntegerField()
    long_window = serializers.IntegerField()
    symbol = serializers.CharField(max_length=10)

