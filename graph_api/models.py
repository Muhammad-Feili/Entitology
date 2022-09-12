from django.db import models
from django.contrib.auth.models import User

class UserAccessLimit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    limit = models.IntegerField(default=300)
    has_access = models.BooleanField(default=True)


    def has_access_limit(self, user):
        return self.has_access
