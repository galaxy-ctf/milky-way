from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group
from account.models import Team
import re
import uuid


class Category(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)

    def __repr__(self):
        return self.name


class Challenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    value = models.IntegerField(default=10)
    category = models.ForeignKey(Category)
    hidden = models.BooleanField(default=False)
    lesson = models.TextField(blank=True)

    def __repr__(self):
        return '<chal %r>' % self.name

    def is_solved_by(self, team):
        return Solves.objects.filter(challenge=self, team=team).count() > 0

class Hint(models.Model):
    chal = models.ForeignKey(Challenge)
    text = models.TextField()


class Flag(models.Model):
    chal = models.ForeignKey(Challenge)
    flag = models.TextField(blank=True)
    flag_is_regex = models.BooleanField(default=False)

    def validate(self, value):
        if not self.flag_is_regex:
            return self.flag == value
        else:
            return re.match(self.flag, value)


class Solves(models.Model):
    challenge = models.ForeignKey(Challenge)
    team = models.ForeignKey(Team)

    class Meta:
        # Do not allow multiple solves for single chal.
        unique_together = ('challenge', 'team')
