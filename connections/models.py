from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from chatproject.models import SoftDeletionModel

class Connection(SoftDeletionModel):
	req_from =  models.ForeignKey(User,on_delete=models.CASCADE,related_name='req_from') 
	req_to =  models.ForeignKey(User,on_delete=models.CASCADE,related_name='req_to')
	accepted_at = models.DateTimeField(default=None,blank=True,null=True)

	# class Meta:
	    # unique_together = ('req_from', 'req_to','deleted_at')
