# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class TimeStamp(models.Model):
    """Base class containing all models common information."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Define Model as abstract."""
        abstract = True

class Book(TimeStamp):
    """Book model defined here"""
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)
    category = models.CharField(max_length=100)


    def __unicode__(self):
        return "Book Title: {}" .format(self.title)


class Issue(TimeStamp):
    book = models.ForeignKey(Book, related_name='bookissue', on_delete=models.CASCADE)
    user = models.ForeignKey(User)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return "Issue for Book: {}" .format(self.book.title)
