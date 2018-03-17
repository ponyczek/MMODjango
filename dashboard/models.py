from django.contrib.auth.models import User
from django.db import models
# from .models import Monster

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    experience = models.PositiveIntegerField(default=0)
    gold = models.PositiveIntegerField(default=0)
    items = models.ManyToManyField('Item')


    # @property
    # def get_level(self):
    #
    #     if self.end_date > timezone.now() and timezone.now() > self.start_date:
    #         return True
    #     else:
    #         return False

    def __unicode__(self):
        return self.user.username


ItemType = (
    ('1', 'Helmet'),
    ('2', 'Armor'),
    ('3', 'Shield'),
    ('4', 'Weapon'),
)

class Item(models.Model):
    arm = models.PositiveIntegerField(default=0)
    defence = models.PositiveIntegerField(default=0)
    atk = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=1, choices=ItemType)
    monsters = models.ManyToManyField('Monster')

class Monster(models.Model):
    experience = models.PositiveIntegerField(default=1)
    gold = models.PositiveIntegerField(default=0)
    health = models.PositiveIntegerField(default=1)
    sprite_url = models.CharField(max_length=200)
    items = models.ManyToManyField(Item)




