from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField, TextField
from django.db.models.fields.related import ForeignKey


class Website_users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.TextField()
    secret_key = models.TextField()

class user_trade_records(models.Model):
    user = ForeignKey(Website_users, on_delete=models.CASCADE)
    record_id = models.CharField(unique=True, blank=False, max_length=30)
    symbol = models.TextField(max_length=10, blank=False)
    price = models.FloatField(blank=False)
    quantity = models.FloatField(blank=False)
    cost = models.FloatField(blank=False)
    time = models.DateField(auto_now=False, blank=False)
    isBuyer = BooleanField(blank=False)


