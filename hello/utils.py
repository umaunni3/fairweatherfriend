#imports 

import requests, json
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import datetime
import matplotlib.pyplot as plt

def get_weather(city_name):
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
            "People using umbrellas always seem to be under the weather.\n"
        ])
    if weather['snow'] > 0:
        output += np.random.choice([
            "The snowstorm arrived at a fortuitous moment. \n It was white on time.\n"
        ])
    if weather['clouds'] > 50:
        output += np.random.choice([
            "What did one raindrop say to the other? \n Two’s company, three’s a cloud. \n"
        ])
    if weather['feels_like'] < 273:
        pass
    if weather['humidity'] > 50: 
        output += np.random.choice([
            "The secretary left me a message saying humidity will hit 90% today... She wrote it on a sticky note \n"
        ])
    if weather['wind_speed'] > 30:
        output += np.random.choice([
            "Coming up with weather puns is a breeze. \n"
        ])
    
def get_city(userID):
    """
    Takes userID, looks up their city from DB
    """
#     TODO: make this work properly
    return "Austin"

def get_user_preferences(userID):
    """
    Takes userID, returns a pandas df of their user preferences
    """
#     TODO: make this work properly
    return train_prefs

def main(userID):
    user_preferences = get_user_preferences(userID)
    city = get_city(userID)   
    weather = get_weather(city)
    
#     TODO
#     similar_preferences = get_similar_preferences(userID, numsamples = 100)
#     TODO
    
    user_assessment = assess_weather(weather, user_preferences)
    if user_assessment == 1:
        return weather
    elif user_assessment == -1:
        return bad_weather_rec()