from django.db import models
from django.contrib.auth.models import User
from meals.models import Dish

class Favourite(models.Model):
    user = models.OneToOneField(User)
    dish = models.ForeignKey(Dish)
