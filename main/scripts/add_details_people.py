import os
import django

import requests
from requests.api import get
from main.models import Movie , Genre , Person,NewPeople
from django.db import transaction
import json


def run():
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
      
      
            
        
         
       
          
      