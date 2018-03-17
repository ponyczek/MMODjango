from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import UserProfile, User


# Create your views here.
@login_required
def adventure(request):
    # user_id = request.user.id
    user = User.objects.filter(pk=request.user.id)
    user_profile = UserProfile.objects.filter(user=user).get()
    return render(request, 'dashboard/adventure.html', {'user_profile': user_profile})

@login_required
def ranking(request):
    # user_id = request.user.id
    users = UserProfile.objects.order_by('experience')
    # user_profile = UserProfile.objects.filter(user=user).get()
    return render(request, 'dashboard/ranking.html', {'users' : users})