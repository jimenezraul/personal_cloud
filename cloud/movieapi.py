import requests
import json
from .models import Movie


class MovieApi:
    api = open("movieapi.txt", "r")
    api = api.read()

    def create(self, movie, user, link):
        url = f"https://api.themoviedb.org/3/movie/{movie['id']}/videos?api_key={self.api}&language=en-US"
        response = requests.get(url)
        response = response.json()
        instance = Movie(user=user)
        instance.movie_id = movie["id"]
        instance.title = movie["original_title"]
        instance.backdrop_path = movie["backdrop_path"]
        instance.overview = movie["overview"]
        instance.poster_path = movie["poster_path"]
        instance.file_url = link
        instance.trailer = response['results'][-1]['key']
        instance.save()

    def create_movie_data(self, movie, user, link):
        url = f"https://api.themoviedb.org/3/search/movie?api_key={self.api}&query={movie}"
        response = requests.get(url)
        response = response.json()
        for i in response["results"]:
            if i['original_title'] == movie.title():
                movies = Movie.objects.filter(user=user)
                if len(movies) != 0:
                    if movie.title() not in [i.title for i in movies]:
                        self.create(i, user, link)

                if len(movies) == 0:
                    self.create(i, user, link)
