from django.contrib.auth.models import User
from django.db import models

class Dish(models.Model):
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    recipe = models.CharField(max_length=10000)
    picture = models.ImageField(upload_to='dish_pictures/', blank=True, null=True)

class Ingredient(models.Model):
    dish = models.ForeignKey(Dish)
    name = models.CharField(max_length=30)
    amount = models.FloatField()
    UNIT = (
        ('kg', 'kg'),
        ('g', 'g'),
        ('L', 'L'),
        ('ml', 'ml'),
        ('tbs', 'tbs'),
        ('ts', 'ts'),
        ('pc', 'pc'),
    )
    unit = models.CharField(max_length=20, choices=UNIT, default='pc')


class Rating(models.Model):
    dish = models.ForeignKey(Dish)
    RATING = (
        ('ONE', 'ONE'),
        ('TWO', 'TWO'),
        ('THREE', 'THREE'),
        ('FOUR', 'FOUR'),
    )
    rating = models.CharField(max_length=5, choices=RATING, default='ONE')
    user = models.ForeignKey(User)	
