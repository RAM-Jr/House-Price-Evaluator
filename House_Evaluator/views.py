from django.http import HttpResponse
from django.shortcuts import render,redirect

def home(request):
    return redirect('evaluations:evaluation_form')
