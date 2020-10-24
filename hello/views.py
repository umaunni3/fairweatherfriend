import requests
from django.shortcuts import render
from django.http import HttpResponse

from .models import User
from .user_verification import checkUser, getUser, registerNewUser

# Create your views here.
def index(request):
    # check if the current site visitor is already registered 
    # in our db as a user; if not, create a 
    # new user profile for them.
    if not request.COOKIES.get("uuid"):
        # use default temp/weather thresholds for
        # determining weather quality
        response = render(request, "index.html")
        
        curr_user = registerNewUser()
    
    response = render(request, "index.html")
    curr_user = checkUser(request, response)
    print("current user is: {}".format(curr_user.uuid))
#    return HttpResponse('<pre>' + r.text + '</pre>')
    return response

def whoami(request):
    curr_user = getUser(request)
    return render(request, "whoami.html", {"user": curr_user})

def db(request):

    user = User(uuid=0)
    user.save()

    users = User.objects.all()
     
    return render(request, "db.html", {"greetings": users})
#
#def addTemp(request):
#    # add the current temperature to the current user's db list thing!
#    
    
