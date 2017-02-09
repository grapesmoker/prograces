import json
import us

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos.collections import MultiPolygon
from core.models import State


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('states_json_file', nargs='?')

    def handle(self, *args, **options):

        data = json.load(open(options['states_json_file'], 'r'))
        for state in data['features']:
            st = us.states.lookup(state['properties']['NAME'])
            print('Loading geometry for', st.name)
            new_state = State()
            new_state.abbr = st.abbr
            new_state.fips = st.fips
            if state['geometry']['type'] == 'Polygon':
                new_state.p_geometry = json.dumps(state['geometry'])
            elif state['geometry']['type'] == 'MultiPolgyon':
                new_state.mp_geometry = json.dumps(state['geometry'])
            new_state.state_name = st.name
            new_state.save()