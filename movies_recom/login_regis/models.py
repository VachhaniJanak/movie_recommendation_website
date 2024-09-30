from django.contrib.auth.hashers import make_password
from django.db import models
from mov_home.models import Movie


# Create your models here.
class UserInfo(models.Model):
	username = models.CharField(max_length=20, null=False)
	email = models.EmailField(null=False, unique=True)
	password = models.CharField(max_length=100, null=False)

	watched = models.ManyToManyField(Movie, through='UserWatched', related_name='watched_by')
	mylist = models.ManyToManyField(Movie, through='UserMyList', related_name='mylist_for')
	like = models.ManyToManyField(Movie, through='UserLike', related_name='liked_by')
	dislike = models.ManyToManyField(Movie, through='UserDislike', related_name='disliked_by')
	rating = models.ManyToManyField(Movie, through='RateMovie', related_name='ratemovie_by')

	def __str__(self):
		return f'{self.username} {self.email}'

	def save(self, *args, **kwargs):
		if not self.pk:  # Only hash the password if it's a new user
			self.password = make_password(self.password)
		super(UserInfo, self).save(*args, **kwargs)


class UserWatched(models.Model):
	user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user} {self.movie} {self.timestamp}'


class UserMyList(models.Model):
	user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user} {self.movie} {self.timestamp}'


class UserLike(models.Model):
	user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user} {self.movie} {self.timestamp}'


class UserDislike(models.Model):
	user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user} {self.movie} {self.timestamp}'


class RateMovie(models.Model):
	user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	rate = models.PositiveSmallIntegerField(null=True, default=0)

	def __str__(self):
		return f'{self.user} {self.movie} {self.rate}'


class UserSession(models.Model):
	user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='sessions')
	session_key = models.CharField(max_length=512, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Session for {self.user.username} ({self.session_key})"


class Payment(models.Model):
	user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
	amount = models.PositiveIntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Payment for {self.user.username} ({self.amount})"
