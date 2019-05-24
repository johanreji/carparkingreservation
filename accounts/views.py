
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User
from django import forms
from .forms import  RegisterForm
from django.urls import reverse
from django.contrib import messages
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
   user.set_password(user_form.cleaned_data["password"])
   user=user_form.save()
   user = authenticate(email=user_form.cleaned_data["email"], password=user_form.cleaned_data["password"])
   if user is not None:
    print("user model: "+ str(user))
    login(request, user)
    messages.success(request, 'Sign up Successfull')
    return redirect(reverse('gridapp:index'))
   else:
    messages.error(request, 'Internal error')	
    return redirect(reverse('gridapp:index'))
  else:
   vs=user_form.visible_fields()
   errorlist=[val for field in vs if field.errors for val in field.errors] 
   #errorhtml=user_form.errors
   messages.warning(request, ' , '.join(errorlist)) 
   return redirect(reverse('gridapp:index'))
 elif request.method == "GET":
  messages.error(request, "invalid request")
  return redirect(reverse('gridapp:index'))
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
   messages.success(request, 'Login Successfull')
   return redirect(reverse('gridapp:index'))
  else:	
   messages.warning(request, "Login error, Please check username and password")    
   return redirect(reverse('gridapp:index'))
 elif request.method == "GET":
  messages.error(request, "invalid request")
  return redirect(reverse('gridapp:index'))


def logoutuser(request):
 logout(request)
 return redirect(reverse('gridapp:index'))
 
@login_required(login_url='gridapp:index')
def profile(request):
	return render(request, "accounts/profile.html/")

  






# from django.urls import reverse_lazy
# from django.views import generic

# from .forms import CustomUserCreationForm

# class SignUp(generic.CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'customsignup.html'