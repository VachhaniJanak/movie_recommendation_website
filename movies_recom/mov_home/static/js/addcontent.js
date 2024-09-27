import { add_item_mylist } from "./index.js";

import {
  get_movies_on_scroll,
  load_on_load,
  clientheight,
  clientwidth,
} from "./assemble.mjs";

import {
  create_recommended_item,
  create_vertical_item,
} from "./create_items.mjs";

const main_container = document.getElementById("main");
const recommendation_container = document.getElementById(
  "recommended-container"
);
const horizontal_container = document.getElementById("horizontal-container");
const mylist_container = document.getElementById("mylist-container");
const trending_now = document.getElementById("trending-now");
const msg_tage = document.getElementById("msg");
const loader = document.getElementById("loader-container");

window.onload = async () => {
  loader.className = "loader";
  load_on_load({
    container: mylist_container,
    container_dim: main_container,
    url_path: "/api/mylist",
    screen_dim: clientwidth,
    along_height: false,
    offset: 50,
    create_item: create_recommended_item,
    class_name: "mylists-items",
    add_icon: false,
  });
  load_on_load({
    container: horizontal_container,
    url_path: "/api/oscar",
    screen_dim: clientwidth,
    along_height: false,
    offset: 50,
    create_item: create_vertical_item,
  });
  await load_on_load({
    container: recommendation_container,
    url_path: "/api/recommendation",
    screen_dim: clientheight,
    along_height: true,
    offset: 10,
    create_item: create_recommended_item,
  });
  loader.className = "";
};

var recommendation_flage = true;
window.addEventListener("scroll", async () => {
  if (
    (document.documentElement.scrollTop +
      document.documentElement.clientHeight >=
    document.documentElement.scrollHeight - 50) &&
    recommendation_flage 
  ) {
    recommendation_flage = false;
    loader.className = "loader";
    await get_movies_on_scroll({
      url_path: "/api/recommendation",
      container: recommendation_container,
      create_item: create_recommended_item,
    });
    loader.className = "";
    recommendation_flage = true;
  }
});

var oscar_flage = true;
document
  .getElementById("horizontal-container")
  .addEventListener("scroll", async () => {
    if (
      (horizontal_container.scrollLeft + document.documentElement.clientWidth >=
      horizontal_container.scrollWidth - 50) && oscar_flage
    ) {
      oscar_flage = false;
      await get_movies_on_scroll({
        url_path: "/api/oscar",
        container: horizontal_container,
        create_item: create_vertical_item,
      });
      oscar_flage = true;
    }
  });

var mylist_flage = true;
document.getElementById("mylist-container").addEventListener("scroll", async () => {
  if (
    (mylist_container.scrollLeft + document.documentElement.clientWidth >=
    mylist_container.scrollWidth - 50) && mylist_flage
  ) {
    mylist_flage = false;
    await get_movies_on_scroll({
      url_path: "/api/mylist",
      container: mylist_container,
      create_item: create_recommended_item,
      add_icon: false,
      class_name: "mylists-items",
    });
    mylist_flage = true;
  }
});

mylist_container.addEventListener("click", async (event) => {
  const childElement = event.target.parentNode.parentElement;
  if (childElement.parentNode === mylist_container) {
    const children = Array.from(mylist_container.children);
    const index = children.indexOf(childElement);
    const id = event.target.parentNode.getAttribute("movie-id");
    fetch("/api/removefrommylist", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getcsrftoken,
      },
      body: JSON.stringify({ movieid: id }),
    }).then((response) => {
      if (response.ok) {
        mylist_container.removeChild(mylist_container.children[index]);
      }
    });
  }
});

function add_to_mylist(listener) {
  var movie_id = listener.parentNode.getAttribute("movie-id");
  movie_id = movie_id | 0;
  if (movie_id) {
    add_item_mylist({
      id: movie_id,
      msg_tage: msg_tage,
      container: mylist_container,
      create_item: create_recommended_item,
    });
  }
}

recommendation_container.addEventListener("click", (event) => {
  add_to_mylist(event.target);
});

horizontal_container.addEventListener("click", (event) => {
  add_to_mylist(event.target);
});

trending_now.addEventListener("click", (event) => {
  add_to_mylist(event.target);
});
