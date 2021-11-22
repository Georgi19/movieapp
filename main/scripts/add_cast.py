import os
import django

import requests
from requests.api import get, request
from main.models import Movie , Genre , Person, NewMovies
from django.db import transaction
import json

def run():
    n=0
    new_movies = NewMovies.objects.all()
  
    
    while n<new_movies.count():
        with transaction.atomic():
        
         for new_movie in new_movies[n:n+500]:
          n+=1
          print(n)
          request = requests.get('https://api.themoviedb.org/3/movie/'+f'{new_movie.id}''/credits?api_key=2b5b38b211b06bb26131ced7fca692bc&language=en-US').json()
          movie = Movie.objects.get(id=new_movie.id)
          for result in request['cast']:
            person = Person.objects.filter(id=result['id']).first()
            if person != None:
              movie.people.add(person)
              person.movies.add(movie)
         if n>=new_movies.count():break
        print(n)
          
    