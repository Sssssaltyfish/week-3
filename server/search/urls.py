from django.urls import path
from django.urls.conf import re_path

from . import views

app_name = ''
urlpatterns = [
    path('', views.index, name='index'),
    path('list/<page_type>/<int:page>', views.list_dispatch, name='list-all'),
    path('list/<page_type>/', views.list_dispatch, { 'page': 1 }, name='list-all'),
    path('movies/<name>', views.movie_detail, name='movie-detail'),
    path('actors/<name>', views.actor_detail, name='actor-detail'),
    path('search', views.search, name='search'),
]
'''\?(?=.*<actor>)?(?=.*<movie>)?(?=.*<comment>)?(?=.*<content>)?'''