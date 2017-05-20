from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group
import re
import uuid


class Challenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    value = models.IntegerField(default=10)
    category = models.CharField(max_length=80)
    hidden = models.BooleanField(default=False)

    def __repr__(self):
        return '<chal %r>' % self.name


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
    team = models.ForeignKey(Group)
