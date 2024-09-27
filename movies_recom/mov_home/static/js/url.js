const fullUrl = window.location.href;
const protocol = window.location.protocol;
const hostname = window.location.hostname;
const port = window.location.port;

function getcoolies_items(item_name) {
  let item_value = null;
  const cookies = document.cookie.split(";");
  cookies.forEach((cookie) => {
    const [name, value] = cookie.trim().split("=");
    if (name === item_name) {
      item_value = decodeURIComponent(value);
    }
  });
  return item_value;
}

const base_url = protocol + "//" + hostname + ":" + port;
const getcsrftoken = getcoolies_items("csrftoken");
