from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,Http404
from django.utils.safestring import mark_safe
from .models import Thread,UserThread,Message
from django.contrib.auth.models import User

import json

def index(request):
	return render(request,'basic_chat/index.html')

def chat(request, thread_id=None):
	# if there is no parameter passed make the thread_id none
	if thread_id == None:
		return render(request, 'basic_chat/chatroom/chatroom_layout.html', {
			'room_name_json': "Chat Room",
			'page_title':chat_room_name + ' : '+'Messages',
			'current_thread' : None,
			'threads' : threads,
		})
	thread_found = True
	try:
		thread = Thread.objects.get(pk=thread_id)
		if (thread == None):
			thread_found = False
			raise Http404			
	except :
		thread_found = False
		raise Http404
	chat_room_name,profile_pic,user = threadProperties(request,thread_id)
	
	# current chat  
	current_chat = {}
	current_chat['profile_pic'] = profile_pic
	current_chat['room_name'] = chat_room_name
	current_chat['thread_id'] = str(thread_id)

	#list of chat threads of current user
	user_threads = UserThread.objects.filter(user = request.user).distinct().order_by('created_at')
	threads = []
	for user_thread in user_threads:
		room_name,pic,user = threadProperties(request,user_thread.thread.id)
		thread = {
			'room_name' : room_name,
			'profile_pic' : pic,
			'thread_id' : str(user_thread.thread.id),
			'user' : user, 
		}
		threads.append(thread)

	return render(request, 'basic_chat/chatroom/chatroom_layout.html', {
    	'room_name_json': mark_safe(json.dumps(current_chat['thread_id'])),
        'page_title':chat_room_name + ' : '+'Messages',
        'current_thread' : current_chat,
        'threads' : threads,
    })

def updateStatus(request):
	if request.method == 'POST':
		msg = "Status Changes Successfully to the "+str(request.POST.get('status'))
		msg_type = "success"
		status = str(request.POST.get('status'))
		if ((status != None or status != "") and (status.lower() == "online".lower() or status.lower() == "offline".lower())):
			request.user.profile.status = request.POST.get('status') 
			request.user.profile.save()
		else : 
			msg_type = "error"
			msg = "Invalid Request !! Failed to Change User Status"
		response = {
			'msg' : msg,
			'msg_type' : msg_type,
		}
		return JsonResponse(response)
	else : 
		raise Http404
def threadProperties(request,thread_id):
	thread = Thread.objects.get(pk=thread_id)
	user_threads = UserThread.objects.filter(thread=thread)	
	# finding the chat room name and user with whom message is ongoing
	chat_room_name = None
	user = None
	if (thread.thread_name != None):
		chat_room_name = thread.thread_name
	else : 
		chat_room_name = ''
		for key,user_thread in enumerate(user_threads):
			if user_thread.user != request.user : 
				chat_room_name += chat_room_name + user_thread.user.first_name + ' ' + user_thread.user.last_name
				if (key != user_threads.count()-1):
					chat_room_name += ','
				if (user_threads.count() == 2):
					user = user_thread.user

	# finding the picture of the user
	profile_pic = user.profile.profile_pic.photo
	return [chat_room_name,profile_pic,user]

def newMsg(request):
	if request.method == 'POST':
		user_to_check = User.objects.get(pk=request.POST.get('user_id'))

		# checking first if there is already a thread present
		threads = Thread.objects.all()
		for thread in threads : 
			# print(thread.user_threads)
			user_threads = UserThread.objects.filter(thread=thread)
			if user_threads.count() != 2 :
				continue
			user1 = user_threads[0].user
			user2 = user_threads[1].user
			if (user1 == user_to_check and user2 == request.user ) or (user2 == user_to_check and user1 == request.user) :
				return redirect('chat:chat',thread_id=thread.id)

		# if there is a message thread present it will return if not the program will further continue
		# creating a new message thread
		thread = Thread()
		thread.save()

		# adding users to that thread

		# first the current logined user
		user_thread = UserThread()
		user_thread.thread = thread
		user_thread.user = request.user
		user_thread.save()

		# first the user with whom we want to chat
		user_thread = UserThread()
		user_thread.thread = thread
		user_thread.user = user_to_check
		user_thread.save()

		return redirect('chat:chat',thread_id=thread.id)
	else : 
		raise Http404