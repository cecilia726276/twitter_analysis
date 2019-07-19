## **This is web application file.**
### Activate the web server ###
>>type 'python.exe manage.py runserver' to activate the web server.

Use '127.0.0.1:8000/Map/show' to open web site
### Directory usage ###
* Team75
>> store setting files and main urls

* app_map
>> store functions in app_map/views.py

>> store urls in app_map/urls.py

>> store web templates in app_map/templates

>> store scripts and imags in app_map/static

#### functions in app_map/views.py ####
* show:
>> init the website

* query:
>> get exact city data when mouse click

* state_outcome:
>>query the database and get all states outcomes

* city_outcome
>>query the database and get all cities outcomes

* city_sentiment
>>query the database and get all cities sentiments

