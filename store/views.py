from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view()
def product_list(request):
	return Response('ok');

@api_view()
def product_detail(request):
	return Response('ok');

