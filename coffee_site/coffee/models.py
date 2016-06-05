from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
        return self.choice_text

class SurveyResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    completed = models.DateTimeField('Completed')
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return str(self.user) + " " + str(self.completed)

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    result = models.ForeignKey(SurveyResult)
    question = models.ForeignKey(Question, blank=True, null=True)
    answer = models.ForeignKey(Choice)
    def __str__(self):
        return self.question.question_text



class Roaster(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True, upload_to='roasters')
    def __str__(self):
        return self.name

class Coffee(models.Model):
    roaster = models.ForeignKey(Roaster)
    origin = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=100, blank=True, null=True)
    varietal = models.CharField(max_length=100, blank=True, null=True)
    process = models.CharField(max_length=100, blank=True, null=True)
    tasting_notes = models.CharField(max_length=500, blank=True, null=True)
    descriptors = models.CharField(max_length=500, blank=True, null=True)
    roast_date = models.DateField()
    brew_date = models.DateField()
    test_date = models.DateField()
    def __str__(self):
        return self.name

class GCMSResult(models.Model):
    coffee = models.ForeignKey(Coffee)
    def __str__(self):
        return self.coffee.name

class Chemical(models.Model):
    result = models.ForeignKey(GCMSResult, null=True)
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    #detectable_ppm = models.IntegerField()
    #detectable_substance = models.CharField(max_length=200)
    primary_sensory = models.CharField(max_length=500, default="", blank=True, null=True)
    secondary_sensory = models.CharField(max_length=500, default="", blank=True, null=True)
    descriptors = models.CharField(max_length=200, default="", null=True, blank=True)
    def __str__(self):
        return self.name

class BrewMethod(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Brew(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    method = models.ForeignKey(BrewMethod)
    coffee = models.ForeignKey(Coffee)
    date = models.DateTimeField(default=timezone.now)
    grams_coffee = models.IntegerField()
    grams_water = models.IntegerField()
    water_temp = models.IntegerField(blank=True, null=True)
    grind = models.CharField(max_length=200, blank=True, null=True)
    duration = models.IntegerField('seconds', blank=True, null=True)
    # just add all the tasting info here. brew--tasting will always be 1-10
    strength = models.IntegerField(default=-1)
    extraction = models.IntegerField(default=-1)
    acidity = models.IntegerField(default=-1)
    overall_score = models.IntegerField(default=-1)
    aftertaste = models.IntegerField(default=-1)
    body = models.IntegerField(default=-1)
    descriptors = models.CharField(max_length=500, default="")
    def __str__(self):
        return self.method.name + " " + str(self.date)
    def totalScore(self):
        return self.strength + self.extraction + self.acidity + self.overall_score + self.aftertaste + self.body

class Tasting(models.Model):
    id = models.AutoField(primary_key=True)
    initial_score = models.IntegerField()
    # aroma
    # body
    # flavor
    # acidity
    # sweetness
    # aftertaste
    # many of these can be 1-10 scale, with some other notes/characteristics

class UserData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    recommendation = models.ForeignKey(Coffee, blank=True, null=True)
    time = models.DateTimeField(default=timezone.now, null=True)
    def __str__(self):
        return self.user.username + " " + str(self.time)
