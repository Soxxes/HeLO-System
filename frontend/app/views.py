from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<H2>Welcome!</H2>")

# Create your views here.
