from django.urls import path

from .views import HomeView, WatchView, ResultView, GenreView
from login_regis.views import LogoutView

urlpatterns = [
	path('', HomeView.as_view(), name='home'),
	path('watch', WatchView.as_view()),
	path('genre', GenreView.as_view()),
	path('result', ResultView.as_view()),
    path('logout', LogoutView.as_view()),
]
