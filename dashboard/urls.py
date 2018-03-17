from django.conf.urls import url
from .views import adventure

urlpatterns = [
    # /login
    url(r'^adventure', adventure, name='adventure' ),
]
