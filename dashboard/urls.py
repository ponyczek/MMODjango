from django.conf.urls import url
from .views import adventure, ranking

urlpatterns = [
    # /login
    url(r'^adventure', adventure, name='adventure' ),
    url(r'^ranking', ranking, name='ranking' ),
]
