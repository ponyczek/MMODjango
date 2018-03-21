from random import randint

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
import json
from .models import UserProfile, User, UserMonster, Monster
from django.core.serializers import serialize
from django.forms.models import model_to_dict


# Create your views here.
@login_required
def adventure(request):
    # user_id = request.user.id
    user = User.objects.get(pk=request.user.id)
    user_profile = UserProfile.objects.filter(user=user).get()
    # get all the monsters that belong to user
    user_monsters = UserMonster.objects.filter(user=user)
    context = {'user_profile': user_profile}
    if (len(user_monsters) < 3):
        monster_count = len(user_monsters)
        while monster_count < 3:
            monster = Monster.objects.order_by('?').first()
            # user_monster = UserMonster()
            # user_monster.user = user
            # user_monster.monster = monster
            # user_monster.health_left = monster.health
            # user = User.objects.filter(pk=request.user.id)
            UserMonster.objects.create(user=user, monster=monster, health_left=monster.health)
            monster_count = monster_count + 1
    user_monsters = UserMonster.objects.filter(user=user)

    return render(request, 'dashboard/adventure.html', {'user_profile': user_profile, 'monsters': user_monsters})


@login_required
def ranking(request):
    # user_id = request.user.id
    users = UserProfile.objects.order_by('experience')
    # user_profile = UserProfile.objects.filter(user=user).get()
    return render(request, 'dashboard/ranking.html', {'users': users})


@login_required()
def attack(request, user_monster_id):
    level = int(request.GET['level'])
    damage = randint(0, (9 + level))  # to include damage from weapon
    print(damage)
    user_monster = UserMonster.objects.get(pk=user_monster_id)
    json_context = {}
    current_monster_health = user_monster.health_left
    if (current_monster_health - damage > 0):
        user_monster.health_left = current_monster_health - damage
        user_monster.save()
        json_context = {
            'killed': False,
            'user_monster_id': user_monster_id,
            'health_left': user_monster.health_left,
            'percentage': user_monster.get_health_percentage,
            'damage_message': 'you dealt x damage to x',
        }
    else:
        user_monster_to_del = UserMonster.objects.get(pk=user_monster_id)
        user = user_monster_to_del.user
        user_monster_to_del.delete()
        monster = Monster.objects.order_by('?').first()
        new_user_monster = UserMonster.objects.create(user=user, monster=monster, health_left=monster.health)
        monster_obj = model_to_dict(monster)
        json_context = {
            'killed': True,
            'killed_monster_id': user_monster_id,
            'user_monster_id': new_user_monster.id,
            'monster': monster_obj,
            # 'health_left': user_monster.health_left,
            # 'percentage': user_monster.get_health_percentage,
            'loot_message': 'you looted x',
            'damage_message': 'you dealt x damage to x',
            'experience_message': 'you gained x experience'
        }
        # print('test')
        # draw items
        # update user experience
        # add user gold
        # destroy monster
        # create user_monster.

    # users = UserProfile.objects.order_by('experience')
    # user_profile = UserProfile.objects.filter(user=user).get()
    # return render(request, 'dashboard/ranking.html', {'users' : users})
    return JsonResponse(json_context)
    # attack monster
    # attack monster
    # attack monster
