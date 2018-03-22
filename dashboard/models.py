from django.contrib.auth.models import User
from django.db import models


# from .models import Monster

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    experience = models.PositiveIntegerField(default=0)
    gold = models.PositiveIntegerField(default=0)
    items = models.ManyToManyField('Item')

    @property
    def get_level(self):
        experience = Experience.objects.filter(experience__lte=self.experience).last()
        return experience.level



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
    drop_chance = models.PositiveIntegerField(default=1)  #generatePseudoRandomNumber(0, 100) if(rand <= dropChance * 100)



class Monster(models.Model):
    name = models.CharField(max_length=50, default="")
    experience = models.PositiveIntegerField(default=1)
    gold = models.PositiveIntegerField(default=0)
    health = models.PositiveIntegerField(default=1)
    sprite_url = models.CharField(max_length=200)
    items = models.ManyToManyField(Item)


class Experience(models.Model):
    experience = models.PositiveIntegerField()
    level = models.PositiveIntegerField(primary_key=True)


class UserMonster(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monster = models.ForeignKey(Monster, on_delete=models.CASCADE)
    health_left = models.PositiveIntegerField()
    @property
    def get_health_percentage(self):
        return (self.health_left/self.monster.health)*100