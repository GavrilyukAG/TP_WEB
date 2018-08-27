# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from djangosphinx.models import SphinxSearch


# ModelManager:


class QuestionManager(models.Manager):
    def newest(self):
        return self.order_by('-created')

    def hottest(self):
        return self.order_by('-rating')


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/img/', default='static/img/default_pic.png') # uploads_to='uploads/'
    rating = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return '%s' % self.user


class Tag(models.Model):
    title = models.CharField(max_length=64)

    objects = models.Manager()

    def __str__(self):
        return self.title


class Question(models.Model):
    author = models.ForeignKey(Profile)
    title = models.CharField(max_length=64)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)
    created = models.DateTimeField(auto_now_add=True)
    # answers count???

    objects = QuestionManager()
    search = SphinxSearch(index='askga')

    def __str__(self):
        return '%s Author: %s, rating:  %s' % (self.title, self.author, self.rating)


class Answer(models.Model):
    author = models.ForeignKey(Profile)
    question = models.ForeignKey(Question)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return '%s' % self.question


class Like(models.Model):
    user = models.ForeignKey(Profile)
    question = models.ForeignKey(Question)
    is_vote = models.BooleanField(default=False) # 1 - like, 0 - dislike

    objects = models.Manager()