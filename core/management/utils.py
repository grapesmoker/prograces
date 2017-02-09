import json
import us
from pyexcel_ods3 import get_data
from core.models import District, State, Candidate, Contest, Vote, Party

import datetime as dt


def va_legislative_districts(electoral_data_filename, geojson_file, district_type):

    geo_data = json.load(open(geojson_file, 'r'))
    electoral_data = get_data(electoral_data_filename)

    state = State.objects.get(abbr='VA')
    if district_type == 'upper':
        va_races = electoral_data['VA_Upper']
    elif district_type == 'lower':
        va_races = electoral_data['VA_Lower']
    else:
        raise ValueError('Unknown type of district!')

    dem_party = Party.objects.get(abbr='D')
    rep_party = Party.objects.get(abbr='R')
    # district_races = [
    #     {'year': 2016,
    #      'date': dt.datetime(year=2016, month=11, day=8),
    #      'type': 'PRES',
    #      'total_vote_index': 7,
    #      'dem': {
    #          'first_name': 'Hillary',
    #          'last_name': 'Clinton'
    #      },
    #      'rep': {
    #          'first_name': 'Donald',
    #          'last_name': 'Trump'
    #      }}
    # ]

    for district in geo_data['features']:
        district_number = district['properties']['name']
        new_district = District()
        if district_type == 'upper':
            new_district.name = 'Senate District {}'.format(district_number)
        elif district_type == 'lower':
            new_district.name = 'House District {}'.format(district_number)

        print('Importing geometry for ', new_district.name)
        new_district.type = 'STU'
        if district['geometry']['type'] == 'Polygon':
            new_district.p_geometry = json.dumps(district['geometry'])
        elif district['geometry']['type'] == 'MultiPolygon':
            new_district.mp_geometry = json.dumps(district['geometry'])
        new_district.state = state

        contests = [c for c in va_races[2:] if len(c) > 0 and str(c[0]) == str(district_number)][0]
        rep = contests[2].split(' ')
        party = contests[3]
        if len(rep) == 2:
            existing = Candidate.objects.filter(first_name=rep[0], last_name=rep[1])
            first_name = rep[0]
            middle_name = ''
            last_name = rep[1]

        elif len(rep) == 3:
            existing = Candidate.objects.filter(first_name=rep[0],
                                                last_name=rep[2],
                                                middle_name=rep[1])
            first_name = rep[0]
            middle_name = rep[1]
            last_name = rep[2]

            if last_name == 'Jr.':
                last_name = rep[1] + ' Jr.'
                middle_name = ''

        if len(existing) == 0:
            new_rep = Candidate(first_name=first_name, last_name=last_name, middle_name=middle_name)
            new_rep.party = Party.objects.get(abbr=party.upper())
            new_rep.save()
        else:
            # need to fix problem of reps having same name
            new_rep = existing[0]
        new_district.representative = new_rep
        new_district.save()
        print('{} is represented by {}'.format(new_district, new_rep))



        # 2016 presidential race
        new_contest = Contest()
        new_contest.year = 2016
        new_contest.date = dt.date(year=2016, month=11, day=8)
        new_contest.type = 'PRES'
        new_contest.total_votes = contests[7]
        new_contest.state = state
        new_contest.district = new_district
        new_contest.save()

        dem, _ = Candidate.objects.get_or_create(first_name='Hillary', last_name='Clinton')
        rep, _ = Candidate.objects.get_or_create(first_name='Donald', last_name='Trump')
        dem_vote = Vote(candidate=dem, votes=int(contests[5]))
        rep_vote = Vote(candidate=rep, votes=int(contests[6]))
        dem_vote.save()
        rep_vote.save()
        new_contest.vote_set.add(dem_vote)
        new_contest.vote_set.add(rep_vote)

        new_contest.candidates.add(dem)
        new_contest.candidates.add(rep)
        new_contest.save()

        # 2012 presidential race
        new_contest = Contest(year=2012, date=dt.date(year=2012, month=11, day=6), type='PRES',
                              total_votes=contests[13], state=state, district=new_district)
        new_contest.save()
        dem, _ = Candidate.objects.get_or_create(first_name='Barack', last_name='Obama')
        rep, _ = Candidate.objects.get_or_create(first_name='Mitt', last_name='Romney')
        dem_vote = Vote(candidate=dem, votes=int(contests[11]))
        rep_vote = Vote(candidate=rep, votes=int(contests[12]))
        dem_vote.save()
        rep_vote.save()
        new_contest.vote_set.add(dem_vote)
        new_contest.vote_set.add(rep_vote)
        new_contest.candidates.add(dem)
        new_contest.candidates.add(rep)
        new_contest.save()

        # 2012 Senate race
        new_contest = Contest(year=2012, date=dt.date(year=2012, month=11, day=6), type='SEN',
                              total_votes=contests[25], state=state, district=new_district)
        new_contest.save()
        dem, _ = Candidate.objects.get_or_create(first_name='Tim', last_name='Kaine', party=dem_party)
        rep, _ = Candidate.objects.get_or_create(first_name='George', last_name='Allen', party=rep_party)
        dem_vote = Vote(candidate=dem, votes=int(contests[23]))
        rep_vote = Vote(candidate=rep, votes=int(contests[24]))
        dem_vote.save()
        rep_vote.save()
        new_contest.vote_set.add(dem_vote)
        new_contest.vote_set.add(rep_vote)
        new_contest.candidates.add(dem)
        new_contest.candidates.add(rep)
        new_contest.save()

        # 2013 Gubernatorial election
        new_contest = Contest(year=2013, date=dt.date(year=2013, month=11, day=5), type='ST',
                              total_votes=contests[31], state=state, district=new_district)
        new_contest.save()
        dem, _ = Candidate.objects.get_or_create(first_name='Terry', last_name='McAuliffe', party=dem_party)
        rep, _ = Candidate.objects.get_or_create(first_name='Ken', last_name='Cuccinelli', party=rep_party)
        dem_vote = Vote(candidate=dem, votes=int(contests[29]))
        rep_vote = Vote(candidate=rep, votes=int(contests[30]))
        dem_vote.save()
        rep_vote.save()
        new_contest.vote_set.add(dem_vote)
        new_contest.vote_set.add(rep_vote)
        new_contest.candidates.add(dem)
        new_contest.candidates.add(rep)
        new_contest.save()

        # 2013 Lieutenant Gubernatorial election
        new_contest = Contest(year=2013, date=dt.date(year=2013, month=11, day=5), type='ST',
                              total_votes=contests[37], state=state, district=new_district)
        new_contest.save()
        dem, _ = Candidate.objects.get_or_create(first_name='Ralph', last_name='Northam', party=dem_party)
        rep, _ = Candidate.objects.get_or_create(first_name='Earl', last_name='Jackson', middle_name='Walker', party=rep_party)
        dem_vote = Vote(candidate=dem, votes=int(contests[35]))
        rep_vote = Vote(candidate=rep, votes=int(contests[36]))
        dem_vote.save()
        rep_vote.save()
        new_contest.vote_set.add(dem_vote)
        new_contest.vote_set.add(rep_vote)
        new_contest.candidates.add(dem)
        new_contest.candidates.add(rep)
        new_contest.save()

        # 2013 Attorney General election
        new_contest = Contest(year=2013, date=dt.date(year=2013, month=11, day=5), type='ST',
                              total_votes=contests[43], state=state, district=new_district)
        new_contest.save()
        dem, _ = Candidate.objects.get_or_create(first_name='Mark', last_name='Herring', party=dem_party)
        rep, _ = Candidate.objects.get_or_create(first_name='Mark', last_name='Obenshain', party=rep_party)
        dem_vote = Vote(candidate=dem, votes=int(contests[41]))
        rep_vote = Vote(candidate=rep, votes=int(contests[42]))
        dem_vote.save()
        rep_vote.save()
        new_contest.vote_set.add(dem_vote)
        new_contest.vote_set.add(rep_vote)
        new_contest.candidates.add(dem)
        new_contest.candidates.add(rep)
        new_contest.save()

        # 2014 Senate election
        new_contest = Contest(year=2014, date=dt.date(year=2014, month=11, day=4), type='SEN',
                              total_votes=contests[49], state=state, district=new_district)
        new_contest.save()
        dem, _ = Candidate.objects.get_or_create(first_name='Mark', last_name='Warner', party=dem_party)
        rep, _ = Candidate.objects.get_or_create(first_name='Ed', last_name='Gillespie', party=rep_party)

        dem_vote = Vote(candidate=dem, votes=int(contests[47]))
        rep_vote = Vote(candidate=rep, votes=int(contests[48]))
        dem_vote.save()
        rep_vote.save()
        new_contest.vote_set.add(dem_vote)
        new_contest.vote_set.add(rep_vote)
        new_contest.candidates.add(dem)
        new_contest.candidates.add(rep)
        new_contest.save()