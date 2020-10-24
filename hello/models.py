from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
#class Greeting(models.Model):
#    when = models.DateTimeField("date created", auto_now_add=True)


# todo: add last_modified field so we can see if we need
# to actually add a new weather to the user's list or not
class User(models.Model):
    uuid = models.IntegerField()
    past_temps = ArrayField(models.IntegerField(), default=list)
    city = models.TextField(default="Austin")
    
    def add_new_temp(self, new_temp):
        assert isinstance(new_temp, int); 'Please provide an integer-valued temperature'
        
        self.past_temps.append(new_temp)
        self.save()
        
    def get_user_temps(self):
        return self.past_temps
    
# represents a weather rating for a single user
class WeatherRating(models.Model):
    uuid = models.BigIntegerField()
    dt = models.BigIntegerField()
    
    temp = models.IntegerField()
    feels_like = models.IntegerField()
    humidity = models.IntegerField()
    wind_speed = models.IntegerField()
    clouds = models.IntegerField()
    rain = models.IntegerField()
    snow = models.IntegerField()
    rating = models.IntegerField()
    
    # a user cannot submit multiple ratings for the same date's weather
    class Meta:
        unique_together = ("uuid", "dt")
    