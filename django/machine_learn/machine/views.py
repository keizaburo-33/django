from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from machine.script import hello
# Create your views here.
import os


def top_view(request):
    return render(request, "top.html")
