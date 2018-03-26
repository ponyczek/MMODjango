import json
from random import randint

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, User, UserMonster, Monster, UserItem


# Create your views here.
@login_required
def adventure(request):
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

    user_items = UserItem.objects.filter(userprofile=user_profile, on_market=False)

    helmet = {}
    armor = {}
    weapon = {}
    shield = {}

    for ui in user_items:
        if ui.equipped:
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
    users = UserProfile.objects.order_by('-experience')
    return render(request, 'dashboard/ranking.html', {'users': users})


@login_required()
def attack(request, user_monster_id):
    user_monster = UserMonster.objects.get(pk=user_monster_id)
    user_profile = UserProfile.objects.get(user=user_monster.user)

    extra_dmg = 0
    try:
        user_item = UserItem.objects.get(userprofile=user_profile, equipped=True, item__type=4)
        extra_dmg = user_item.item.atk
    except UserItem.DoesNotExist:
        extra_dmg = 0
    level = int(request.GET['level'])
    damage = randint(0, (9 + level)) + (extra_dmg*2)  # to include damage from weapon
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
        user_monster_to_del = user_monster
        user = user_monster_to_del.user
        experience_gained = user_monster_to_del.monster.experience
        user_profile.experience = user_profile.experience + experience_gained
        gold_gained = randint(0, (user_monster_to_del.monster.gold))
        user_profile.gold = user_profile.gold + gold_gained

        killed_monster = Monster.objects.get(pk=user_monster.monster_id)
        loot = killed_monster.items.all()
        loot_items_str = ""

        looted_items = []

        for item in loot:
            random_val = randint(0, (10))
            if random_val + item.drop_chance > 10:
                user_item = UserItem(item=item, userprofile=user_profile)
                user_item.save()
                loot_items_str += item.name
                loot_items_str += ", "
                looted_items.append(user_item.pk)

        user_profile.save()

        user_monster_to_del.delete()

        # spawn new monster
        monster = Monster.objects.order_by('?').first()
        new_user_monster = UserMonster.objects.create(user=user, monster=monster, health_left=monster.health)
        monster_obj = model_to_dict(monster)
        user_obj = model_to_dict(user_profile)
        items = UserItem.objects.filter(userprofile=user_profile)
        serialised_items = serialise_user_items(items)

        json_context = {
            'killed': True,
            'killed_monster_id': user_monster_id,
            'user_monster_id': new_user_monster.id,
            'monster': monster_obj,
            'user_profile': user_obj,
            'items': json.dumps(serialised_items),
            'level': user_profile.get_level,
            'loot_message': loot_msg(loot_items_str, killed_monster.name, gold_gained),
            'damage_message': dmg_msg(damage, user_monster.monster.name),
            'experience_message': exp_msg(experience_gained, user_monster.monster.name)
        }

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


def serialise_user_items(items):
    serialised_items = []
    for item in items:
        serialised_items.append({
            'id': item.pk,
            'item': model_to_dict(item.item),
        })
    return serialised_items

@login_required()
def equip(request, user_item_id):
    user_item = UserItem.objects.get(pk=user_item_id)
    try:
        equipped_item_to_replace = UserItem.objects.get(equipped=True, item__type=user_item.item.type)
    except UserItem.DoesNotExist:
        equipped_item_to_replace = None
    if (equipped_item_to_replace):
        equipped_item_to_replace.equipped = False
        equipped_item_to_replace.save()
    user_item.equipped = True
    user_item.save()
    return HttpResponseRedirect(reverse('dashboard:adventure'))


@login_required()
def take_off(request, user_item_id):
    user_item = UserItem.objects.get(pk=user_item_id)
    user_item.equipped = False
    user_item.save()
    return HttpResponseRedirect(reverse('dashboard:adventure'))

@csrf_exempt
@login_required()
def sell_item(request, user_item_id):
    user_item = UserItem.objects.get(pk=user_item_id)
    user_item.on_market = True
    user_item.price = request.POST['price']
    user_item.save()
    return JsonResponse({'item_to_sell': user_item.pk})


@login_required()
def market(request):
    user = User.objects.get(pk=request.user.id)
    user_profile = UserProfile.objects.get(user=user)
    items_to_buy = UserItem.objects.all().exclude(userprofile=user_profile)
    return render(request, 'dashboard/market.html', {'items': items_to_buy, 'user_profile': user_profile})

@login_required()
def buy_item(request, user_item_id):
    user_item = UserItem.objects.get(pk=user_item_id)

    if user_item.on_market:
        buyer = UserProfile.objects.get(user_id=request.user.id)
        seller = user_item.userprofile
        if buyer.gold >= user_item.price:
            seller.gold = seller.gold + user_item.price
            buyer.gold = buyer.gold - user_item.price
            user_item.userprofile = buyer
            user_item.on_market = False
            user_item.save()
            seller.save()
            buyer.save()
            user = User.objects.get(pk=request.user.id)
            user_profile = UserProfile.objects.get(user=user)
            items_to_buy = UserItem.objects.all().exclude(userprofile=user_profile)
            return render(request, 'dashboard/market.html', {'items': items_to_buy, 'user_profile': user_profile, 'success': 'Congratulations! Transaction was successful.'})
        else:
            user = User.objects.get(pk=request.user.id)
            user_profile = UserProfile.objects.get(user=user)
            items_to_buy = UserItem.objects.all().exclude(userprofile=user_profile)
            return render(request, 'dashboard/market.html', {'items': items_to_buy, 'user_profile': user_profile, 'error': 'Not enough gold.'})
    else:
        user = User.objects.get(pk=request.user.id)
        user_profile = UserProfile.objects.get(user=user)
        items_to_buy = UserItem.objects.all().exclude(userprofile=user_profile)
        return render(request, 'dashboard/market.html',
                      {'items': items_to_buy, 'user_profile': user_profile, 'error': 'Item no longer on the market'})

