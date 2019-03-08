from django.utils.safestring import mark_safe
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth,messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import time

from .models import UserEmailVerify

# Create your views here.
def login(request):
	if request.method=='POST':
		try:
			user = auth.authenticate(request,username=request.POST['username'],password = request.POST['password'])
			if user is not None:
				auth.login(request,user)
				messages.add_message(request,messages.SUCCESS,'Successfull Login')
				return redirect('basic:index')
			else:
				messages.add_message(request,messages.ERROR,'Either Username or password is wrong')
				return redirect('accounts:login')		
		except User.DoesNotExist as e:
			messages.add_message(request,messages.ERROR,'Either Username or password is wrong')
			return redirect('accounts:login')	
		
	else:
		return render(request,'accounts/login_and_register.html',{'page_title':'Login'})

	
def register(request):
	# print(request.POST)
	#check if a request is of post method
	if request.method=='POST':
		#check if password matches
		if request.POST['password']==request.POST['password_confirmation']:
			#check if user exists
			try:
				user = User.objects.get(username=request.POST['username'])
				messages.add_message(request,messages.ERROR,'Username Already taken!! Please choose another one')
				return redirect('accounts:register')				
			except User.DoesNotExist as e:
				user = User.objects.create_user(
					password=request.POST['password'],
					email=str(request.POST['username'])+'@chatproject.com',
					first_name=str(request.POST['fname']).capitalize(),
					last_name=str(request.POST['lname']).capitalize(),
					username=request.POST['username'],
					)				
				# making is email verified false 
				user_email_verify = UserEmailVerify()
				user_email_verify.user = user
				# as no value is given in is_verified field it will be null while saving
				user_email_verify.save()

				messages.add_message(request,messages.SUCCESS,'User Successfully Registered!! Please Confirm Your Email')
				return redirect('accounts:login')
		else:
			messages.add_message(request,messages.ERROR,'Password Do Not Matches with Password Confirmation')
			return redirect('accounts:register')
		
	else:
		return render(request,'accounts/login_and_register.html',{'page_title':'Register'}) 

@csrf_exempt
def isUsernameAvailable(request):
	print(request.POST)
	# return_val = "true"

	if(request.method=='POST'):
		try:
			user = User.objects.get(username=request.POST['username'])
			return_val = "false"
		except:
			return_val = "true"
	else:		
		try:
			user = User.objects.get(username=request.username)
			return_val =  "false"
		except:
			return_val =  "true"

	return HttpResponse(return_val);

def logout(request):
	auth.logout(request)
	messages.add_message(request,messages.SUCCESS,'Successfully Logouted')
	return redirect('accounts:login')