from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class UserEmailVerify(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	is_verified = models.DateTimeField(default=None, blank=True, null=True)
	created = models.DateTimeField(default=timezone.now )	
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.is_verified

class Photo(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	photo = models.ImageField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.OneToOneField(Photo,on_delete=models.CASCADE)
    gender = models.CharField(max_length=20,null=True,blank=True,default=None)
    dob = models.DateField(null=True, blank=True,default=None)
    about = models.TextField(null=True,blank=True,default=None)
    status = models.CharField(default='Online',max_length=50)

