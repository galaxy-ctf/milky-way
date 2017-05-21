from django.core.management.base import BaseCommand
from account.models import Account, Team
from milkyway.models import Challenge, Hint, Team, Category, Flag
import datetime
import yaml


class Command(BaseCommand):
    help = 'Export data to yaml file'

    def handle(self, *args, **options):
        data = {'chals': []}
        for category in Category.objects.all():
            chal_data = {
                'name': category.name,
                'desc': category.description,
                'chals': []
            }

            for challenge in category.challenge_set.all():
                c = {
                    'id': challenge.id,
                    'name': challenge.name,
                    'desc': challenge.description,
                    'value': challenge.value,
                    'hints': [hint.text for hint in challenge.hint_set.all()],
                    'flags': [
                        {'flag': flag.flag, 'regex': flag.flag_is_regex}
                        for flag in challenge.flag_set.all()
                    ],
                }
                chal_data['chals'].append(c)

            data['chals'].append(chal_data)
        print(yaml.dump(data, default_flow_style=False))
