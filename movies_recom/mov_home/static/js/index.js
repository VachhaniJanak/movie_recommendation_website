// Sleep function
function sleep(time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

// Function to add a movie in mylist using movie id
export function add_item_mylist({
  id,
  msg_tage = "",
  container = "",
  create_item = "",
}) {
  fetch("/api/addtomylist", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getcsrftoken,
    },
    body: JSON.stringify({ movieid: id }),
  })
    .then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          if (data.msg) {
            msg_tage.lastElementChild.innerText = data.msg;
            msg_tage.style.visibility = "visible";
            sleep(4000).then(() => {
              msg_tage.style.visibility = "hidden";
            });
            if (container && data.movie) {
              container.prepend(
                create_item({
                  base_url: base_url,
                  movie: data.movie,
                  add_icon: false,
                  class_name: "mylists-items",
                })
              );
            }
          }
        });
      } else {
        // Handle the error if the response is not successful
        console.error(
          "Failed to add item:",
          response.status,
          response.statusText
        );
      }
    })
    .catch((error) => {
      // Handle network errors
      console.error("Network error:", error);
    });
}
