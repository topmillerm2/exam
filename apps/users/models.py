from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField(auto_now=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "<User object: {} {} {} {} {} >".format(self.name, self.alias, self.email,self.password, self.dob)

class Quote(models.Model):
    quoted_by = models.CharField(max_length=255)
    message = models.TextField()
    poster = models.ForeignKey(User, related_name="my_quotes")
    quotes = models.ManyToManyField(User, related_name="quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "<Quote object: {} {}>".format(self.quoted_by, self.message)