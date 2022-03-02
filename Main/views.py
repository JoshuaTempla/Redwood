from django.core.files.base import ContentFile
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
#from .forms import *
from django.views.generic import View

# Create your views here.

def IndexView(request):
    return render(request, 'index.html', {})
