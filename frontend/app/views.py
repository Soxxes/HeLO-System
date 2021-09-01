from django.shortcuts import render
from django.http import HttpResponse
from . forms import InputForm

# def index(request):
#     return HttpResponse("<H2>Welcome!</H2>")

def index(request):
    form = InputForm()
    context = {
        "myinputform": form
    }
    return render(request, "app/index.html", context)

# Create your views here.
