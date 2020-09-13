import time
from functools import lru_cache
from typing import Any

from django.db.models.query_utils import Q
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest
from django.http.request import HttpRequest
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from urllib.parse import urlencode

from .models import *

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return movies_list(request)

def movie_detail(request: HttpRequest, name: str) -> HttpResponse:
    movie = Movie.objects.get(title=name)
    context = {
        'movie': movie,
    }
    return render(request, 'search/movies/detail.html', context)

def actor_detail(request: HttpRequest, name: str) -> HttpResponse:
    actor = Actor.objects.get(name=name)
    context = {
        'actor': actor,
    }
    return render(request, 'search/actors/detail.html', context)

def movies_list(request: HttpRequest, page: int = 1) -> HttpResponse:
    movies = Movie.objects.all()
    paginator = Paginator(movies, 10, 4)
    page = paginator.get_page(page)
    context = {
        'page': page,
        'page_type': 'movies',
    }
    return render(request, 'search/movies/list.html', context)

def actors_list(request: HttpRequest, page: int = 1) -> HttpResponse:
    actors = Actor.objects.all()
    paginator = Paginator(actors, 10, 4)
    page = paginator.get_page(page)
    context = {
        'page': page,
        'page_type': 'actors',
    }
    return render(request, 'search/actors/list.html', context)

def list_dispatch(request: HttpRequest, page_type: str, page: int = 1) -> HttpResponse:
    try:
        return globals()[f'{page_type}_list'](request, page)
    except KeyError as e:
        raise Http404(f"Page not found: {page_type} {page}")

def search(request: HttpRequest) -> HttpResponse:
    context = {
        'search': request.POST.get('search', ''),
        'search-type': request.POST.get('search-type', ''),
    }
    return redirect(f'/list/result/1?{urlencode(context)}', permanent=True)

@ lru_cache
def get(query, query_type):
    result: Any
    if query_type == 'actor':
        result = Actor.objects.filter(Q(name__icontains=query) | Q(movie__title__icontains=query)).distinct()
    elif query_type == 'movie':
        result = Movie.objects.filter(Q(title__icontains=query) | Q(actors__name__icontains=query)).distinct()
    elif query_type == 'comment':
        result = Movie.objects.filter(Q(comments__icontains=query)).distinct()
    else:
        print('Impossible!')
        return HttpResponseBadRequest("Invalid search type")
    return result

def result_list(request: HttpRequest, page: int = 1) -> HttpResponse:

    query = request.GET.get('search', '')
    query_type = request.GET.get('search-type', '')
    start = time.time()
    result = get(query, query_type)
    if isinstance(result, HttpResponse):
        return result

    interval = time.time() - start
    paginator = Paginator(result, 20, 6)
    page = paginator.get_page(page)
    context = {
        'page': page,
        'time_spent': interval,
        'page_type': 'result',
    }
    return render(request, 'search/search.html', context)
