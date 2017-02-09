from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib import admin
from django.contrib.gis.db import models as geomodels


class State(models.Model):

    state_name = models.CharField(max_length=100)
    abbr = models.CharField(max_length=2)
    fips = models.CharField(max_length=15)
    mp_geometry = geomodels.MultiPolygonField(null=True)
    p_geometry = geomodels.PolygonField(null=True)

    @property
    def geometry(self):
        if self.mp_geometry and not self.p_geometry:
            return self.mp_geometry
        elif self.p_geometry and not self.mp_geometry:
            return self.p_geometry
        else:
            return None


class County(models.Model):

    county_name = models.CharField(max_length=200)
    state = models.ForeignKey(State)
    fips = models.CharField(max_length=15)
    geometry = JSONField()


class City(models.Model):

    city_name = models.CharField(max_length=200)
    state = models.ForeignKey(State)
    county = models.ForeignKey(County)
    geometry = JSONField()


class District(models.Model):

    name = models.CharField(max_length=100)
    state = models.ForeignKey(State)
    type = models.CharField(max_length=100, choices=[['STL', 'state upper'],
                                                     ['STU', 'state lower'],
                                                     ['FED', 'congressional']])
    mp_geometry = geomodels.MultiPolygonField(null=True)
    p_geometry = geomodels.PolygonField(null=True)

    representative = models.ForeignKey('Candidate', null=True)

    @property
    def geometry(self):
        if self.mp_geometry and not self.p_geometry:
            return self.mp_geometry
        elif self.p_geometry and not self.mp_geometry:
            return self.p_geometry
        else:
            return None

    def __str__(self):
        return self.name


class Precinct(models.Model):

    name = models.CharField(max_length=100)
    state = models.ForeignKey(State)
    geometry = JSONField()


class Party(models.Model):

    name = models.CharField(max_length=100)
    abbr = models.CharField(max_length=5)


class Candidate(models.Model):

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(null=True, max_length=200)
    party = models.ForeignKey(Party, null=True)

    def __str__(self):
        return '{}, {} {} ({})'.format(self.last_name, self.first_name, self.middle_name or '', self.party.abbr)


class Vote(models.Model):

    candidate = models.ForeignKey(Candidate)
    votes = models.IntegerField()
    contest = models.ForeignKey('Contest', null=True)

    def __str__(self):
        return '{} ({})'.format(self.candidate, self.votes)


class Contest(models.Model):

    type = models.CharField(max_length=100, choices=[['MU', 'municipal'],
                                                     ['ST', 'state'],
                                                     ['FED', 'federal'],
                                                     ['PRES', 'presidential'],
                                                     ['SEN', 'senate']])
    year = models.IntegerField()
    date = models.DateField()
    district = models.ForeignKey(District, null=True)
    state = models.ForeignKey(State)
    candidates = models.ManyToManyField(Candidate)
    total_votes = models.IntegerField()

    def __str__(self):
        votes = [v for v in self.vote_set.all()]
        return '<Race on {} between {} ({}) and {} ({}), total votes cast: {}>'.format(
            self.date, votes[0].candidate, votes[0].votes,
            votes[1].candidate, votes[1].votes,
            self.total_votes
        )

admin.site.register([State, County, City, District, Precinct, Candidate, Vote, Contest])