from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BacktestingParamsSerializer
from .backtesting import perform_backtesting


class BacktestingView(APIView):
    def post(self, request):
        serializer = BacktestingParamsSerializer(data=request.data)
        if serializer.is_valid():
            results = perform_backtesting(serializer.validated_data)
            return Response(results)
        return Response(serializer.errors, status=400)
