from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


# Sample view for GET , POST requests
# if your url has /person/<id>/ , then, the id value will be injected into args
# so , the function def would be def get(self, request, id, format=None)
class TestView(APIView):
	def get(self, request, format=None):
		data  = {'string': 'hello'}
		return Response(data, status=status.HTTP_200_OK)

	def post(self, request, format=None):
		print self.request.data;
		return Response(self.request.data, status=status.HTTP_200_OK)
