from django.db import models
from django.contrib.auth.models import User
from meals.models import Dish


class User_extend(models.Model):

    user = models.OneToOneField(User)
    state = models.IntegerField(blank=True, null=True)
    wunderlist_token = models.CharField(max_length=300, blank=True, null=True)

    def get_favourites(self):
        return [fav.dish for fav in self.user.user_extend.favourite_set.all()]

class Favourite(models.Model):
    user = models.ForeignKey(User_extend)
    dish = models.ForeignKey(Dish)
