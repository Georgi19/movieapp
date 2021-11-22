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
         movie = Movie.objects.get(id=new_movie.id)
         request_genres = requests.get('https://api.themoviedb.org/3/movie/'+f'{new_movie.id}''?api_key=2b5b38b211b06bb26131ced7fca692bc&language=en-US').json()
         for genre_id in request_genres['genres']:
            genre = Genre.objects.filter(id=genre_id['id']).first()
            movie.genres.add(genre)
         if n>=new_movies.count():break
        
    