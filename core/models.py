from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib import admin


class State(models.Model):

    state_name = models.CharField(max_length=100)
    fips = models.CharField(max_length=15)
    geometry = JSONField()


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
    geometry = JSONField()


class Precinct(models.Model):

    name = models.CharField(max_length=100)
    state = models.ForeignKey(State)
    geometry = JSONField()


class Candidate(models.Model):

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(null=True, max_length=200)


class Vote(models.Model):

    candidate = models.ForeignKey(Candidate)
    votes = models.IntegerField()


class Contest(models.Model):

    type = models.CharField(max_length=100, choices=[['MU', 'municipal'],
                                                     ['ST', 'state'],
                                                     ['FED', 'federal']])
    year = models.IntegerField()
    date = models.DateField()
    district = models.ForeignKey(District, null=True)
    state = models.ForeignKey(State)
    candidates = models.ManyToManyField(Candidate)
    votes = models.ForeignKey(Vote)

admin.site.register([State, County, City, District, Precinct, Candidate, Vote, Contest])