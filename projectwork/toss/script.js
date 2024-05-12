const team1Button = document.getElementById('team1-button');
const team2Button = document.getElementById('team2-button');
const batButton = document.getElementById('bat-button');
const bowlButton = document.getElementById('bowl-button');
const teamButtonsSection = document.querySelector('.team-buttons');
const choiceButtonsSection = document.querySelector('.choice-buttons');
const tossResult = document.querySelector('.toss-result');
const decideText = document.querySelector('#decide');

let tossWinner = null;  

function handleTeamClick(teamName) {
  tossWinner = teamName; 
  tossResult.textContent = teamName +" won the toss!";

  // Remove 'selected' from team buttons
  team1Button.classList.remove('selected');
  team2Button.classList.remove('selected'); 

  // Add 'selected' to the clicked button
  if (teamName === "Team 1") {
    team1Button.classList.add('selected');
  } else {
    team2Button.classList.add('selected');
  }
  decideText.textContent='Decide:';
  choiceButtonsSection.style.display = 'flex'; // Show choice buttons
}

function handleChoiceClick(choice) {
  // Remove 'selected' from choice buttons
  batButton.classList.remove('selected'); 
  bowlButton.classList.remove('selected'); 

  // Add 'selected' to the clicked button
  if (choice === "bat") {
    batButton.classList.add('selected');
  } else {
    bowlButton.classList.add('selected');
  } 

  
  // Replace the console.log with your code to load the scorecard here
  const startMatchSection = document.querySelector('.start-match-section');
  startMatchSection.style.display = 'block';
}

team1Button.addEventListener('click', () => handleTeamClick("Team 1"));
team2Button.addEventListener('click', () => handleTeamClick("Team 2"));
batButton.addEventListener('click', () => handleChoiceClick("bat"));
bowlButton.addEventListener('click', () => handleChoiceClick("bowl"));