from django.core.management.base import BaseCommand
from core.models import Candidate, Vote, State, District, Contest


class Command(BaseCommand):

    def handle(self, *args, **options):

        print('Deleting everything from the database!')

        for c in Candidate.objects.all():
            c.delete()
        for v in Vote.objects.all():
            v.delete()
        for c in Contest.objects.all():
            c.delete()
        for d in District.objects.all():
            d.delete()