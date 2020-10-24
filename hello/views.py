import requests
import json
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view

from .models import User, WeatherRating
from .user_verification import checkUser, getUser, registerNewUser
from .weather import get_weather

# Create your views here.
def index(request):
    # check if the current site visitor is already registered 
    # in our db as a user; if not, create a 
    # new user profile for them.
    if not request.COOKIES.get("uuid"):
        # use default temp/weather thresholds for
        # determining weather quality
        response = render(request, "index.html", {"weather": "Cloudy", "temp":68})
        
        curr_user = registerNewUser(response)
        return response
    else:
        # get the current weather or a "weather sucks, here is alternate thing" response to display onscreen
        response = render(request, "index.html", {"weather": "Cloudy", "temp":66})
        return response
    
#    response = render(request, "index.html")
#    curr_user = checkUser(request, response)
#    print("current user is: {}".format(curr_user.uuid))
##    return HttpResponse('<pre>' + r.text + '</pre>')
#    return response

@api_view(['PUT'])
def register_weather_rating(request, rate_val):
    """ After the user rates the current weather, make a record of how they felt about the weather (in our database), so we can keep track of their preferences over time. """
    
    # get weather data for current user
    curr_user = getUser(request)
    curr_weather = get_weather(curr_user.city)
    
    # put this into the database, along with the user's rating
    weather_rating = WeatherRating.objects.create(
        uuid=curr_user.uuid,
        dt=curr_weather.dt,
        temp=curr_weather.temp,
        feels_like=curr_weather.feels_like,
        humidity=curr_weather.humidity,
        wind_speed=curr_weather.wind_speed,
        clouds=curr_weather.clouds,
        rain=curr_weather.rain,
        snow=curr_weather.snow,
        rating=int(rate_val),
    )
    
    weather_rating.save()
    
    
    
    
    

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
    
