import os
import django

import requests
from requests.api import get
from main.models import Movie , Genre , Person, NewMovies
from django.db import transaction
import json


def run():

    
        
        results_movie=requests.get('https://api.themoviedb.org/3/discover/movie?api_key=2b5b38b211b06bb26131ced7fca692bc').json()
        for page_movie in range(1,2):
         page_results_movie = requests.get('https://api.themoviedb.org/3/discover/movie?page='+f'{page_movie}'+'&api_key=2b5b38b211b06bb26131ced7fca692bc').json()
         with transaction.atomic():
          for item_movie in page_results_movie['results']:
            
            release_date = "N/A" 
            try: release_date = item_movie['release_date']
            except KeyError: pass
            print(page_movie)
            movie_exists =  Movie.objects.filter(id=item_movie['id']).first()
            if movie_exists == None:
                NewMovies.objects.update_or_create(id=item_movie['id'],defaults={"title":item_movie['title']})
            Movie.objects.update_or_create(
            id=item_movie['id'],

            defaults={
                "title" : item_movie['title'],
                "popularity" : item_movie['popularity'],
                "poster_path" : item_movie['poster_path'],
                "backdrop_path" : item_movie['backdrop_path'],
                "vote_avg" : item_movie['vote_average'],
                "vote_count" : item_movie['vote_count'],
                "adult" : item_movie['adult'],
                "overview" : item_movie['overview'],
                "release_date" : release_date
            }
          )
           
   

    
                
            

