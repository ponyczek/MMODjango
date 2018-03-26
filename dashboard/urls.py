from django.conf.urls import url

from .views import adventure, ranking, attack, equip, take_off

urlpatterns = [
    # /login
    url(r'^adventure/', adventure, name='adventure'),
    url(r'^equip/(?P<user_item_id>[0-9]+)/$', equip, name='equip'),
    url(r'^take-off/(?P<user_item_id>[0-9]+)/$', take_off, name='take_off'),
    url(r'^(?P<user_monster_id>[0-9]+)/attack/$', attack, name='attack'),
    url(r'^ranking', ranking, name='ranking'),
]
