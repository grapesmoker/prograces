import json
import us

from django.core.management.base import BaseCommand
from core.models import Candidate, Party


class Command(BaseCommand):

    def handle(self, *args, **options):

        dem, _ = Party.objects.get_or_create(name='Democratic Party', abbr='D')
        rep, _ = Party.objects.get_or_create(name='Republican Party', abbr='R')

        obama = Candidate(first_name='Barack', last_name='Obama', middle_name='Hussein')
        romney = Candidate(first_name='Mitt', last_name='Romney')
        clinton = Candidate(first_name='Hillary', last_name='Clinton', middle_name='Rodham')
        trump = Candidate(first_name='Donald', last_name='Trump', middle_name='John')

        obama.party = dem
        romney.party = rep
        clinton.party = dem
        trump.party = rep

        obama.save()
        romney.save()
        clinton.save()
        trump.save()