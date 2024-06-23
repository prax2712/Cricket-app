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
      
document.getElementById('profile-img').addEventListener('click', function() {
  const profileInfo = document.getElementById('profile-info');
  profileInfo.style.display = profileInfo.style.display === 'none' ? 'block':'none';
});
document.addEventListener("DOMContentLoaded", function() {
  var loginButton = document.getElementById("login-button");
  var logoutButton = document.getElementById("logout-button");

  if (loginButton) {
    loginButton.onclick = function() {
      window.location.href = "http://127.0.0.1:8000/login";
    }
  }

  if (logoutButton) {
    logoutButton.onclick = function() {
      window.location.href = "http://127.0.0.1:8000/logout";
    }
  }
});
