
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User
from django import forms
from .forms import  RegisterForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
def signup(request):
 if request.method == "POST":
  user_form = RegisterForm(request.POST)
  print("sign up data: " + str(request.POST))
  if user_form.is_valid():
   user=user_form.save()
   user.set_password(request.POST["password"])
   user=user_form.save()

   user = authenticate(email=request.POST["email"], password=request.POST["password"])
   if user is not None:
   	print("user model: "+ str(user))
   	login(request, user)
   	return redirect(reverse('index'))
   else:	
    return redirect("/grid/getslots/html/")
  else:
   return redirect("/grid/getslots/html/")
 elif request.method == "GET":
  return redirect("/grid/getslots/html/")

@csrf_exempt
def loginuser(request):
 if request.method == "POST":
  email = request.POST["email"]
  password = request.POST["password"]
  print("login up data: " + str(request.POST))
  user = authenticate(email=email, password=password)
  if user is not None:
   print("user model: "+ str(user))
   login(request, user)
   return redirect("/grid/getslots/html/")
  else:	
   return redirect("/grid/getslots/html/")
 elif request.method == "GET":
  return redirect('/grid/getslots/html/')


def logoutuser(request):
 logout(request)
 return redirect("/grid/getslots/html/")
 
@login_required(login_url="/grid/getslots/html/")
def profile(request):
	return render(request, "accounts/profile.html/")

  






# from django.urls import reverse_lazy
# from django.views import generic

# from .forms import CustomUserCreationForm

# class SignUp(generic.CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'customsignup.html'