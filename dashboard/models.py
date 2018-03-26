from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max


# from .models import Monster

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    experience = models.PositiveIntegerField(default=0)
    gold = models.PositiveIntegerField(default=0)
    items = models.ManyToManyField('Item', through="UserItem")


    @property
    def get_level(self):
        experience = Experience.objects.filter(experience__lte=self.experience).last()
        return experience.level

    @property
    def get_best_helmet(self):
        return self.items.filter(type=1).latest('arm')

    @property
    def get_best_armor(self):
        return self.items.filter(type=2).latest('arm')

    @property
    def get_best_weapon(self):
        return self.items.filter(type=4).latest('atk')

    @property
    def get_best_shield(self):
        return self.items.filter(type=3).latest('defence')


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
    name = models.CharField(max_length=50, default="")
    sprite_url = models.CharField(max_length=200, default="")


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


class UserItem(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    equipped = models.BooleanField(default=False)
    on_market = models.BooleanField(default=False)
    price = models.PositiveIntegerField(default=1)