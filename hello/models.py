from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
#class Greeting(models.Model):
#    when = models.DateTimeField("date created", auto_now_add=True)


# todo: add last_modified field so we can see if we need
# to actually add a new weather to the user's list or not
class User(models.Model):
    uuid = models.IntegerField()
    past_temps = ArrayField(models.BigIntegerField(), default=list)
    
    def add_new_temp(self, new_temp):
        assert isinstance(new_temp, int); 'Please provide an integer-valued temperature'
        
        self.past_temps.append(new_temp)
        self.save()
        
    def get_user_temps(self):
        return self.past_temps