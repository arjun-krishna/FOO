from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import functions
from scraper.googlescraper_mod import *
from scraper.cppscraper import *
from chat.chat import *
from wit import Wit
import subprocess
# Create your views here.
chat_context = {}
client = Wit(access_token="UBTCYTFGDP3K3DJIGRV462NLNG2MM4I7", actions=actions)
# client.interactive()
client.logger.setLevel(logging.WARNING)

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


class NlpCodingMateView(APIView):
	def post(self, request, format=None):
		string = str(self.request.data['string'])
		print string
		flag = cppscrape(string)
		if flag is True:
			data  = {'string': "Here is an example from cppreference site. :)"}
		else :
			data = {'string' : "Sorry, Couldn't find any example :("}
		return Response(data, status = status.HTTP_200_OK)

class NlpChatView(APIView):
	def post(self, request, format=None):
		string = str(self.request.data['string'])
		print string, "gold"
		f = open("file.txt","w")
		f.write(string)
		f.close()
		proc = subprocess.Popen("python chat/chat.py", stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()
		print "shit"
		print out
		resp = {"string":out}
		# chat_context = chat_bot(client, 'my-user-session-42', string, chat_context)

		return Response(resp, status = status.HTTP_200_OK)

class NlpScrapeView(APIView):
	def post(self, request, format=None):
		string = self.request.data['string']
		print string
		# search_string = functions.get_search_string(string)
		final_obj = googlescrape(string)
		# print final_obj
		if not final_obj :
			final_obj = {"error" :"Sorry. Can't find any suggestions"}

		# Function call in nlp functions

		return Response(final_obj, status = status.HTTP_200_OK)
