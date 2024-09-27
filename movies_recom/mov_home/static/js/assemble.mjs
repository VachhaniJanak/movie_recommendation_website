import { fetchMovies } from "./featch_data.mjs";

export const clientheight = document.documentElement.clientHeight;
export const clientwidth = document.documentElement.clientWidth;

export async function load_on_load({
  container,
  url_path,
  screen_dim,
  along_height,
  offset,
  create_item,
  class_name = "",
  add_icon = true,
}) {
  let max_limit = 100;
  let count = 0;
  let flag = true;
  let scroll_dim;
  while (flag && count < max_limit) {
    count += 1;
    const movies = await fetchMovies({
      request_url: url_path,
      present_count: container.childElementCount,
    });
    try {
      if (movies.length == 0) flag = false;
      for (const movie of movies) {
        if (along_height) {
          scroll_dim = container.scrollHeight;
        } else {
          scroll_dim = container.scrollWidth;
        }
        if (screen_dim + offset < scroll_dim) {
          flag = false;
        }
        container.appendChild(
          create_item({
            base_url: base_url,
            movie: movie,
            class_name: class_name,
            add_icon: add_icon,
          })
        );
      }
    } catch (error) {
      console.error("Failed to fetch movies:", error);
      flag = false;
      break;
    }
  }
}

export async function get_movies_on_scroll({
  url_path,
  container,
  create_item,
  add_icon = true,
  class_name = "",
}) {
  const movies = await fetchMovies({
    request_url: url_path,
    present_count: container.childElementCount,
  });

  for (const movie of movies) {
    container.appendChild(
      create_item({
        base_url: base_url,
        movie: movie,
        add_icon: add_icon,
        class_name: class_name,
      })
    );
  }
}
