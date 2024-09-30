from itertools import islice
from random import shuffle

import torch
import torch.nn as nn
from torch import (
	ones,
	tensor, sort,
	concat, unique_consecutive,
	mean, bool, long)


def fetch_data(userid: int, attr_name, upto_history: int) -> tuple:
	return tuple(
		islice(
			attr_name.objects.filter(user=userid).order_by('-timestamp').values_list('movie', flat=True).iterator(),
			upto_history
		)
	)


class CollRecSysModel(nn.Module):
	def __init__(self, users_buckets, movies_buckets, embedding_dim=32):
		super().__init__()

		self.users_buckets = users_buckets
		self.movies_buckets = movies_buckets

		self.user_embed = nn.Embedding(users_buckets, embedding_dim, sparse=True)
		self.movie_embed = nn.Embedding(movies_buckets, embedding_dim, sparse=True)

		self.user_embed.weight.data.uniform_(-0.05, 0.05)
		self.movie_embed.weight.data.uniform_(-0.05, 0.05)

		self.dropout0 = nn.Dropout(0.5)
		self.dropout1 = nn.Dropout(0.5)

		self.m = torch.nn.Sigmoid()

	def forward(self, users_ids, movies_ids):
		hashed_users_ids = users_ids % self.users_buckets
		hashed_movies_ids = movies_ids % self.movies_buckets

		user_embed = self.user_embed(hashed_users_ids)
		movie_embed = self.movie_embed(hashed_movies_ids)

		output = (self.dropout0(user_embed) * self.dropout1(movie_embed)).sum(1)
		return self.m(output)

	def expand_embeddings(self, users_buckets, movies_buckets):
		"""
		Expand the embedding table to accommodate more embeddings.
		new_num_embeddings: New total number of embeddings after expansion.
		"""
		if users_buckets > self.users_buckets:
			# Create a new embedding layer with the expanded size
			new_user_embed = nn.Embedding(users_buckets, self.embedding_dim)

			# Copy the old embeddings into the new expanded layer
			with torch.no_grad():
				new_user_embed.weight[:self.users_buckets] = self.user_embed.weight
				self.user_embed = new_user_embed
				self.users_buckets = users_buckets

		if movies_buckets > self.movies_buckets:
			# Create a new embedding layer with the expanded size
			new_movie_embed = nn.Embedding(movies_buckets, self.embedding_dim)

			# Copy the old embeddings into the new expanded layer
			with torch.no_grad():
				new_movie_embed.weight[:self.movies_buckets] = self.movie_embed.weight
				self.movie_embed = new_movie_embed
				self.movies_buckets = movies_buckets


class ContentRecommendation:
	def __init__(self, device, vectordatabase) -> None:
		self.device = device
		self.vectordatabase = vectordatabase

	def resultdone_vector(self, movies_ids: tuple):
		movies_ids = [str(id) for id in movies_ids]
		return mean(tensor(self.vectordatabase.get_vectors_by_ids(movies_ids)).to(self.device), dim=0)

	def get_nearest(self, like_ids: tuple[int], watched_ids: tuple[int], upto: int) -> tuple[int]:
		vector0 = self.resultdone_vector(watched_ids).tolist()
		vector1 = self.resultdone_vector(like_ids).tolist()
		if vector0 and vector1:
			result = self.vectordatabase.get_ids_by_vectors([vector0, vector1], upto)
		elif vector0:
			result = self.vectordatabase.get_ids_by_vectors([vector0], upto)
		elif vector1:
			result = self.vectordatabase.get_ids_by_vectors([vector1], upto)
		else:
			result = [[]]
		result = [int(id) for result_list in result for id in result_list]
		shuffle(result)
		return tuple(result)

	def get_nearest_ids(self, movies_ids: tuple[int], upto: int) -> tuple[int]:
		vector = self.vectordatabase.get_vectors_by_ids([str(id) for id in set(movies_ids)])
		result = self.vectordatabase.get_ids_by_vectors(vector, upto)
		return tuple(int(id) for result_list in result for id in result_list)


class CollaborativeRecommendation:
	def __init__(self, device, base_path) -> None:
		self.device = device
		self.model = CollRecSysModel(users_buckets=73616, movies_buckets=34619, ).to(device)

		self.model.load_state_dict(torch.load(base_path / "rec_model/coll_model.pth", map_location=device))

	def predict(self, user_id: int, movies_ids: tuple, min_max_rating: tuple) -> tuple:
		user_ids = tensor(user_id, dtype=long).to(self.device).repeat(len(movies_ids))
		movies_ids = tensor(movies_ids, dtype=long).to(self.device)
		model_predict = self.model(user_ids, movies_ids).squeeze()
		# index = model_predict >= min_max_rating[0]
		index = model_predict >= 0.5
		model_predict = model_predict[index]
		movies_ids = movies_ids[index]
		# index = model_predict <= min_max_rating[1]
		# model_predict = concat([model_predict[index].unsqueeze(0), movies_ids[index].unsqueeze(0)])
		model_predict = concat([model_predict.unsqueeze(0), movies_ids.unsqueeze(0)])
		return tuple(model_predict[1][sort(model_predict, descending=True).indices[0]].tolist())


