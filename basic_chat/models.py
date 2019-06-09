from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 
from chatproject.models import SoftDeletionModel

class Thread(SoftDeletionModel):
    thread_name = models.CharField(max_length=255,default=None, blank=True, null=True)
    is_group = models.BooleanField(default=False,blank=True,null=True)
    
class UserThread(SoftDeletionModel):
    thread = models.ForeignKey(Thread,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)  
    
class Message(SoftDeletionModel):
    thread = models.ForeignKey(Thread,on_delete=models.SET_NULL,null=True)
    message = models.TextField()
    sender =  models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name='sender')  
    
class DeletedMesssage(SoftDeletionModel):
    message = models.ForeignKey(Message,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
