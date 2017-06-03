import os
import re
import uuid
import requests
import json
import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)

from django.core.management.base import BaseCommand
from account.models import Team
from django.conf import settings
from django.utils import timezone


class Command(BaseCommand):
    help = 'output metadata stuff'

    def handle(self, *args, **options):
        external_data = requests.get('http://rancher-metadata/latest/stacks', headers={'Accept': 'application/json'}).json()
        output = {}
        for proj in external_data:
            if proj['name'] != 'galaxy':
                continue
            for service in proj['services']:

                for container in service['containers']:
                    if 'org.galaxians.ctf.team.name' not in container['labels']:
                        continue

                    ip = container['primary_ip']
                    team_id = int(container['labels']['org.galaxians.ctf.team.id'])
                    team_name = container['labels']['org.galaxians.ctf.team.name']
                    try:
                        team = Team.objects.get(name=team_name)
                        output[ip] = str(team.admin_password)
                    except:
                        pass
        print(json.dumps(output))
