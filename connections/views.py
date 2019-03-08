from django.utils.safestring import mark_safe
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth,messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
import json
import time

from .models import Connection

# Create your views here.
def addConnection(request):
	if request.method == 'POST':
		try:
			user = User.objects.get(pk=request.POST['connect_with_user_id'])
			if user is None:
				print('user is none')
				messages.error(request,'Invalid Request')
			else:
				if (request.user == user):
					messages.error(request,"You cannot connect with yourself")
				else : 	
					existed_request_1 = Connection.objects.filter(req_from=request.user,req_to=user)
					existed_request_2 = Connection.objects.filter(req_from=request.user,req_to=user)
					if len(existed_request_1) == 0 and len(existed_request_2) == 0:
						connection = Connection()
						connection.req_from = request.user
						connection.req_to = user
						connection.save()
						msg = 'Connect Request Sent to '+user.first_name+' '+user.last_name+' ('+user.username+')'
						# msg = 'Connect Request Sent '
						messages.success(request, msg)					
					else:
						msg = 'Connect Request is already sent OR already connected to '+user.first_name+' '+user.last_name+' ('+user.username+')'
						# msg = 'Connect Request Already Sent'
						messages.error(request,msg)								
		except Exception as e:			
			messages.error(request, 'Invalid Request')
		next = request.POST.get('next', '/')
		return HttpResponseRedirect(next)

	users = User.objects.all()
	
	# searching the users
	if request.GET.get('search') != None:
		search = request.GET['search']
		# users = User.objects.filter(Q(first_name__unaccent__icontains=search)|
		# 	Q(last_name__unaccent__icontains=search)|
		# 	Q(username__unaccent__icontains=search))
		users = User.objects.filter(Q(first_name__icontains=search)|
			Q(last_name__icontains=search)|
			Q(username__icontains=search))
	
	users = users.order_by('-date_joined')
	
	page = None
	try:
		page = request.GET['page']
	except :
		page = 1
	if page is None :
		page =1

	
	for user in users:
		user.connection = getUserConnection(request.user.id,user.id)
		
	paginator = Paginator(users, 15)
	users = paginator.get_page(page)

	pagination_pages_until = int(page) + 5	
	
	return render(request,'connections/add_connections.html',{'users':users,
		'pagination_pages_until':pagination_pages_until,
		'page_title':'Add Connections'
		})

def getUserConnection(user_id_1,user_id_2):
	user_1 = User.objects.get(pk=user_id_1)
	user_2 = User.objects.get(pk=user_id_2)
	
	conn = Connection.objects.filter(Q(req_from=user_1,req_to=user_2) | Q(req_from=user_2,req_to=user_1)).filter(deleted_at=None)
	if len(conn) is 0:
		return None
	return conn[0]

def deleteConnection(request):
	if request.method == 'POST':
		try:
			conn = Connection.objects.get(pk=request.POST['connection_id'])
			conn.hard_delete()
			messages.success(request, 'Connection Deleted Successfully ')
		except:
			messages.error(request, 'Error while deleting the Connection')
		next = request.POST.get('next', '/')
		return HttpResponseRedirect(next)

	else:
		return HttpResponse('Invalid Request')

def confirmConnection(request):
	if request.method == 'POST':
		conn = Connection.objects.get(pk=request.POST['connection_id'])
		try:
			conn.accepted_at = timezone.now()
			conn.save()
			messages.success(request, 'You are now Connected to user : '+str(conn.req_from))
		except:
			messages.error(request, 'Error while confirming the Connection')
		next = request.POST.get('next', '/')
		return HttpResponseRedirect(next)

	else:
		return HttpResponse('Invalid Request')