function wait(time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

export async function fetchMovies({ request_url, present_count}) {
  try {
    const res = await fetch(request_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getcsrftoken,
      },
      body: JSON.stringify({present_count: present_count }),
    });
    if (!res.ok) {
      throw new Error(`HTTP error! Status: ${res.status}`);
    }
    const data = await res.json();
    return data.movies;
  } catch (error) {
    console.error("Error fetching movies:", error);
    throw error;
  }
}
