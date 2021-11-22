from django.core import paginator
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from requests.api import get
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from main.forms import ProfileForm
from .models import Movie ,Genre , Person, Profile
from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger, Paginator
import requests
import json
from django.http import Http404
from django.db.models import Q, query
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.contrib.auth import get_user_model


discover_api_url = ("https://api.themoviedb.org/3/discover/movie?")

images_url = "https://image.tmdb.org/t/p/w1280"
api_key = "2b5b38b211b06bb26131ced7fca692bc"



def catalogue(request):
  movie_data = Movie.objects.order_by('-popularity')
  paginator = Paginator(movie_data, 20)
  page = request.GET.get('page')
 
  page_number = page

 
  page_obj = paginator.get_page(page_number)
  return render(request,"main/movie_catalogue.html",{"data":page_obj})

def movie_info(request, id):
  try:
    movie = Movie.objects.get(id=id)
    people = movie.people.all()
  except Movie.DoesNotExist:
    raise Http404("movie does not exist")

  if request.user.is_authenticated:
   seen = request.user.profile.seen_movies.filter(id=id).first()
  else: seen = None

  if request.method == 'DELETE':
    
    request.user.profile.seen_movies.remove(movie)
    
  if request.method == 'POST':
    
    request.user.profile.seen_movies.add(movie)
    
  return render(request,"main/movie_info.html",{'movie':movie,'people':people.order_by('-popularity'),'seen': seen is not None})

def full_cast(request,id):
  movie = Movie.objects.get(id=id)
  people = movie.people.all()
  return render(request,"main/full_cast.html",{'people':people, "title":movie.title})

def people(request):
  people = Person.objects.all().order_by('-popularity')
 
  paginator = Paginator(people, 20)
  page = request.GET.get('page')
  
  page_number = page
 
  page_obj = paginator.get_page(page_number)
  return render(request,"main/people.html",{"data":page_obj})


def person_details(request,id):
  try:
    person = Person.objects.get(id=id)
    movies= person.movies.all()
  except Person.DoesNotExist:
    raise Http404("person does not exist")
  return render(request,"main/person_details.html",{'person':person,'movies':movies.order_by('-popularity')})


def all_credits(request,id):
  person = Person.objects.get(id=id)
  movies = person.movies.all()
  return render(request,"main/all_credits.html",{'movies':movies, "name":person.name})

def home(request):
   data = requests.get('https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=2b5b38b211b06bb26131ced7fca692bc').json()
   return render(request,"main/home.html")
  
def auto_complete_search(request):
  print(request.GET)
  if 'term' in request.GET:
    or_lookup = (Q(title__istartswith=request.GET.get('term')))
    popular = Movie.objects.filter(or_lookup).order_by('-popularity')
    qs = popular[0:10]
    
    titles = list()
    for movie in qs:
      titles.append(movie.title)
    return JsonResponse(titles,safe=False)
  return redirect('/')
  
def show_movie_res(request,searched):
  
    or_lookup = (Q(title__istartswith=searched)|Q(title__contains=searched))
    results = Movie.objects.filter(or_lookup).distinct().order_by('-popularity')
    paginator = Paginator(results, 20)
    page = request.GET.get('page')
  
    page_number = page
 
    page_obj = paginator.get_page(page_number)
    return render(request,"main/search_results.html",{"data":page_obj,"searched":searched})

def show_people_res(request,searched):
  ord_lookup = (Q(name__istartswith=searched)|Q(name__contains=searched))
  results = Person.objects.filter(ord_lookup).distinct().order_by('-popularity')
  paginator = Paginator(results, 20)
  page = request.GET.get('page')
  
  page_number = page
 
  page_obj = paginator.get_page(page_number)
  return render(request,"main/search_res_people.html",{"data":page_obj,"searched":searched})

def show_user_res(request,searched):
  ord_lookup = (Q(username__istartswith=searched)|Q(username__contains=searched))
  User = get_user_model()
  results = User.objects.filter(ord_lookup).distinct()
  paginator = Paginator(results, 20)
  page = request.GET.get('page')
  
  page_number = page
 
  page_obj = paginator.get_page(page_number)
  return render(request,"main/search_res_user.html",{"data":page_obj,"searched":searched})
def search_results(request):
   
  if request.POST.get('searched'):
    searched = request.POST.get('searched')
    return redirect('main:show_movies_res',searched)
    
  elif request.POST.get('people_res'):
    searched = request.POST.get('people_res')
    return redirect('main:show_people_res',searched)
  elif request.POST.get('user_res'):
    searched = request.POST.get('user_res')
    return redirect('main:show_user_res',searched)


def profile(request,username):
  try:
    User = get_user_model()
    user = User.objects.get(username=username)
    seen_movies= user.profile.seen_movies.all()
  except:
    raise Http404("profile does not exist")
  return render(request,"main/profile.html",{"seen_movies":seen_movies,'cuser':user})
  
@login_required(login_url='accounts/login')
def change_pic(request):
  
 
   form = ProfileForm(instance=request.user.profile)
   if request.method == "POST" :
    form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
    if form.is_valid():
     form.save()
   return render(request,"main/change_pic.html",{"form":form})
    

def redirect_login(request):
  
  return redirect('main:profile',request.user.username)

def get_popular_movies(request):
  movie_data = Movie.objects.order_by('-popularity')[:20]
  data =[{'id':movie.id,'title':movie.title,'poster_path':movie.poster_path}for movie in movie_data]
  return HttpResponse(json.dumps(data))

