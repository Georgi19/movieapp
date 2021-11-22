import os
import django

import requests
from requests.api import get, request
from main.models import Movie , Genre, NewPeople , Person, NewMovies
from django.db import transaction
import json

def run():
   count_nm = NewMovies.objects.count()
   count_p = NewPeople.objects.count()

  # NewMovies.objects.all().delete()
   #NewPeople.objects.all().delete()

   print("Added movies : " ,count_nm)
   print("Added people : " ,count_p)

   
      