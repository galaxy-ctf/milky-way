from django.core.management.base import BaseCommand
from account.models import Account, Team
from milkyway.models import Challenge, Hint, Team, Category, Flag
import datetime
import yaml


class Command(BaseCommand):
    help = 'Load data from yaml file'

    def add_arguments(self, parser):
        parser.add_argument('dataset', type=str)

    def handle(self, *args, **options):
        with open(options['dataset'], 'r') as handle:
            data = yaml.load(handle)

        Category.objects.all().delete()

        for cat in data['chals']:
            category = Category.objects.create(
                name=cat['name'],
                description=cat['desc']
            )
            chals = []
            for chal in cat['chals']:
                chal_data = {
                    'id': chal['id'],
                    'name': chal['name'],
                    'description': chal['desc'],
                    'value': chal['value'],
                    'category': category,
                    'lesson': chal.get('lesson', ''),
                }
                c = Challenge.objects.create(**chal_data)
                for hint in chal['hints']:
                    Hint.objects.create(text=hint, chal=c)
                c.save()

                for flag in chal['flags']:
                    Flag.objects.create(
                        chal=c,
                        flag=flag['flag'],
                        flag_is_regex=flag['regex'],
                    )
