import os
import django

import requests
from requests.api import get
from main.models import Movie , Genre, NewPeople , Person
from django.db import transaction
import json


def run():
    
    

        results_movie_credits=requests.get('https://api.themoviedb.org/3/person/popular?api_key=2b5b38b211b06bb26131ced7fca692bc&language=en-US&language=en-US').json()
        for page_people in range(1,results_movie_credits['total_pages']+1):
         page_results_people = requests.get('https://api.themoviedb.org/3/person/popular?api_key=2b5b38b211b06bb26131ced7fca692bc&language=en-US&page='+f'{page_people}').json()
        
         print(page_people)
         with transaction.atomic():
          for person_data in page_results_people['results']:
           person_exists =  Person.objects.filter(id=person_data['id']).first()
           if person_exists == None:
             NewPeople.objects.update_or_create(id=person_data['id'],defaults={"name":person_data['name']})
           Person.objects.update_or_create(
            id=person_data['id'],

            defaults={
                "name" : person_data['name'],
                "popularity" : person_data['popularity'],
                "profile_path" : person_data['profile_path'],
                "gender" : person_data['gender'],
            }
        )
          
           #print (person.movies)

        