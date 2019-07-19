from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('show', views.show ,name = 'Show'),
    path('test', views.query ,name = 'Test'),
    path('state_outcome', views.state_outcome ,name = 'State_outcome'),
    path('city_outcome', views.city_outcome ,name = 'City_outcome'),
    path('city_sentiment', views.city_sentiment ,name = 'City_sentiment'),
]