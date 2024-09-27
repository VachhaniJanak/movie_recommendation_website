from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from login_regis.models import UserInfo, UserMyList, UserWatched, UserLike, UserDislike, RateMovie
from django.views import View
from .models import Movie, vectordatabase, MostWatched
from engines.views import Engine
from torch import device, cuda

from threading import Thread


device = device("cuda") if cuda.is_available() else device("cpu")
slice_size = 16

genres_types = {"action": "Action",
                "adventure": "Adventure",
                "animation": "Animation",
                "comedy": "Comedy",
                "crime": "Crime",
                "documentary": "Documentary",
                "drama": "Drama",
                "family": "Family",
                "fantasy": "Fantasy",
                "history": "History",
                "horror": "Horror",
                "music": "Music",
                "mystery": "Mystery",
                "romance": "Romance",
                "science fiction": "Sci Fi",
                "tv movie": "TV Movie",
                "thriller": "Thriller",
                "war": "War",
                "western": "Western"}

engine_model = Engine(device=device, vectordatabase=vectordatabase, min_max_rating=(3, 5), upto=32,
                      each_upto=32, table_name=Movie, users_attrs_names=(UserMyList, UserLike, UserDislike, UserWatched))

def create_session(request, user):
	request.session['id'] = user.id
	request.session['username'] = user.username
	request.session['search_query'] = ""
	request.session['genre_name'] = ""
	request.session['recommend_movies_ids'] = tuple()
	request.session['search_movies_ids'] = tuple()
	request.session['watch_recommend_ids'] = tuple()

flage = True

def top_ten_movies_of_last_week(days=7, upto=10):
	global flage
	if flage:
		flage = False
		# Get the current date and time
		now = timezone.now()
		# Calculate the date one week ago
		one_week_ago = now - timedelta(days=days)
		day = now.strftime("%a")
		if day == "Sat":
			# Get the top 10 most-watched movies in the last week
			# Group by 'movie'
			# Count occurrences of each movie
			# Order by the count in descending order and limit to 10
			top_movies = tuple(UserWatched.objects.filter(timestamp__gte=one_week_ago).order_by('-timestamp').values('movie').annotate(watch_count=Count('movie')).order_by('-watch_count')[:upto]) 
			if top_movies:
				MostWatched.objects.all().delete()
			for movie in top_movies:
				count = movie['watch_count']
				movie = Movie.objects.get(id=movie['movie'])
				MostWatched(movie=movie, count=count).save()

		flage = True

top_ten_movies_of_last_week()

class HomeView(View):
	def get(self, request):
		userinfo = request.session
		user = UserInfo.objects.filter(id=userinfo.get('id')).first()
		if user:
			now = timezone.now()
			day = now.strftime("%a")
			if flage:
				Thread(target=top_ten_movies_of_last_week).start()
			create_session(request, user)
			request.session['recommend_movies_ids'] = engine_model.recommended_movies_from_history(user.id, mylist_wight=16, like_wight=16, dislike_wight=32, watched_wight=256)
			request.session.modified = True
			top_ten = Movie.objects.filter(
				id__in=tuple(MostWatched.objects.all().order_by('-count')[:10].values_list('movie', flat=True))
				)
			return render(request, 'index.html', {
				'user_name': user.username[0].upper(),
				'genres': genres_types,
				'top_ten': top_ten,
				'mylist_movies':UserMyList.objects.filter(user=user).first(),
				'recommended_movies':len(request.session['recommend_movies_ids'])
			})
		else:
			return HttpResponseRedirect(reverse('login'))

class ResultView(View):
	def get(self, request):
		query = request.GET.get('query')
		userinfo = request.session
		if userinfo.get('id'):
			request.session['search_query'] = query
			request.session['search_movies_ids'] = engine_model.get_query_result(query)
			request.session.modified = True
			return render(request, 'result.html', {
				'user_name': userinfo['username'][0].upper(),
				'genres': genres_types,
				'query': query,
				'result_page': True,
			})
		else:
			return HttpResponseRedirect(reverse('login'))


class GenreView(View):
	def get(eslf, request):
		genre_name = request.GET.get('key')
		userinfo = request.session
		if userinfo.get('id'):
			request.session['genre_name'] = genre_name
			request.session.modified = True
			return render(request, 'result.html', {
			'user_name': userinfo['username'][0].upper(),
			'genres': genres_types,
			'query': genre_name,
			'result_page': False,
		})
		else:
			return HttpResponseRedirect(reverse('login'))
		

class WatchView(View):
	def get(self, request):
		movie_id = request.GET.get('movieid')
		userinfo = request.session
		if userinfo.get('id'):
			request.session['watch_recommend_ids'] = engine_model.recommend_movies(movie_id, 64)
			request.session.modified = True

			selected_movie = Movie.objects.get(id=movie_id)
			user = UserInfo.objects.get(id=userinfo['id'])
			user.watched.add(selected_movie)

			liked = "liked" if user.like.filter(id=movie_id) else ""
			disliked = "disliked" if user.dislike.filter(id=movie_id) else ""

			rated = RateMovie.objects.filter(user=user, movie=selected_movie).first()
			rated = rated.rate if rated else 0

			return render(request, 'watch.html', {
			'liked': liked,
			'disliked': disliked,
			'selected_movie': selected_movie,
			'rated': rated
		})
		else:
			return HttpResponseRedirect(reverse('login'))


