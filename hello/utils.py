#imports 

import requests, json
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import datetime
import matplotlib.pyplot as plt

from .models import WeatherRating, User
from .user_verification import getUser

def get_weather(city_name, return_descriptor=False):
    """
    Takes a city name, and returns a dictionary of weather and location data. 
    """
    # Python program to find current  
    # weather details of any city 
    # using openweathermap api 

    # Enter your API key here 
    api_key = "9291be5e6daedb7e3a4a03f8857a8d5f"

    # base_url variable to store url 
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # complete_url variable to store 
    # complete url address 
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name 

    # get method of requests module 
    # return response object 
    response = requests.get(complete_url) 

    # json method of response object  
    # convert json format data into 
    # python format data 
    x = response.json() 
    
    # Now x contains list of nested dictionaries 
    # Check the value of "cod" key is equal to 
    # "404", means city is found otherwise, 
    # city is not found 
    if x["cod"] != "404": 
        output_dict = {}
        output_dict['temp'] = x['main']['temp']
        output_dict['feels_like'] = x['main']['feels_like']
        output_dict['humidity'] = x['main']['humidity']
        output_dict['clouds'] = x['clouds']['all']
        output_dict['wind_speed'] = x['wind']['speed']
        if 'rain' not in x.keys():
            output_dict['rain'] = 0
        else:
            output_dict['rain'] = x['rain']['1h']
        if 'snow' not in x.keys():
            output_dict['snow'] = 0
        else:
            output_dict['snow'] = x['snow']['1h']
            
        if return_descriptor:
            output_dict['descriptor'] = x['weather'][0]['main']
            output_dict['subdescriptor'] = x['weather'][0]['description']
        return output_dict 
    else: 
        print(" City Not Found ") 
        return None

def assess_weather(weather_dict, user_preferences = None):
    """
    Takes as input a dictionary with the weather parameters of interest:
        - temp
        - feels_like
        - humidity
        - clouds 
        - wind_speed
        - rain
        - snow
    Current implementation looks for a dictionary with a 'main' key, coresponding to a subdictionary
        which contains a 'temp' entry 
    Also takes user_preferences, a pandas dataframe with the same columns as weather_dict, but also has columns
        - dt
        - rating
    If user_preferences = None, use default temp cutoff
    
    Returns -1 or 1, for negative or positive predicted user response to weather.
    """
    temp = weather_dict['feels_like'] # temperature in Kelvin
    if user_preferences is None or len(user_preferences) < 50:
        if temp > 294: # 294K, 70 F 
            return 1
        else:
            return -1
    else:
        learned_preference_model = learn_preferences(user_preferences)
        return learned_preference_model.predict(pd.DataFrame(weather_dict, index =[0]))

def learn_preferences(user_preferences):
    """
    Trains and returns a logistic regression model based on the user_preferences, which is a pd DataFrame with:
        - dt
        - temp
        - feels_like
        - humidity
        - clouds 
        - wind_speed
        - rain
        - snow
        - rating
    """
    X, y = user_preferences.drop(['rating', 'dt'], axis = 1), user_preferences['rating']
    lg = LogisticRegression(max_iter = 1000)
    cvals = np.logspace(-4, -0.5, 30)
    clf = GridSearchCV(lg, [{'C':cvals}], cv = 5)
    return clf.fit(X, y)

def bad_weather_rec(weather):
    """
    To be called in case of user-disliked weather. 
    Returns (currently) just a fun pun to be displayed instead of actual weather data. 
    """
    output = ""
    if weather['rain'] > 0:
        output +=  np.random.choice([
            "People using umbrellas always seem to be under the weather.\n\n"
        ])
    if weather['snow'] > 0:
        output += np.random.choice([
            "The snowstorm arrived at a fortuitous moment. \nIt was white on time.\n\n"
        ])
    if weather['clouds'] > 50:
        output += np.random.choice([
            "What did one raindrop say to the other? \nTwo’s company, three’s a cloud. \n\n"
        ])
    if weather['feels_like'] < 273:
        output += np.random.choice([
            "Cold winter weather is snow laughing matter!\n\n"
        ])
    if weather['feels_like'] > 303:
        output += np.random.choice([
            "I received a message from the sun, it was enlightening.\n\n"
        ])
    if weather['humidity'] > 50: 
        output += np.random.choice([
            "The secretary left me a message saying humidity will hit 90% today... She wrote it on a sticky note \n\n"
        ])
    if weather['wind_speed'] > 30:
        output += np.random.choice([
            "Coming up with weather puns is a breeze. \n\n"
        ])
    return output
    
