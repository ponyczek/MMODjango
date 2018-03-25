import json
from random import randint

from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from .models import UserProfile, User, UserMonster, Monster, Item, UserItem


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
            UserMonster.objects.create(user=user, monster=monster, health_left=monster.health)
            monster_count = monster_count + 1
    user_monsters = UserMonster.objects.filter(user=user)

    user_items = UserItem.objects.filter(userprofile=user_profile, equipped=True)

    helmet = {}
    armor = {}
    weapon = {}
    shield = {}

    for ui in user_items:
        if ui.item.type == '1':
            helmet = ui.item
        elif ui.item.type == '2':
            armor = ui.item
        elif ui.item.type == '3':
            shield = ui.item
        else:
            weapon = ui.item

    context = {
        'user_profile': user_profile,
        'user_items': user_items,
        'monsters': user_monsters,
        'helmet': helmet,
        'armor': armor,
        'shield': shield,
        'weapon': weapon,
    }

    return render(request, 'dashboard/adventure.html', context)


@login_required
def ranking(request):
    # user_id = request.user.id
    users = UserProfile.objects.order_by('experience')
    # user_profile = UserProfile.objects.filter(user=user).get()
    return render(request, 'dashboard/ranking.html', {'users': users})


@login_required()
def attack(request, user_monster_id):
    level = int(request.GET['level'])
    damage = randint(0, (9 + level)) + 200  # to include damage from weapon
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
            'damage_message': dmg_msg(damage, user_monster.monster.name),
        }
    else:
        # update user.
        user_monster_to_del = UserMonster.objects.get(pk=user_monster_id)
        user = user_monster_to_del.user
        user_profile = UserProfile.objects.get(user=user)
        experience_gained = user_monster_to_del.monster.experience
        user_profile.experience = user_profile.experience + experience_gained
        gold_gained = randint(0, (user_monster_to_del.monster.gold))
        user_profile.gold = user_profile.gold + gold_gained

        # handle items drop.3
        # killed_monster = Monster.objects.get(pk=)
        # possible_items = Item.objects.filter(monster=user_monster.monster)
        # print(possible_items)
        killed_monster = Monster.objects.get(pk=user_monster.monster_id)
        loot = killed_monster.items.all()
        loot_items_str = ""

        looted_items = []

        for item in loot:
            random_val = randint(0, (10))
            if random_val + item.drop_chance > 10:
                user_item = UserItem(item=item, userprofile=user_profile)
                # user_profile.items.add(item)
                user_item.save()
                loot_items_str += item.name
                loot_items_str += ", "
                looted_items.append(item.pk)

        user_profile.save()

        user_monster_to_del.delete()

        # spawn new monster
        monster = Monster.objects.order_by('?').first()
        new_user_monster = UserMonster.objects.create(user=user, monster=monster, health_left=monster.health)
        monster_obj = model_to_dict(monster)
        user_obj = model_to_dict(user_profile)
        items = Item.objects.filter(pk__in=looted_items).values()
        # items_obj = model_to_dict(items)

        json_context = {
            'killed': True,
            'killed_monster_id': user_monster_id,
            'user_monster_id': new_user_monster.id,
            'monster': monster_obj,
            'user_profile': user_obj,
            'items': json.dumps(list(items)),
            'level': user_profile.get_level,
            'loot_message': loot_msg(loot_items_str, killed_monster.name, gold_gained),
            'damage_message': dmg_msg(damage, user_monster.monster.name),
            'experience_message': exp_msg(experience_gained, user_monster.monster.name)
        }

    # users = UserProfile.objects.order_by('experience')
    # user_profile = UserProfile.objects.filter(user=user).get()
    # return render(request, 'dashboard/ranking.html', {'users' : users})
    return JsonResponse(json_context)


def exp_msg(exp, monster):
    return str('You gained ' + str(exp) + ' experience points for killing ' + monster + '.')


def loot_msg(items, monster, gold):
    if items != "":
        return str('Loot from ' + monster + ': ' + items + '. Gold: ' + str(gold))
    else:
        return str('Gold: ' + str(gold) + ' from ' + monster + '.')


def dmg_msg(dmg, monster):
    return str('You dealt ' + str(dmg) + ' damage to ' + monster + '.')
