#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from django.db import models

class Player(models.Model):
  name = models.CharField(max_length=30)

class Competition(models.Model):
  name = models.CharField(max_length=30)

class Round(models.Model):
  competition =  models.ForeignKey(Competition)
  index = models.IntegerField()

class RoundRobin(Round):
  pass

class Elimination(Round):
  pass

class Stage(models.Model):
  round = models.ForeignKey(Round)
  name = models.CharField(max_length=30)

class Bracket(Stage):
  pass

class Group(models.Model):
  members = models.ManyToManyField(Player)

class Match(models.Model):
  stage = models.ForeignKey(Stage)
  first_player = models.ForeignKey(Player, related_name='+')
  second_player = models.ForeignKey(Player, related_name='+')
  first_score = models.IntegerField()
  second_score = models.IntegerField()

