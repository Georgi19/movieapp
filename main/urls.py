from django.urls import path
from django.urls.conf import include
from . import views


app_name = 'main'


person_detail_patterns = [
    path('',views.person_details, name="person_details"),
    path("all_credits/",views.all_credits, name="all_credits"),
]
people_patterns = [
    path('',views.people, name="people"),
    path("person_details/<int:id>/",include(person_detail_patterns)),
]

more_info_patterns = [
    path('',views.movie_info, name="movie_info"),
    path("full_cast/",views.full_cast, name="full_cast"),
]

catalogue_urlpatterns = [
    path('',views.catalogue, name="catalogue"),
    path("movie_info/<int:id>/",include(more_info_patterns)),
]
movie_res_url = [
     path('',views.search_results,name="search_movies_res"),
     path('show/<str:searched>/',views.show_movie_res,name="show_movies_res"),
]
user_res_url = [
     path('',views.search_results,name="search_user_res"),
     path('show/<str:searched>/',views.show_user_res,name="show_user_res"),
]
people_res_url = [
     path('',views.search_results,name="search_people_res"),
     path('show/<str:searched>/',views.show_people_res,name="show_people_res"),
]
profile_urls = [
    path('',views.profile,name="profile"),
    
]
accounts_url = [
    path('redirect_login',views.redirect_login,name="redirect_login"),
    path('profile/<slug:username>/',include(profile_urls)),
]
urlpatterns = [
    path('',views.home, name="home"),
    path("catalogue/",include(catalogue_urlpatterns)),
    path("people/",include(people_patterns)),
    path('auto_complete_search/',views.auto_complete_search,name="auto_complete_search"),
    path('search_results/',include(movie_res_url)),
    path('search_people/',include(people_res_url)),
    path('search_user/',include(user_res_url)),
    path('accounts/',include(accounts_url)),
    path('change_pic',views.change_pic,name="change_pic"),
    path('get_popular_movies/',views.get_popular_movies,name="get_popular_movies"),
 
]
