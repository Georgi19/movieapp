from django.contrib import admin
from .models import  Genre, Movie, NewMovies, Person, Profile

# Register your models here.



admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Person)
admin.site.register(NewMovies)
admin.site.register(Profile)
