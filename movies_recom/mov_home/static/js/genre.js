import { add_item_mylist } from "./index.js";
import {
  get_movies_on_scroll,
  load_on_load,
  clientheight,
} from "./assemble.mjs";
import { create_recommended_item } from "./create_items.mjs";

const recommendation_container = document.getElementById(
  "recommended-container"
);
const msg_tage = document.getElementById("msg");

window.onload = () => {
  load_on_load({
    container: recommendation_container,
    url_path: "/api/genre",
    screen_dim: clientheight,
    along_height: true,
    offset: 300,
    create_item: create_recommended_item,
  });
};

var genre_flage = true;
window.addEventListener("scroll", async () => {
  if (
    (document.documentElement.scrollTop +
      document.documentElement.clientHeight >=
    document.documentElement.scrollHeight - 50) && genre_flage
  ) {
    genre_flage = false;
    await get_movies_on_scroll({
      url_path: "/api/genre",
      container: recommendation_container,
      create_item: create_recommended_item,
    });
    genre_flage = true;
  }
});

function add_to_mylist(listener) {
  var movie_id = listener.parentNode.getAttribute("movie-id");
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
