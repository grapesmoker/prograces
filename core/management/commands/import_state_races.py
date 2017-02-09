import json
import us

from django.core.management.base import BaseCommand
from core.models import Candidate

from core.management import utils


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('state', nargs='?')
        parser.add_argument('level', nargs='?')
        parser.add_argument('election_data_file', nargs='?')
        parser.add_argument('geojson_data_file', nargs='?')

    def handle(self, *args, **options):

        import_dispatcher = {
            'VA:upper': utils.va_legislative_districts,
            'VA:lower': utils.va_legislative_districts,
        }

        state = us.states.lookup(options['state'])
        if state:
            key = state.abbr + ':' + options['level'].lower()
            import_func = import_dispatcher[key]
            import_func(options['election_data_file'], options['geojson_data_file'], options['level'])