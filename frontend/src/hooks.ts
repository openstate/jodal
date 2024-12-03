// import { identity } from "$lib/stores";
// import { get } from "svelte/store";

// // isLoggedIn function that checks logged_in cookie which is 1 or 0
// function isLoggedIn() {
//   const cookie = document.cookie
//     .split(";")
//     .find((cookie) => cookie.includes("logged_in"));
//   return cookie ? cookie.split("=")[1] === "1" : false;
// }

// export const reroute = ({ url }) => {
//   if (url.pathname === "/") return isLoggedIn() ? "/app" : "/home";
//   if (url.pathname === "/__data.json")
//     return isLoggedIn() ? "/app/__data.json" : "/home/__data.json";
// };
