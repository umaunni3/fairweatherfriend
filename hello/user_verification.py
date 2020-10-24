""" Register new users and identify existing users. """

import uuid
import requests
from .models import User

def registerNewUser(response):
    """
    If no user object currently exists for the current visitor, do the following:
        - generate UUID corresponding to current user
            - make sure UUID is actually unique?
        - store UUID in user's document cookie
        - create a new User model instance, and associate it with the given UUID
        - return the new User object, for convenience
    """
    
    new_uuid = uuid.uuid1()
    # trim the UUID to half its size (64 instead of 128) so that
    # we can store it in a BigIntegerField attribute in the model
    uuid_bytes_shortened = new_uuid.bytes[:4]
    short_uuid = int.from_bytes(uuid_bytes_shortened, "big")
    
    # set the cookie to associate that user with their UUID
    response.set_cookie("uuid", str(short_uuid))
    
    
    
    # create a new User object with the given UUID
    new_user = User.objects.create(
        uuid=short_uuid,
        past_temps=list(),
    )
    
    new_user.save()
    return new_user
    
def getUser(request):
    assert request.COOKIES.get("uuid") is not None; "current site visitor's cookie does not contain uuid field"
    
    user_uuid = int(request.COOKIES.get("uuid"))
    curr_user = User.objects.filter(uuid=user_uuid).first()
    return curr_user

def checkUser(request, response):
    if not request.COOKIES.get("uuid"):
        curr_user = registerNewUser(response)
    else:
        # get the user object and return it
        curr_user = getUser(request)
    return curr_user
        
#def updateUser