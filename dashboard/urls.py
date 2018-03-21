from django.conf.urls import url

from .views import adventure, ranking, attack

urlpatterns = [
    # /login
    url(r'^adventure/', adventure, name='adventure'),
    url(r'^(?P<user_monster_id>[0-9]+)/attack/$', attack, name='attack'),
    url(r'^ranking', ranking, name='ranking'),
]
