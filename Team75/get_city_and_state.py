from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import *
from django import forms
from django.core.mail import send_mail
from urllib.request import urlopen
import time
import json
@csrf_exempt
def query(request):    
    url = 'https://maps.google.com/maps/api/geocode/xml?key=AIzaSyC4XatT9vxskvkPJPaH8VYreC0Cq2eXD34&latlng=-37.9330062866211,145.034378051758&language=zh-CN&sensor=false'
    html =urlopen(url)     
    rst = html.read().decode("ISO-8859-1") 
    index = rst.find('street_address')
    index2 = rst.find('political',index)
    loc2 = rst.find('</short_name>',index2)
    loc1 = rst.find('<short_name>',index2)
    city = rst[loc1+12:loc2]
    loc3 = rst.find('<short_name>',loc1+1)
    loc4 = rst.find('</short_name>',loc2+1)
    state = rst[loc3+12:loc4]
    print(city,state)
    return HttpResponse('show.html')