class HybrideRecommendation:

	def __init__(self, device, base_path, vectordatabase, min_max_rating: tuple,
	             upto: int,
	             each_upto: int, ) -> None:
		self.content_recom = ContentRecommendation(device=device, vectordatabase=vectordatabase)
		self.coll_recom = CollaborativeRecommendation(device, base_path)
		self.min_max_rating = min_max_rating
		self.upto = upto
		self.each_upto = each_upto

	def get_recommendation(self, user_id: int, mylist_ids: tuple, like_ids: tuple, dislike_ids: tuple,
	                       watched_ids: tuple, watched_weight: int) -> tuple[int]:
		new_watched_ids = tuple(set(watched_ids[:watched_weight]) - set(mylist_ids))

		all_nearest_movies_ids = self.content_recom.get_nearest_ids(
			movies_ids=set(mylist_ids + like_ids + new_watched_ids), upto=self.each_upto)

		positive_movies_ids = self.content_recom.get_nearest(like_ids=like_ids, watched_ids=new_watched_ids,
		                                                     upto=self.upto)
		negative_movies_ids = self.content_recom.get_nearest_ids(dislike_ids, self.upto)
		predicted_list = self.coll_recom.predict(user_id, all_nearest_movies_ids, self.min_max_rating)

		negative_movies_ids += watched_ids
		return self.filter(predicted_list, positive_movies_ids, negative_movies_ids)

	def filter(self, collaborative_list: tuple, content_list: tuple, remove_list: tuple) -> tuple[int]:
		collaborative_list_length = len(collaborative_list)
		content_list_length = len(content_list)
		combine_list = list()

		for i in range(
				collaborative_list_length if collaborative_list_length > content_list_length else content_list_length):
			if i < collaborative_list_length:
				combine_list.append(collaborative_list[i])
			if i < content_list_length:
				combine_list.append(content_list[i])

		out = tensor(combine_list)
		index = ones((out.shape[0]), dtype=bool)
		for i in remove_list:
			index &= (out - i).bool()
		out = out[index]
		return tuple(unique_consecutive(out).tolist())


class Engine:

	def __init__(self, device, base_path, vectordatabase, min_max_rating: tuple, upto: int,
	             each_upto: int, users_attrs_names: tuple) -> None:
		"""
			users_attrs_name is in order of (mylist, like, dislike, watched)
		"""

		self.vectordatabase = vectordatabase

		self.hybride = HybrideRecommendation(
			device,
			base_path,
			vectordatabase=self.vectordatabase,
			min_max_rating=min_max_rating,
			upto=upto,
			each_upto=each_upto,
		)
		self.users_attrs_names = users_attrs_names

	def search_suggestions(self, query: str, no_result: int = 12) -> tuple:
		return self.vectordatabase.search_title_query(query=(query,), top_n=no_result, document=True)

	def get_query_result(self, query: str, no_result: int = 500) -> tuple:
		return self.vectordatabase.search_title_query(query=(query,), top_n=no_result, document=False)

	def recommend_movies(self, movie_id: int, upto_no: int = 128) -> tuple:
		vector = self.vectordatabase.get_vectors_by_ids([str(movie_id)])
		ids = self.vectordatabase.get_ids_by_vectors(vectors=vector, top_n=upto_no)[0][1:]
		return tuple(int(id) for id in ids)

	def recommended_movies_from_history(self, userid: int, mylist_wight: int, like_wight: int, dislike_wight: int,
	                                    watched_wight: int) -> tuple[int]:
		mylist = fetch_data(userid=userid, attr_name=self.users_attrs_names[0], upto_history=mylist_wight)
		like = fetch_data(userid=userid, attr_name=self.users_attrs_names[1], upto_history=like_wight)
		dislike = fetch_data(userid=userid, attr_name=self.users_attrs_names[2], upto_history=dislike_wight)
		watched = fetch_data(userid=userid, attr_name=self.users_attrs_names[3], upto_history=watched_wight)
		return self.hybride.get_recommendation(
			user_id=userid,
			mylist_ids=mylist,
			like_ids=like,
			dislike_ids=dislike,
			watched_ids=watched,
			watched_weight=like_wight
		)
