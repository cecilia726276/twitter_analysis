from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse,JsonResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import *
from django import forms
from django.core.mail import send_mail
from urllib.request import urlopen
import time
import json
import couchdb
import requests
@csrf_exempt
def show(request):
    return render(request, 'show.html')
location_list = []
with open("VIC.txt") as dictionary:
    for word in dictionary:
        word = word[:-1]
        #print(word)
        location_list.append(word)
@csrf_exempt
def query(request):  
    #get exact city using google api
    lat = request.POST.get('lat','')
    lng = request.POST.get('lng','') 
    url = "https://maps.google.com/maps/api/geocode/xml?key=AIzaSyC4XatT9vxskvkPJPaH8VYreC0Cq2eXD34&latlng="+lat+","+lng+"&language=zh-CN&sensor=false"
    rst = str(requests.get(url).content)
    for substring in location_list:
        if substring in rst:
            break
    city = substring
    state = 'VIC'
    #print(city,state)
    server = couchdb.Server('http://admin:admin@45.113.233.208:5984/')
    # get sentiment analysis from exact city
    outcome_name = "au_outcome"
    outcome = server[outcome_name]
    k ='746c64122cdc6c1953ecfc13a8df8edd'
    ds = outcome[k]
    p =json.dumps(ds)
    q = json.loads(p)
    #get obesity
    db_name = "aurin"
    db = server[db_name]
    for item in db.view("aurin_vic_viewer/VIC_obesity_view"):#macth obesity data with exact city
        p1 = json.dumps(item)
        q1 = json.loads(p1)
        if q1.get('key') ==city:
            #print (q1.get('value'))
            #print ('get')
            break
    #get overweight        
    for item in db.view("aurin_vic_viewer/VIC_overweight_view"):#macth overweight data with exact city
        p2 = json.dumps(item)
        q2 = json.loads(p2)
        if q1.get('key') ==city:
            #print (q2.get('value'))
            #print ('get')
            break
    #package data
    context={'city':city,"state":state,"neu":q[city]['score']['neu'],"neg":q[city]['score']['neg'],"pos":q[city]['score']['pos'],"count":q[city]['count'],"obesity":q1.get('value'),"overweight":q2.get('value')}
    #print (context)
    return JsonResponse (context)#return to front end
@csrf_exempt
def state_outcome(request):#query the database and get all states outcomes
    server = couchdb.Server('http://admin:admin@45.113.233.208:5984/')#make connection
    # The final outcome of tweet analysis
    outcome_name = "au_outcome"
    outcome = server[outcome_name]
    i=0
    adict ={}
    state = ['NSW', 'ACT', 'VIC', 'QLD', 'SA','WA', 'TAS','NT']
    for _id in outcome:#get state data
        if i<8:
            data = outcome[_id]
            m = json.dumps(data)
            b =json.loads(m)
            adict[state[i]] = b[state[i]]
            i=i+1
        else:
            break
    #print(adict)
    return JsonResponse(adict) #return to front end
@csrf_exempt
def city_outcome(request):#query the database and get all cities outcomes
    server = couchdb.Server('http://admin:admin@45.113.233.208:5984/')#make connection
    db_name = "aurin"
    db = server[db_name]
    city_obesity={}
    city_overweight={}
    for item in db.view("aurin_vic_viewer/VIC_obesity_view"):#get obesity data
        p1 = json.dumps(item)
        q1 = json.loads(p1)
        city_obesity[q1.get('key')]= q1.get('value')
    for item in db.view("aurin_vic_viewer/VIC_overweight_view"):#get overweight data
        p2 = json.dumps(item)
        q2 = json.loads(p2)
        city_overweight[q2.get('key')]= q2.get('value')
    context ={"obesity":city_obesity,"overweight":city_overweight} #package
    #print (context)
    return JsonResponse(context) #return to front end
@csrf_exempt
def city_sentiment(request):#query the database and get all cities sentiments
    server = couchdb.Server('http://admin:admin@45.113.233.208:5984/')#make connection
    # The final outcome of tweet analysis
    outcome_name = "au_outcome"
    outcome = server[outcome_name]
    db_name = "aurin"
    db = server[db_name]
    i=0
    city_pos={}
    city_neu={}
    city_neg={}
    for _id in outcome:
        if i ==8:
            data = outcome[_id]
            m = json.dumps(data)
            b =json.loads(m)
            break
        else:
            i=i+1
    for item in db.view("aurin_vic_viewer/VIC_obesity_view"):#get obesity data
        p1 = json.dumps(item)
        q1 = json.loads(p1)
        try:
            city_pos[q1.get('key')]= b[q1.get('key')]['score']['pos']
            city_neu[q1.get('key')]= b[q1.get('key')]['score']['neu']
            city_neg[q1.get('key')]= b[q1.get('key')]['score']['neg']
        except Exception as e:
            continue
    context ={"pos":city_pos,"neu":city_neu,"neg":city_neg}
    print (context)
    return JsonResponse(context)

