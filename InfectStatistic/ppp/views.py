from django.shortcuts import render
from ppp import models
# Create your views here.
from django.shortcuts import HttpResponse

def index(request):
   # return HttpResponse("hello world!")
   data_list=models.data.objects.all()
   return render(request,"index.html",{"data":data_list})