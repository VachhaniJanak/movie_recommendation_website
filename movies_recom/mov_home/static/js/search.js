function redirect() {
  const query = document.getElementById("search-input").value.trim();
  if (query !== "") {
    window.location.href = `/home/result?query=${encodeURIComponent(query)}`;
  }
}

function showSuggestions() {
  const searchcontainer = document.getElementById(
    "search-suggestion-container"
  );
  const input = document.getElementById("search-input").value.toLowerCase();
  const suggestionList = document.getElementById("suggestion-list");
  searchcontainer.style.visibility = "hidden";
  count = -1;
  if (input.trim() !== "") {
    fetch(`/api/search?query=${encodeURIComponent(input.trim())}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        suggestionList.innerHTML = "";
        data.suggestions.forEach((suggestion) => {
          const li = document.createElement("li");
          const i = document.createElement("i");
          i.classList.add("fa", "fa-search");
          li.appendChild(i);
          i.textContent = " " + suggestion;
          li.addEventListener("click", () => {
            document.getElementById("search-input").value = suggestion;
            suggestionList.innerHTML = "";
          });
          suggestionList.appendChild(li);
        });
      });
    searchcontainer.style.visibility = "visible";
  }
}

function showGenreList() {
  const genrelistcontainer = document.getElementById("genre-list-container");
  genrelistcontainer.style.visibility = "visible";
  flag = true;
}

document.addEventListener("click", (event) => {
  const suggestionList = document.getElementById("suggestion-list");
  if (event.target !== document.getElementById("search-input")) {
    suggestionList.innerHTML = "";
  }
  const searchcontainer = document.getElementById(
    "search-suggestion-container"
  );
  searchcontainer.style.visibility = "hidden";
  if (event.target !== document.getElementById("genre")) {
    const genrelistcontainer = document.getElementById("genre-list-container");
    genrelistcontainer.style.visibility = "hidden";
  }
});

document.getElementById("search-input").addEventListener("keydown", (event) => {
  const suggestionList = document.getElementById("suggestion-list");
  const items = suggestionList.getElementsByTagName("li");

  if (event.key === "ArrowDown") {
    if (count > -1) {
      items[count].classList.remove("selected");
    }
    if (count < items.length - 1) {
      count = count + 1;
      items[count].classList.add("selected");
    } else {
      items[0].classList.add("selected");
      count = 0;
    }
  }

  if (event.key === "ArrowUp") {
    if (count > -1) {
      items[count].classList.remove("selected");
    }
    if (count > 0) {
      count = count - 1;
      items[count].classList.add("selected");
    } else {
      items[items.length - 1].classList.add("selected");
      count = items.length - 1;
    }
  }

  if (event.key === "Enter") {
    if (count > -1) {
      items[count].click();
    }
    redirect();
  }

  if (event.key === "Escape") {
    const searchcontainer = document.getElementById(
      "search-suggestion-container"
    );
    searchcontainer.style.visibility = "hidden";
    count = 0;
  }
});
