from django.db import models
from django.contrib.auth.models import User


class Website_users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.TextField()
    secret_key = models.TextField()

