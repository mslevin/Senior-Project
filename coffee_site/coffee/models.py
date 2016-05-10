from __future__ import unicode_literals

from django.db import models
from django.conf import settings

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
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Choice)
    def __str__(self):
        return self.question.question_text

class Chemical(models.Model):
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    detectable_ppm = models.IntegerField()
    detectable_substance = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class PrimaryFlavor(models.Model):
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.name

class SecondaryFlavor(models.Model):
    parent_flavor = models.ForeignKey(PrimaryFlavor)
    chemical_compound = models.ForeignKey(Chemical, blank=True, null=True)
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.name

class TertiaryFlavor(models.Model):
    parent_flavor = models.ForeignKey(SecondaryFlavor)
    chemical_compound = models.ForeignKey(Chemical)
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.name

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
    roast_date = models.DateField()
    brew_date = models.DateField()
    test_date = models.DateField()
    def __str__(self):
        return self.name
