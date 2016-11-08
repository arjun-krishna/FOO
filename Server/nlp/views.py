from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import functions
from scraper.googlescraper import *
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


class NlpProgrammingView(APIView):
	def post(self, request, format=None):
		string = self.request.data
		print string
		return Response(self.request.data, status = status.HTTP_200_OK)

class NlpChatView(APIView):
	def post(self, request, format=None):
		string = str(self.request.data)
		print string
		return Response(self.request.data, status = status.HTTP_200_OK)

class NlpScrapeView(APIView):
	def post(self, request, format=None):
		string = self.request.data['string']
		print string
		search_string = functions.get_search_string(string)
		final_obj = googlescrape(search_string)
		# Function call in nlp functions
		return Response(final_obj, status = status.HTTP_200_OK)