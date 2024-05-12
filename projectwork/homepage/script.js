
let upcoming = document.getElementById("upcoming");
upcoming.addEventListener("click", () => {
  document.getElementById("tab-content-upcoming").style.display = "block";
  document.getElementById("tab-content-live").style.display = "none";
  document.getElementById("tab-content-recent").style.display = "none";
  document.getElementById("live").style.backgroundColor = "rgb(255,255,255)";
  document.getElementById("upcoming").style.backgroundColor = "rgb(40, 159, 149)";
  document.getElementById("recent").style.backgroundColor = "rgb(255,255,255)";
});

let live = document.getElementById("live");
live.addEventListener("click", () => {
  document.getElementById("tab-content-live").style.display = "block";
  document.getElementById("tab-content-upcoming").style.display = "none";
  document.getElementById("tab-content-recent").style.display = "none";
  document.getElementById("live").style.backgroundColor = "rgb(40, 159, 149)";
  document.getElementById("upcoming").style.backgroundColor = "rgb(255,255,255)";
  document.getElementById("recent").style.backgroundColor = "rgb(255,255,255)";
});

let recent = document.getElementById("recent");
recent.addEventListener("click", () => {
  document.getElementById("tab-content-recent").style.display = "block";
  document.getElementById("tab-content-live").style.display = "none";
  document.getElementById("tab-content-upcoming").style.display = "none";
  document.getElementById("live").style.backgroundColor = "rgb(255,255,255)";
  document.getElementById("upcoming").style.backgroundColor = "rgb(255,255,255)";
  document.getElementById("recent").style.backgroundColor = "rgb(40, 159, 149)";
});


