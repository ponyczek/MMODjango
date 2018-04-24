#render library for returning views to the browser
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pusher import Pusher
from dashboard.models import UserProfile
from os import environ
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

pusher = Pusher(app_id=environ.get('PUSHER_ID'), key=environ.get('PUSHER_KEY'), secret=environ.get('PUSHER_SECRET'), cluster='eu')
#login required to access this page. will redirect to admin login page.
@login_required(login_url='/admin/login/')
def chat(request):
    return render(request,"chat.html")

@csrf_exempt
def broadcast(request):
    user_profile = UserProfile.objects.get(pk=request.user.id)
    level = user_profile.get_level
    pusher.trigger(u'a_channel', u'an_event', {u'name': request.user.username, u'level': str(level), u'message': request.POST['message']})
    return HttpResponse("done")