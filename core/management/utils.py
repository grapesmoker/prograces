import json
import us
from pyexcel_ods3 import get_data
from core.models import District


def va_senate(electoral_data_filename, geojson_file):

    geo_data = json.load(open(geojson_file, 'r'))

    for district in geo_data['features']:
        district_number = district['properties']['name']
