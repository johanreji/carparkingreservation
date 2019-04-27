

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

def register(request):
 if request.method == "POST":
  name = request.POST["name"]
  email = request.POST["email"]
  password = request.POST["password"]
  user = User.objects.create_user(name, email, password)
  user.save()
  return HttpResponse("user created")
 elif request.method == "GET":
  return render(request, "register.html")  	