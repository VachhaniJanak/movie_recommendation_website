from django.urls import path

from .views import GetSearchView, GetSearchResultView, GetGenreView, GetOscarMoviesView, GetRecommendationView, \
	GetWatchRecommendationView, GetMyListView, AddToMyListView, RemoveFromMyListView, LikeMovieView, DislikeMovieView, RateMovieView

urlpatterns = [
	path('search', GetSearchView.as_view()),
	path('searchresult', GetSearchResultView.as_view()),
	path('genre', GetGenreView.as_view()),
	path('oscar', GetOscarMoviesView.as_view()),
	path('recommendation', GetRecommendationView.as_view()),
	path('watchrecommendation', GetWatchRecommendationView.as_view()),
	path('mylist', GetMyListView.as_view()),
	path('addtomylist', AddToMyListView.as_view()),
	path('removefrommylist', RemoveFromMyListView.as_view()),
	path('like', LikeMovieView.as_view()),
	path('dislike', DislikeMovieView.as_view()),
	path('rating', RateMovieView.as_view()),
]
