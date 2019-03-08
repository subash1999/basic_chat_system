from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from chatproject.models import SoftDeletionModel

class Thread(SoftDeletionModel):
    thread_Name = models.CharField(max_length=255,default=None, blank=True, null=True)
    is_group = models.CharField(max_length=255,default=None, blank=True, null=True)
    
class UserThread(SoftDeletionModel):
    therad = models.ForeignKey(Thread,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)  
    is_group = models.CharField(max_length=255,default=None, blank=True, null=True)

class Message(SoftDeletionModel):
    thread = models.ForeignKey(Thread,on_delete=models.SET_NULL,null=True)
    message = models.TextField()
    sender =  models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name='sender')  
    receiver =  models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='receiver')  
    deleted_for_sender =  models.DateTimeField(default=None,blank=True,null=True)  
    deleted_for_receiver =  models.DateTimeField(default=None,blank=True,null=True)  
    
