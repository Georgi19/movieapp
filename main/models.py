from typing import Text
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields import BooleanField, CharField, TextField
from django.contrib.auth.models import User
from django.db.models.fields.related import ManyToManyField, OneToOneField
from allauth.account.signals import user_signed_up


# Create your models here.


class Genre(models.Model):

    id = models.IntegerField(primary_key=True,unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Movie(models.Model):

    id = models.IntegerField(primary_key=True,unique=True)
    title = models.CharField(max_length=2000)
    popularity = models.DecimalField(max_digits=10, decimal_places=3)
    poster_path = models.CharField(max_length=2000,null=True)
    backdrop_path = models.CharField(max_length=2000,null=True)
    vote_avg = models.DecimalField(max_digits=10, decimal_places=3)
    vote_count = models.IntegerField()
    adult = models.BooleanField(default=False)
    release_date = models.CharField(max_length=200)
    overview = models.TextField(default='N/A')
    genres = models.ManyToManyField(Genre)
    people = models.ManyToManyField("Person")

    def __str__(self):
        return self.title

class Person(models.Model):

    id = models.IntegerField(primary_key=True,unique=True)
    name = models.CharField(max_length=200)
    movies = models.ManyToManyField(Movie)
    gender = models.IntegerField()
    popularity = models.DecimalField(max_digits=10, decimal_places=3)
    profile_path = models.CharField(max_length=2000,null=True)

    birthday = models.CharField(max_length=200,default='N/A',null=True)
    biography = models.TextField(default='N/A',null=True)
    place_of_birth = models.TextField(max_length=200,default='N/A',null=True)
    known_for_department = models.CharField(max_length=100,default='N/A',null=True)

    def __str__(self):
        return self.name
class NewMovies(models.Model):
    
    title = models.CharField(max_length=2000)
    id = models.IntegerField(primary_key=True,unique=True)
     
    def __str__(self):
        return self.name
class NewPeople(models.Model):
    name = models.CharField(max_length=200)
    id = models.IntegerField(primary_key=True,unique=True)
     
    def __str__(self):
        return self.name
class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    seen_movies = models.ManyToManyField(Movie)
    profile_pic = models.ImageField(default="default_profile.png",null=True,blank=True)
    
   


User = get_user_model()

def user_signed_up_receiver(request,user, **kwargs):
    movie_list = Profile(user=user)
    movie_list.save()

user_signed_up.connect(user_signed_up_receiver,sender=User)
