import requests
from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from .user_verification import checkUser, getUser

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    response = render(request, "index.html")
    curr_user = checkUser(request, response)
    print("current user is: {}".format(curr_user.uuid))
#    return HttpResponse('<pre>' + r.text + '</pre>')
    return response

def whoami(request):
    curr_user = getUser(request)
    return render(request, "whoami.html", {"user": user})

def db(request):

    user = User(uuid=0)
    user.save()

    users = User.objects.all()
     
    return render(request, "db.html", {"greetings": users})
#
#def addTemp(request):
#    # add the current temperature to the current user's db list thing!
#    
    
