import { add_item_mylist } from "./index.js";

import {
  get_movies_on_scroll,
  load_on_load,
  clientheight,
} from "./assemble.mjs";

import { create_recommended_item } from "./create_items.mjs";

const like_icon = document.getElementsByClassName("fa fa-thumbs-up");
const dislike_icon = document.getElementsByClassName("fa fa-thumbs-down");
const recommendation_container = document.getElementById(
  "recommended-container"
);
const description_container = document.getElementById("description");
const msg_tage = document.getElementById("msg");
const movie_id = document.getElementById("movieid").value;

window.onload = () => {
  load_on_load({
    container: recommendation_container,
    url_path: "/api/watchrecommendation",
    screen_dim: clientheight,
    along_height: true,
    offset: 200,
    create_item: create_recommended_item,
  });
};

var watchrecommendation_flage = true;
window.addEventListener("scroll", async () => {
  if (
    document.documentElement.scrollTop +
      document.documentElement.clientHeight >=
      document.documentElement.scrollHeight - 50 &&
    watchrecommendation_flage
  ) {
    watchrecommendation_flage = false;
    await get_movies_on_scroll({
      url_path: "/api/watchrecommendation",
      container: recommendation_container,
      create_item: create_recommended_item,
    });
    watchrecommendation_flage = true;
  }
});

function add_to_mylist(listener) {
  let movie_id = listener.parentNode.getAttribute("movie-id");
  movie_id = movie_id | 0;
  if (movie_id) {
    add_item_mylist({
      id: movie_id,
      msg_tage: msg_tage,
    });
  }
}

recommendation_container.addEventListener("click", (event) => {
  add_to_mylist(event.target);
});

function like_func() {
  fetch("/api/like", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getcsrftoken,
    },
    body: JSON.stringify({ movieid: movie_id }),
  });

  if (like_icon[0].style.color == "rgb(51, 98, 185)") {
    like_icon[0].style.color = "#B0B0B0";
  } else {
    like_icon[0].style.color = "#3362b9";
    dislike_icon[0].style.color = "#B0B0B0";
  }
}

function dislike_func(id) {
  fetch("/api/dislike", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getcsrftoken,
    },
    body: JSON.stringify({ movieid: movie_id }),
  });

  if (dislike_icon[0].style.color == "rgb(51, 98, 185)") {
    dislike_icon[0].style.color = "#B0B0B0";
  } else {
    like_icon[0].style.color = "#B0B0B0";
    dislike_icon[0].style.color = "#3362b9";
  }
}

description_container.addEventListener("click", (event) => {
  var child = event.target;
  if (movie_id) {
    if (child.className === "fa fa-thumbs-up") {
      like_func();
    } else if (child.className === "fa fa-thumbs-down") {
      dislike_func();
    }
  }
});
