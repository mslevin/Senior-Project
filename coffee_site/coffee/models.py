from __future__ import unicode_literals

from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.question_text
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.choice_text
 
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
    parent_flavor = models.ForeignKey(PrimaryFlavor, on_delete=models.CASCADE)
    chemical_compound = models.ForeignKey(Chemical, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.name

class TertiaryFlavor(models.Model):
    parent_flavor = models.ForeignKey(SecondaryFlavor, on_delete=models.CASCADE)
    chemical_compound = models.ForeignKey(Chemical, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.name
