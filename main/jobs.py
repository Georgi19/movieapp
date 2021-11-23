from django.conf import settings
import os
import django

import requests
from requests.api import get
from main.models import Movie , Genre, NewMovies , Person, NewPeople
from django.db import transaction
import json

def add_cast():
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

def add_details_people():
 n=0
 people = NewPeople.objects.all()
   
 while n<people.count():
     with transaction.atomic():
        
        for new_person in people[n:n+500]:
            result = requests.get('https://api.themoviedb.org/3/person/'+f'{new_person.id}'+'?api_key=2b5b38b211b06bb26131ced7fca692bc&language=en-US').json()
            
            n+=1
            print(n)
            person = Person.objects.get(id = new_person.id)
            try:
             person.biography = result['biography'] 
             person.birthday = result['birthday']
             person.place_of_birth = result['place_of_birth']
             person.known_for_department = result['known_for_department']
             person.save(update_fields=['biography','birthday','place_of_birth','known_for_department'])
            except: pass
            if n>=people.count():break


def add_genres():
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

def update_movies_db():
      
        results_movie=requests.get('https://api.themoviedb.org/3/discover/movie?api_key=2b5b38b211b06bb26131ced7fca692bc').json()
        for page_movie in range(1,results_movie['total_pages']+1):
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
def update_people_db():
    
    

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

def delete_new():
   count_nm = NewMovies.objects.count()
   count_p = NewPeople.objects.count()

   NewMovies.objects.all().delete()
   NewPeople.objects.all().delete()

   print("Added movies : " ,count_nm)
   print("Added people : " ,count_p)
           
