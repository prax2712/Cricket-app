const inn1Button = document.querySelector(".inn1");
const inn2Button = document.querySelector(".inn2");
const inn1Content = document.querySelector(".inn1-content");
const inn2Content = document.querySelector(".inn2-content");

// ... Data Structures
var inn = 0;
inn1Button.addEventListener("click", () => {
  inn1Button.style.border = "3px solid black";
  inn2Button.style.border = "none";
  inn = 1;
  if(inn1Content.style.display=="block"){
    inn1Button.style.border = "none";
    inn1Content.style.display = "none";
  }
  else {
    inn2Content.style.display = "none";
    inn1Content.style.display = "block";

  }
});

inn2Button.addEventListener("click", () => {
  inn2Button.style.border = "3px solid black";
  inn1Button.style.border = "none";
  inn = 2;
  if(inn2Content.style.display=="block"){
    inn2Button.style.border = "none";
    inn2Content.style.display = "none";
  }
  else {
    inn1Content.style.display = "none";
    inn2Content.style.display = "block";
  }
});

var innings1_score = "",
  innings2_score = "";
function buildTableBatting(containerSelector, playerData) {
  const container = document.querySelector(containerSelector);
  container.innerHTML = "Batting";
  const details = document.createElement("p");
  if (inn == 1) details.textContent = innings1_score;
  else details.textContent = innings2_score;
  container.appendChild(details);
  const table = document.createElement("table");
  const headerRow = table.insertRow();
  headerRow.insertCell().textContent = "Batsman";
  headerRow.insertCell().textContent = "Runs";
  headerRow.insertCell().textContent = "Balls";
  headerRow.insertCell().textContent = "4s";
  headerRow.insertCell().textContent = "6s";
  headerRow.insertCell().textContent = "SR";

  playerData.forEach((player) => {
    if (player.balls > 0) {
      const row = table.insertRow();
      row.insertCell().textContent = player.name;
      row.insertCell().textContent = player.runs;
      row.insertCell().textContent = player.balls;
      row.insertCell().textContent = player.fours;
      row.insertCell().textContent = player.sixes;
      row.insertCell().textContent = parseFloat(player.strike_rate).toFixed(2);
    }
  });
  container.appendChild(table);
}
function buildTableBowling(containerSelector, playerData) {
  const container = document.querySelector(containerSelector);
  container.innerHTML = "Bowling";
  table = document.createElement("table");
  headerRow = table.insertRow();
  headerRow.insertCell().textContent = "Bowler";
  headerRow.insertCell().textContent = "Overs";
  headerRow.insertCell().textContent = "Runs";
  headerRow.insertCell().textContent = "Wickets";
  headerRow.insertCell().textContent = "Economy";

  playerData.forEach((player) => {
    if (player.overs > 0) {
      const row = table.insertRow();
      row.insertCell().textContent = player.name;
      row.insertCell().textContent =
        parseInt(player.overs / 6) + "." + (player.overs % 6);
      row.insertCell().textContent = player.bowler_runs;
      row.insertCell().textContent = player.wickets;
      row.insertCell().textContent = player.economy;
    }
  });
  container.appendChild(table);
}

var innings1DataBatting = [];
var innings2DataBatting = [];
var innings1DataBowling = [];
var innings2DataBowling = [];

const match_id = JSON.parse(document.getElementById("match-id").textContent);

const chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/match/" + match_id + "/"
);
function sendMessage() {
  chatSocket.send("hello");
}
chatSocket.onopen = function () {
  console.log("WebSocket connection established!");
  chatSocket.send("hello");
  const intervalId = setInterval(sendMessage, 1000);
};
chatSocket.onerror = function (error) {
  console.error("WebSocket connection error:", error);
};
chatSocket.onmessage = function (event) {
  var data = JSON.parse(event.data);
  if(data.match_status==3){
    window.location.href = "/match_summary/" + match_id;
  }
  document.getElementById("team1").textContent = data.team1;
  document.getElementById("team2").textContent = data.team2;
  document.getElementById("score-value").textContent = data.score + " ";
  document.getElementById("innings_no").textContent = data.innings_no;
  document.getElementById("wickets-value").textContent = " " + data.wickets;
  if (data.strike == 1) {
    document.getElementById("batter1").textContent = data.batter1_name + " *";
  } else {
    document.getElementById("batter1").textContent = data.batter1_name;
  }
  document.getElementById("batter-1-score").textContent = data.batter1_score;
  document.getElementById("batter-1-balls").textContent = data.batter1_balls;
  if (data.strike == 2) {
    document.getElementById("batter2").textContent = data.batter2_name + " *";
  } else {
    document.getElementById("batter2").textContent = data.batter2_name;
  }
  document.getElementById("batter-2-score").textContent = data.batter2_score;
  document.getElementById("batter-2-balls").textContent = data.batter2_balls;
  document.getElementById("bowler-name").textContent = data.bowler_name;
  document.getElementById("bowler-score").textContent =
    data.bowler_runs + "-" + data.bowler_wickets;
  document.getElementById("bowler-overs").textContent =
    "Overs: " + parseInt(data.bowler_balls / 6) + "." + (data.bowler_balls % 6);
  document.getElementById("overs-value").textContent =
    "Overs: " +
    parseInt(data.overs / 6) +
    "." +
    (data.overs % 6) +
    " / " +
    data.maximum_overs;
  if (data.innings_no == 1)
    document.getElementById("target").textContent = "Target: " + "-";
  else document.getElementById("target").textContent = "Target: " + data.target;
  document.getElementById("ball1").textContent = data.overs_timeline[0];
  if(data.overs_timeline[0]=='W'){
    document.getElementById("ball1").style.backgroundColor = "red";
    document.getElementById("ball1").style.color = "white";
  }
  else if(data.overs_timeline[0]=='4'||data.overs_timeline[0]=='6'){
    document.getElementById("ball1").style.backgroundColor = "green";
    document.getElementById("ball1").style.color = "white";
  }
  document.getElementById("ball2").textContent = data.overs_timeline[1];
  if(data.overs_timeline[1]=='W'){
    document.getElementById("ball2").style.backgroundColor = "red";
    document.getElementById("ball2").style.color = "white";
  }
  else if(data.overs_timeline[1]=='4'||data.overs_timeline[1]=='6'){
    document.getElementById("ball2").style.backgroundColor = "green";
    document.getElementById("ball2").style.color = "white";
  }
  document.getElementById("ball3").textContent = data.overs_timeline[2];
  if(data.overs_timeline[2]=='W'){
    document.getElementById("ball3").style.backgroundColor = "red";
    document.getElementById("ball3").style.color = "white";
  }
  else if(data.overs_timeline[2]=='4'||data.overs_timeline[2]=='6'){
    document.getElementById("ball3").style.backgroundColor = "green";
    document.getElementById("ball3").style.color = "white";
  }
  document.getElementById("ball4").textContent = data.overs_timeline[3];
  if(data.overs_timeline[3]=='W'){
    document.getElementById("ball4").style.backgroundColor = "red";
    document.getElementById("ball4").style.color = "white";
  }
  else if(data.overs_timeline[3]=='4'||data.overs_timeline[3]=='6'){
    document.getElementById("ball4").style.backgroundColor = "green";
    document.getElementById("ball4").style.color = "white";
  }
  document.getElementById("ball5").textContent = data.overs_timeline[4];
  if(data.overs_timeline[4]=='W'){
    document.getElementById("ball5").style.backgroundColor = "red";
    document.getElementById("ball5").style.color = "white";
  }
  else if(data.overs_timeline[4]=='4'||data.overs_timeline[4]=='6'){
    document.getElementById("ball5").style.backgroundColor = "green";
    document.getElementById("ball5").style.color = "white";
  }
  document.getElementById("ball6").textContent = data.overs_timeline[5];
  if(data.overs_timeline[5]=='W'){
    document.getElementById("ball6").style.backgroundColor = "red";
    document.getElementById("ball6").style.color = "white";
  }
  else if(data.overs_timeline[5]=='4'||data.overs_timeline[5]=='6'){
    document.getElementById("ball6").style.backgroundColor = "green";
    document.getElementById("ball6").style.color = "white";
  }
  if (data.team1 == data.first_batting) {
    innings1DataBatting = data.team1_players;
    innings2DataBowling = data.team1_players;
    innings1DataBowling = data.team2_players;
    innings2DataBatting = data.team2_players;
  } else {
    innings1DataBatting = data.team2_players;
    innings2DataBowling = data.team2_players;
    innings1DataBowling = data.team1_players;
    innings2DataBatting = data.team1_players;
  }
  var x;
  if (data.toss_winner == data.first_batting) {
    x = "bat";
  } else {
    x = "bowl";
  }
  document.getElementById("toss").textContent =
    data.toss_winner + " won the toss and chose to " + x + " first !";
  if(data.innings_no==1){
    document.getElementById("curr-run-rate").textContent = parseFloat(data.innings1_score_num/parseFloat(data.overs/6)).toFixed(2);
    
  }
  else {
    document.getElementById("curr-run-rate").textContent = parseFloat(data.innings1_score_num/parseFloat(data.overs/6)).toFixed(2);
    document.getElementById("req-run-rate").textContent = parseFloat((data.target - data.innings1_score_num)/parseFloat(((data.maximum_overs)*6 - data.overs)/6)).toFixed(2);
  }
  console.log(data.target-data.innings1_score_num);
  if(data.innings_no==2){
    document.getElementById('need').textContent = "Need " + String(data.target - data.innings1_score_num) + " runs from " + String(data.maximum_overs*6 - data.overs) + " balls"; 
  }
  buildTableBatting(".inn1-batting-container", innings1DataBatting);
  buildTableBowling(".inn1-bowling-container", innings1DataBowling);
  buildTableBatting(".inn2-batting-container", innings2DataBatting);
  buildTableBowling(".inn2-bowling-container", innings2DataBowling);
};