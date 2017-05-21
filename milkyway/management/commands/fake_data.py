from django.core.management.base import BaseCommand
from account.models import Account, Team
from milkyway.models import Challenge, Hint, Team, Category, Flag
import lorem
import datetime
import random


class Command(BaseCommand):
    help = 'Generate some fake data.'

    def handle(self, *args, **options):
        categories = ['intro', 'dev', 'bio', 'sec', 'galaxy']
        categories_o = []
        for cat in categories:
            obj, _ = Category.objects.get_or_create(name=cat)
            categories_o.append(obj)

        for i in range(50):
            name = lorem.sentence()
            obj, _ = Challenge.objects.get_or_create(
                name=name[0:name.index(' ')],
                description=lorem.text(),
                value=random.randint(1, 100),
                category=random.choice(categories_o),
            )

            f, _ = Flag.objects.get_or_create(
                chal=obj,
                flag='^a',
                flag_is_regex=True
            )

            for i in range(random.randint(0, 3)):
                Hint.objects.create(
                    chal=obj,
                    text=lorem.paragraph()
                )
