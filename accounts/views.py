from django.utils.safestring import mark_safe
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,Http404
from django.contrib.auth.models import User
from django.contrib import auth,messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Count
from django.core import serializers
from django.contrib.auth.hashers import check_password

import json
import time

from connections.models import Connection 
from .models import UserEmailVerify,Profile,Photo

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

				# photo of the user
				photo = Photo()
				photo.user = user
				photo.photo = '/media/system/no_user_img.jpg'
				photo.save()

				#profile of the user
				profile = Profile()
				profile.user = user
				profile.profile_pic = photo
				profile.save()

				messages.add_message(request,messages.SUCCESS,'User Successfully Registered!!')
				return redirect('accounts:login')
		else:
			messages.add_message(request,messages.ERROR,'Password Do Not Matches with Password Confirmation')
			return redirect('accounts:register')
		
	else:
		return render(request,'accounts/login_and_register.html',{'page_title':'Register'}) 

@csrf_exempt
def isUsernameAvailable(request):
	
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

def connectedUsersSearch(request):	
	connections = Connection.objects.filter(Q(req_from=request.user)|
			Q(req_to=request.user)).exclude(accepted_at=None)
	connected_users = set()
	for connection in connections:
		if connection.req_from!=request.user:
			connected_users.add(connection.req_from)
		if connection.req_to!=request.user:
			connected_users.add(connection.req_to)
	searched_users = []
	search = request.GET.get('search')
	for user in connected_users:	
		username = user.username.lower()
		first_name = user.first_name.lower()
		last_name = user.last_name.lower()
		# searching in the connected_users
		if(search!=None and search!=''):
			if (search in username) or (search in first_name) or (search in last_name):
				searched_users.append(user)
		else:
			searched_users.append(user)
	data = serializers.serialize('json', searched_users)
	return HttpResponse(data, content_type="application/json")

def profile(request):
	connected_connections = Connection.objects.filter(Q(req_from=request.user)|
			Q(req_to=request.user)).exclude(accepted_at=None)
	user = request.user
	user.num_connected_users = connected_connections.count()
	not_connected_users = Connection.objects.filter(Q(req_to=request.user)).filter(accepted_at=None)
	user.num_connect_requests = not_connected_users.count()
	photo = Photo.objects.filter(user=request.user)
	user.num_photos = photo.count()
	data = {
	'user' : user,
	'page_title':str(request.user.get_full_name())+': Profile',
	}
	return render(request,'accounts/profile_index.html',data)

def authSetting(request):
	data = {
		'page_title' : str(request.user.get_full_name())+': Authentication Settings',
	}
	return render(request,'accounts/auth_setting.html',data)

def changeUsername(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		try:
			user = User.objects.filter(username=username)
			if(user.count() > 0):
				if (user[0].username == request.user.username):
					messages.add_message(request,messages.WARNING,'No Changes in Username')		
				else : 
					messages.add_message(request,messages.ERROR,'Username Already taken!! Please choose another one')
			else : 
				request.user.username = username
				request.user.save()
				messages.add_message(request,messages.SUCCESS,'Username Successfully Changed')	
		except User.DoesNotExist as e:
			request.user.username = username
			request.user.save()
			messages.add_message(request,messages.SUCCESS,'Username Successfully Changed')	
		return redirect('accounts:auth_setting')	
	else : 
		raise Http404	
def changePassword(request):
	errors = []
	if request.method == 'POST':
		old = request.POST.get('old_password')
		new = request.POST.get('new_password')
		new_confirm = request.POST.get('new_password_confirmation')

		if new != new_confirm :
			msg = 'Confirm Password Doesnot Match With the Password Entered'
			errors.append(msg)
			messages.add_message(request,messages.ERROR,msg)
		else:
			check_pass = check_password(old, request.user.password)
			if not check_pass:
				msg = 'Old Password is wrong !! Password is not Changed'
				errors.append(msg)
				messages.add_message(request,messages.ERROR,msg)
			else:
				user = request.user
				request.user.set_password(new) 
				request.user.save()
				auth.login(request,user)
				msg = 'Password is Changed Successfully'
				errors.append(msg)
				messages.add_message(request,messages.SUCCESS,msg)
		return redirect('accounts:auth_setting')
	else:
		raise Http404
def deleteAccount(request):
	errors = []
	if request.method == 'POST':
		check_pass = check_password(request.POST.get('password'), request.user.password)
		if not check_pass:
			msg = 'Password Wrong While Deleting Account'
			errors.append(msg)
			messages.add_message(request,messages.ERROR,msg)
		else:
			msg = 'Account Deleted Successfully'
			errors.append(msg)
			messages.add_message(request,messages.SUCCESS,msg)
			request.user.delete()
			return redirect('accounts:register')
		return redirect('accounts:auth_setting')
	else:
		raise Http404
def otherUsersSearch(request):	
	connections = Connection.objects.filter(Q(req_from=request.user)|
			Q(req_to=request.user)).exclude(accepted_at=None)
	connected_users = set()
	for connection in connections:
		if connection.req_from!=request.user:
			connected_users.add(connection.req_from)
		if connection.req_to!=request.user:
			connected_users.add(connection.req_to)
	other_users = User.objects
	for connection in connections:
		other_users = other_users.exclude(username=connection.req_from)
		other_users = other_users.exclude(username=connection.req_to)
	searched_users = []
	search = request.GET.get('search')
	for user in other_users:	
		username = user.username.lower()
		first_name = user.first_name.lower()
		last_name = user.last_name.lower()
		# searching in the connected_users
		if(search!=None and search!=''):
			if (search in username) or (search in first_name) or (search in last_name):
				searched_users.append(user)
		else:
			searched_users.append(user)
	return HttpResponse(searched_users)
	data = serializers.serialize('json', searched_users)
	return HttpResponse(data, content_type="application/json")