import requests
import json
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
import datetime

from .models import User, WeatherRating
from .user_verification import checkUser, getUser, registerNewUser
from .utils import main, get_weather, generate_dummy_data1, generate_dummy_data2, KtoF

# Create your views here.
def index(request):
    # check if the current site visitor is already registered 
    # in our db as a user; if not, create a 
    # new user profile for them.
    if not request.COOKIES.get("uuid"):
        # use default temp/weather thresholds for
        # determining weather quality
        data_full = get_weather("Austin", return_descriptor=True)  # default city
        data = {'weather':data_full['descriptor'], 'temp':KtoF(data_full['feels_like'])}
        response = render(request, "index.html", {'data':data, 'is_quote':False})
        
        curr_user = registerNewUser(response)
        # initialize a little bit of data for the new user
        generate_dummy_data1(curr_user.uuid)
        return response
    else:
        # get the current weather or a "weather sucks, here is alternate thing" response to display onscreen
        data_full = main(int(request.COOKIES.get("uuid")), return_descriptor=True)
        if isinstance(data_full, dict):
            # we got an actual data thing instead of a quote
            data = {'weather':data_full['descriptor'], 'temp':KtoF(data_full['feels_like'])}
            response = render(request, "index.html", {'data':data, 'is_quote':False})
        else:
            # we just got a quote
            data = {'quote':data_full}  # data_full is actually a quote
            response = render(request, "index.html", {'data':data, 'is_quote':True})
        curr_user = getUser(request)
        return response
    
#    response = render(request, "index.html")
#    curr_user = checkUser(request, response)
#    print("current user is: {}".format(curr_user.uuid))
##    return HttpResponse('<pre>' + r.text + '</pre>')
#    return response

@api_view(['PUT'])
def register_weather_rating(request, pk=0):
    """ After the user rates the current weather, make a record of how they felt about the weather (in our database), so we can keep track of their preferences over time. """
    
    # get weather data for current user
    curr_user = getUser(request)
    curr_weather = get_weather(curr_user.city)
    today = int(datetime.datetime.today().timestamp())
    rating_val = int(pk) - 1 # rescale from [0, 2] scale to [-1, 1] scale
    
    # put this into the database, along with the user's rating
    weather_rating = WeatherRating.objects.create(
        uuid=curr_user.uuid,
        dt=today,
        temp=curr_weather['temp'],
        feels_like=curr_weather['feels_like'],
        humidity=curr_weather['humidity'],
        wind_speed=curr_weather['wind_speed'],
        clouds=curr_weather['clouds'],
        rain=curr_weather['rain'],
        snow=curr_weather['snow'],
        rating=rating_val,
    )
    
    weather_rating.save()
    
    
    data_full = main(int(request.COOKIES.get("uuid")), return_descriptor=True)
    if isinstance(data_full, dict):
        # we got an actual data thing instead of a quote
        data = {'weather':data['descriptor'], 'temp':KtoF(data['feels_like'])}
        response = render(request, "index.html", {'data':data, 'is_quote':False})
    else:
        # we just got a quote
        data = {'quote':data_full}  # data_full is actually a quote
        response = render(request, "index.html", {'data':data, 'is_quote':True})
    return response
    
    
    
    
    
    

def whoami(request):
    curr_user = getUser(request)
    return render(request, "whoami.html", {"user": curr_user})

def db(request):

#    user = User(uuid=0)
#    user.save()

    weathers = WeatherRating.objects.all()
     
    return render(request, "db.html", {"greetings": weathers})
#
#def addTemp(request):
#    # add the current temperature to the current user's db list thing!
#    

def options(request):
    return render(request, "options.html")

@api_view(['PUT'])
def set_user_profile(request, pk=None):
    """ Populate the current user's preference history with one of two possible user profiles:
        - cold-lover
        - heat-lover
    """
    
    curr_user = getUser(request)
    if pk == "cold":
        generate_dummy_data2(curr_user.uuid)
    elif pk == "heat":
        generate_dummy_data1(curr_user.uuid)
        
    data_full = main(int(request.COOKIES.get("uuid")), return_descriptor=True)
    if isinstance(data_full, dict):
        # we got an actual data thing instead of a quote
        data = {'weather':data_full['descriptor'], 'temp':KtoF(data_full['feels_like'])}
        response = render(request, "index.html", {'data':data, 'is_quote':False})
    else:
        # we just got a quote
        data = {'quote':data_full}  # data_full is actually a quote
        response = render(request, "index.html", {'data':data, 'is_quote':True})
    return response
    
        
    
