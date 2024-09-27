from django.views import View

from django.http import JsonResponse
from login_regis.models import UserInfo, RateMovie, UserMyList
from mov_home.models import Movie
from mov_home.views import engine_model, slice_size
from django.db.models import Case, When
import json


def json_return(user_id, movies):
	return JsonResponse(
		{
			'movies':
				[
					{
						'id': movie.id,
						'title': movie.title,
						'watched': 'watched' if movie.watched_by.filter(id=user_id) else 'notwatched',
						'landscape_poster': movie.landscape_poster.url,
						'vertical_poster': movie.vertical_poster.url,
						'year': movie.year,
						'language': movie.language,
						'runtime': str(movie.runtime),
						'rating': movie.rating,
					} for movie in list(movies)
				]
		}
	)


# Create your views here.
class GetSearchView(View):
	def get(self, request):
		return JsonResponse({'suggestions': engine_model.search_suggestions(request.GET.get('query'))})


class GetSearchResultView(View):
	def post(self, request):
		userinfo = request.session
		userid = userinfo.get('id')
		if userid:
			count = json.loads(request.body).get('present_count')
			movies_ids = userinfo['search_movies_ids'][count:count + slice_size]
			order = Case(*[When(id=id, then=pos) for pos, id in enumerate(movies_ids)])
			movies = Movie.objects.filter(id__in=movies_ids).order_by(order)
			return json_return(userid, movies)
		else:
			return JsonResponse({})


class GetGenreView(View):
	def post(self, request):
		userinfo = request.session
		userid = userinfo.get('id')
		if userid:
			count = json.loads(request.body).get('present_count')
			movies = Movie.objects.filter(genre__contains=userinfo['genre_name']).order_by('-year')[count:count + slice_size]
			return json_return(userid, movies)
		else:
			return JsonResponse({})


class GetOscarMoviesView(View):
	def post(self, request):
		userinfo = request.session
		userid = userinfo.get('id')
		if userid:
			count = json.loads(request.body).get('present_count')
			movies = Movie.objects.filter(year__gte="2021-1-1", oscars=True).order_by('-year')[count:count + slice_size]
			return json_return(userid, movies)
		else:
			return JsonResponse({})

class GetRecommendationView(View):
	def post(self, request):
		userinfo = request.session
		userid = userinfo.get('id')
		if userid:
			count = json.loads(request.body).get('present_count')
			movies_ids = userinfo['recommend_movies_ids'][count: count+slice_size]
			order = Case(*[When(id=id, then=pos) for pos, id in enumerate(movies_ids)])
			movies = Movie.objects.filter(id__in=movies_ids).order_by(order)
			return json_return(userid, movies)
		else:
			return JsonResponse({})


class GetWatchRecommendationView(View):
	def post(self, request):
		userinfo = request.session
		userid = userinfo.get('id')
		if userid:
			count = json.loads(request.body).get('present_count')
			movies_ids = userinfo['watch_recommend_ids'][count: count+slice_size]
			order = Case(*[When(id=id, then=pos) for pos, id in enumerate(movies_ids)])
			movies = Movie.objects.filter(id__in=movies_ids).order_by(order)
			return json_return(userid, movies)
		else:
			return JsonResponse({})


class GetMyListView(View):
	def post(self, request):
		userinfo = request.session
		userid = userinfo.get('id')
		if userid:
			count = json.loads(request.body).get('present_count')
			user = UserInfo.objects.get(id=userinfo['id'])
			movies_ids = tuple(UserMyList.objects.filter(user=user).order_by('-timestamp').values_list('movie', flat=True))[count: count+slice_size]
			order = Case(*[When(id=id, then=pos) for pos, id in enumerate(movies_ids)])
			movies = Movie.objects.filter(id__in=movies_ids).order_by(order)
			return json_return(userid, movies)
		else:
			return JsonResponse({})


class AddToMyListView(View):
	def post(self, request):
		userinfo = request.session
		userid = userinfo.get('id')
		if userid:
			movie_id = json.loads(request.body).get('movieid')
			user = UserInfo.objects.get(id=userid)
			if not user.mylist.filter(id=movie_id).exists():
				movie = Movie.objects.get(id=movie_id)
				user.mylist.add(movie)
				return JsonResponse({
					"msg": f"{movie.title.title()} is added to your list successfully.",
					"movie": {'id': movie.id,
					          'title': movie.title,
					          'watched': 'watched' if movie.watched_by.filter(id=userid) else 'notwatched',
					          'landscape_poster': movie.landscape_poster.url,
					          'year': movie.year,
					          'language': movie.language,
					          'runtime': str(movie.runtime),
					          'rating': movie.rating, }
				})
			else:
				return JsonResponse({"msg": "Movie already in your list."})
		else:
			return JsonResponse({})


class RemoveFromMyListView(View):
	def post(self, request):
		userinfo = request.session
		userid = userinfo.get('id')
		if userid:
			movie_id = json.loads(request.body).get('movieid')
			user = UserInfo.objects.get(id=userid)
			if user.mylist.filter(id=movie_id).exists():
				user.mylist.remove(Movie.objects.get(id=movie_id))
				return JsonResponse({})
		else:
			return JsonResponse({})


class LikeMovieView(View):
	def post(self, request):
		userinfo = request.session
		userid = userinfo.get('id')
		if userid:
			movie_id = json.loads(request.body).get('movieid')		
			user = UserInfo.objects.get(id=userid)
			movie = Movie.objects.get(id=movie_id)
			if user.like.filter(id=movie_id).exists():
				user.like.remove(movie)
			else:
				user.like.add(movie)
				user.dislike.remove(movie)
			return JsonResponse({})
		else:
			return JsonResponse({})


class DislikeMovieView(View):
	def post(self, request):
		userinfo = request.session
		userid = userinfo.get('id')
		if userid:
			movie_id = json.loads(request.body).get('movieid')		
			user = UserInfo.objects.get(id=userid)
			movie = Movie.objects.get(id=movie_id)
			if user.dislike.filter(id=movie_id).exists():
				user.dislike.remove(movie)
			else:
				user.dislike.add(movie)
				user.like.remove(movie)
			return JsonResponse({})
		else:
			return JsonResponse({})


class RateMovieView(View):
	def post(self, request):
		userinfo = request.session
		userid = userinfo.get('id')
		if userid:
			data = json.loads(request.body)
			rating_num = data.get('rating')
			movie_id = data.get('movieid')
			movie = Movie.objects.get(id=movie_id)
			user = UserInfo.objects.get(id=userid)
			if user.rating.filter(id=movie_id).exists():
				user.rating.remove(movie)
				RateMovie.objects.create(user=user, movie=movie, rate=int(rating_num))
			else:
				RateMovie.objects.create(user=user, movie=movie, rate=rating_num)
			return JsonResponse({})
		else:
			return JsonResponse({})

