from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    experience = models.PositiveIntegerField(default=0)
    gold = models.PositiveIntegerField(default=0)

    # @property
    # def get_level(self):
    #
    #     if self.end_date > timezone.now() and timezone.now() > self.start_date:
    #         return True
    #     else:
    #         return False

    def __unicode__(self):
        return self.user.username


