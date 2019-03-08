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
