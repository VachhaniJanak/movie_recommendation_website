import datetime
from pathlib import Path

import chromadb
from django.db import models
from sentence_transformers import SentenceTransformer

# Build paths inside the project like this: BASE_DIR / 'subdir'.
base_path = Path(__file__).resolve().parent.parent


class vectordb:
	def __init__(self, path) -> None:
		self.emb_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
		self.client = chromadb.PersistentClient(path=f'{base_path / "vector_database"}')
		self.titles_collection = self.client.get_or_create_collection(name="titles")
		self.desc_collection = self.client.get_or_create_collection(name="descriptions")

	def search_title_query(self, query: tuple[str], top_n: int, document=True) -> tuple[str] | tuple[int]:
		result = self.titles_collection.query(
			query_embeddings=self.emb_model.encode(query).tolist(),
			n_results=top_n)
		return tuple(
			title for sub_list in result['documents'] for title in sub_list
		) if document else tuple(
			int(id) for sub_list in result['ids'] for id in sub_list
		)

	def delete(self, ids: tuple[str]) -> None:
		self.titles_collection.delete(ids=ids)
		self.desc_collection.delete(ids=ids)

	def create(self, embedding: list[float], id: tuple[str], title: tuple[str]) -> None:
		self.titles_collection.add(
			documents=[title],
			ids=[id],
			embeddings=[self.emb_model.encode(title).tolist()]
		)
		self.desc_collection.add(
			documents=[title],
			ids=[id],
			embeddings=[embedding]
		)

	def get_vectors_by_ids(self, movie_ids: tuple[str]) -> list[list[float]]:
		if len(movie_ids) == 0:
			return [[]]
		return self.desc_collection.get(ids=movie_ids, include=['embeddings'])['embeddings']

	def get_ids_by_vectors(self, vectors: list[list[float]], top_n: int) -> list[list[str]]:
		if len(vectors) == 0 or len(vectors[0]) == 0:
			return [[]]
		return self.desc_collection.query(query_embeddings=vectors,
		                                  n_results=top_n)['ids']


vectordatabase = vectordb(path=f'{base_path}/chromadb')


class Movie(models.Model):
	title = models.CharField(max_length=200, null=False)

	year = models.DateField(
		default=datetime.datetime.now().strftime('%Y-%m-%d'),
		null=True
	)

	runtime = models.DurationField(
		default=datetime.timedelta(hours=2),
		null=True
	)

	oscars = models.BooleanField(
		verbose_name="Oscars wins",
		default=False,
		null=True
	)

	adult = models.BooleanField(
		verbose_name="Adult",
		default=False,
		null=True
	)

	language = models.CharField(max_length=500, null=True)
	country = models.CharField(max_length=500, null=True)

	director = models.TextField(null=True)
	genre = models.TextField(null=False)
	writer = models.TextField(null=True)
	actors = models.TextField(null=True)
	plot = models.TextField(null=True)

	video_path = models.CharField(null=True, max_length=500)
	vertical_poster = models.ImageField(null=False, upload_to='uploads/movies_posters/vertical/')
	landscape_poster = models.ImageField(null=False, upload_to='uploads/movies_posters/landscape/')
	rated = models.CharField(max_length=10, null=True)
	rating = models.FloatField(null=True)

	def __str__(self):
		return f"{self.title}"

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		desc = [
			f"{self.director} {self.writer} {self.actors}",
			f"{self.genre}",
			f"{self.plot}",
			f"{self.language} {self.country} {self.oscars} {self.adult}",
		]

		embedding = 0
		for desc_string in desc:
			embedding += vectordatabase.emb_model.encode(desc_string)
		embedding = embedding / len(desc)

		vectordatabase.create(embedding.tolist(), str(self.id), self.title)


class MostWatched(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	count = models.IntegerField()
