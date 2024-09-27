// Item for Recommendation and mylist movies
export function create_recommended_item({
  base_url,
  movie,
  add_icon = true,
  class_name = "",
  redirect_url = "/home/watch",
}) {
  const item = document.createElement("div");
  const mylist = document.createElement("div");
  const plus = document.createElement("i");
  const play_icon = document.createElement("img");
  const a = document.createElement("a");
  const thumbnail = document.createElement("img");
  const movies_details = document.createElement("div");
  const title = document.createElement("div");
  const details1 = document.createElement("div");
  const runtime = document.createElement("span");
  const language = document.createElement("span");
  const details2 = document.createElement("div");
  const year = document.createElement("span");
  const rating = document.createElement("span");
  const star = document.createElement("span");
  const ratingfield = document.createElement("span");
  const watched = document.createElement("div");

  item.className = `recommended-item ${class_name}`;
  mylist.className = "mylist";
  if (!add_icon) plus.className = "fa fa-close";
  if (add_icon) plus.className = "fa fa-plus";
  mylist.setAttribute("movie-id", movie.id);
  play_icon.className = "play-icon";
  thumbnail.className = "thumbnail";
  movies_details.className = "movies-details";
  title.className = "title";
  details1.className = "details";
  runtime.className = "runtime";
  language.className = "language";
  details2.className = "details";
  year.className = "year";
  rating.className = "rating";
  watched.className = movie.watched;

  // plus.addEventListener("click", () => add(movie.id));
  play_icon.src = base_url + "/static/play-button.svg";
  a.href = `${redirect_url}?movieid=${encodeURIComponent(movie.id)}`;
  thumbnail.src = base_url + "/" + movie.landscape_poster;
  title.textContent = movie.title;
  runtime.textContent = movie.runtime;
  language.textContent = "lg " + movie.language;
  year.textContent = movie.year;
  star.textContent = "\u2605";
  ratingfield.textContent = movie.rating;

  rating.appendChild(star);
  rating.appendChild(ratingfield);
  details2.appendChild(year);
  details2.appendChild(rating);
  details1.appendChild(runtime);
  details1.appendChild(language);
  movies_details.appendChild(title);
  movies_details.appendChild(details1);
  movies_details.appendChild(details2);
  a.appendChild(thumbnail);
  a.appendChild(watched);
  a.appendChild(movies_details);
  mylist.appendChild(plus);
  item.appendChild(play_icon);
  item.appendChild(mylist);
  item.appendChild(a);
  return item;
}

// Item for trending and ocscar movies
export function create_vertical_item({
  base_url,
  movie,
  add_icon = "",
  class_name = "",
  redirect_url = "/home/watch",
}) {
  const item = document.createElement("div");
  const mylist = document.createElement("div");
  const plus = document.createElement("i");
  const play_icon = document.createElement("img");
  const a = document.createElement("a");
  const thumbnail = document.createElement("img");
  const details = document.createElement("div");
  const title = document.createElement("div");
  const year = document.createElement("span");
  const watched = document.createElement("div");

  item.className = "horizontal-container-item";
  mylist.className = "mylist";
  plus.className = "fa fa-plus";
  mylist.setAttribute("movie-id", movie.id);
  play_icon.className = "play-icon";
  play_icon.src = base_url + "/static/play-button.svg";
  thumbnail.className = "thumbnail";
  details.className = "details";
  year.className = "year";
  title.className = "title";

  a.href = `${redirect_url}?movieid=${encodeURIComponent(movie.id)}`;
  // plus.addEventListener("click", () => add(movie.id));
  thumbnail.src = base_url + "/" + movie.vertical_poster;
  year.textContent = movie.year;
  title.textContent = movie.title;
  watched.className = movie.watched;

  details.appendChild(year);
  details.appendChild(title);
  a.appendChild(thumbnail);
  a.appendChild(watched);
  a.appendChild(details);
  mylist.appendChild(plus);
  item.appendChild(play_icon);
  item.appendChild(mylist);
  item.appendChild(a);
  return item;
}
