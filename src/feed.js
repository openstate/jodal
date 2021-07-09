// https://css-tricks.com/how-to-fetch-and-parse-rss-feeds-in-javascript/
function fetch_feed(feed, callback) {
  return fetch(feed)
  .then(response => response.text())
  .then(str => new window.DOMParser().parseFromString(str, "text/xml"))
  .then(function(data) {
    var parsed = {
      items: []
    };
    const items = data.querySelectorAll("item");
    items.forEach(function (el) {
      var result = {
        title: el.querySelector("title").innerHTML,
        link: el.querySelector("link").innerHTML,
        guid: el.querySelector("guid").innerHTML,
        description: el.querySelector("description").innerHTML,
        date: el.querySelector("pubDate").innerHTML
      };
      parsed.items.append(result);
    });
    callback(parsed);
  })
}
