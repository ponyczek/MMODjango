from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import UserProfile, User, UserMonster, Monster


# Create your views here.
@login_required
def adventure(request):
    # user_id = request.user.id
    user = User.objects.get(pk=request.user.id)
    user_profile = UserProfile.objects.filter(user=user).get()
    #get all the monsters that belong to user
    user_monsters = UserMonster.objects.filter(user=user)
    context = {'user_profile': user_profile }
    if(len(user_monsters)<3):
        monster_count = len(user_monsters)
        while monster_count < 3:
            monster = Monster.objects.order_by('?').first()
            # user_monster = UserMonster()
            # user_monster.user = user
            # user_monster.monster = monster
            # user_monster.health_left = monster.health
            # user = User.objects.filter(pk=request.user.id)
            UserMonster.objects.create(user=user, monster= monster, health_left=monster.health)
            monster_count = monster_count + 1
    user_monsters = UserMonster.objects.filter(user=user)

    return render(request, 'dashboard/adventure.html', {'user_profile': user_profile, 'monsters': user_monsters})

@login_required
def ranking(request):
    # user_id = request.user.id
    users = UserProfile.objects.order_by('experience')
    # user_profile = UserProfile.objects.filter(user=user).get()
    return render(request, 'dashboard/ranking.html', {'users' : users})