def get_city(userID):
    """
    Takes userID, looks up their city from DB
    """
#     TODO: make this work properly
    curr_user = User.objects.filter(uuid=userID).first()
    return curr_user.city

def get_user_preferences(userID):
    """
    Takes userID, returns a pandas df of their user preferences
    """
#     TODO: make this work properly
    ratings = list(map(list, WeatherRating.objects.filter(uuid=userID).values_list('dt', 'temp', 'feels_like', 'humidity', 'wind_speed', 'clouds', 'rain', 'snow', 'rating')))
    ratings_df = pd.DataFrame(ratings, columns=['dt', 'temp', 'feels_like', 'humidity', 'wind_speed', 'clouds', 'rain', 'snow', 'rating'])
    
    
    return ratings_df

def main(userID, return_descriptor=False):
    user_preferences = get_user_preferences(userID)
    city = get_city(userID)   
    weather = get_weather(city)
    
#     TODO
#     similar_preferences = get_similar_preferences(userID, numsamples = 100)
#     TODO
    
    user_assessment = assess_weather(weather, user_preferences)
    if user_assessment == 1:
        return get_weather(city, return_descriptor=return_descriptor)
    elif user_assessment == -1:
        return bad_weather_rec(weather)
    
    

# temperature cutoffs for warm-lover and cold-lover are based on weather conditions for oct 25, ATX- to show different cases in demo
    
# dummy data generation
def generate_dummy_data1(uuid, num_samples=50):
    """
    A hot weather lover, so good weather = anything below 100 F
    """

    np.random.seed(429)
    base = datetime.datetime.today()
    for x in range(num_samples):
        temp = np.random.normal(loc = 293, scale = 5, size = 1)
        rain = np.random.normal(scale = 10, size = 1)
        snow = np.random.normal(scale = 10, size = 1)
        rating1 = np.random.binomial(1, .95) # more likely to produce 1
        rating2 = np.random.binomial(1, .05) # more likely to produce 0
        new_weather_rating = WeatherRating.objects.create(
            uuid= uuid,
            dt = int((base - datetime.timedelta(days=x)).timestamp()),
            temp= temp, 
            humidity= 50 + np.random.normal(scale = 25, size = 1),
            clouds= 50 + np.random.normal(scale = 25, size = 1), 
            wind_speed= np.random.gamma(shape = 5, size = 1),
            rain = 0 if rain < 0 else rain,
            snow = 0 if snow < 0 else snow,
            feels_like= temp + np.random.normal(scale = 2, size = 1),
            rating = (rating1 if rating1 == 1 else -1) if temp < 310 else (rating2 if rating2 == 1 else -1),
        )
        new_weather_rating.save()


# dummy data generation
def generate_dummy_data2(uuid, num_samples=50):
    """
    A cold weather lover, so good weather = anything below 32 F 
    """
    np.random.seed(429)
    base = datetime.datetime.today()
    for x in range(num_samples):
        temp = np.random.normal(loc = 293, scale = 5, size = 1)
        rain = np.random.normal(scale = 10, size = 1)
        snow = np.random.normal(scale = 10, size = 1)
        rating1 = np.random.binomial(1, .95)
        rating2 = np.random.binomial(1, .05)
        new_weather_rating = WeatherRating.objects.create(
            uuid= uuid,
            dt = int((base - datetime.timedelta(days=x)).timestamp()),
            temp= temp, 
            humidity= 50 + np.random.normal(scale = 25, size = 1),
            clouds= 50 + np.random.normal(scale = 25, size = 1), 
            wind_speed= np.random.gamma(shape = 5, size = 1),
            rain = 0 if rain < 0 else rain,
            snow = 0 if snow < 0 else snow,
            feels_like= temp + np.random.normal(scale = 2, size = 1),
            rating= (rating1 if rating1 == 1 else -1) if temp < 273 else (rating2 if rating2 == 1 else -1),
        )
        new_weather_rating.save()

def KtoF(T):
    return (T - 273.15) * 9/5 + 32
    