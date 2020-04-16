from django.http import HttpResponse,QueryDict
from django.shortcuts import render
from django.http import HttpResponseRedirect


def homepage(request):
    return render(request,"homepage.html",{})