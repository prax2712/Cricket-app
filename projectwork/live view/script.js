const inn1Button = document.querySelector('.inn1');
const inn2Button = document.querySelector('.inn2');
const inn1Content = document.querySelector('.inn1-content');
const inn2Content = document.querySelector('.inn2-content');

// ... Data Structures 

inn1Button.addEventListener('click', () => {
    showInningsContent(inn1Content, inn2Content);
    buildTableBatting('.inn1-batting-container', innings1DataBatting);
    buildTableBowling('.inn1-bowling-container', innings1DataBowling);
});

inn2Button.addEventListener('click', () => {
    showInningsContent(inn2Content, inn1Content); 
    buildTableBatting('.inn2-batting-container', innings2DataBatting);
    buildTableBowling('.inn2-bowling-container', innings2DataBowling);
});

function showInningsContent(contentToShow, contentToHide) {
    contentToShow.style.display = 'block';
    contentToHide.style.display = 'none';
}
function buildTableBatting(containerSelector, playerData) {
    const container = document.querySelector(containerSelector);
    container.innerHTML = 'Batting';
    const table = document.createElement('table');
    const headerRow = table.insertRow();  
    headerRow.insertCell().textContent = "Batsman";
    headerRow.insertCell().textContent = "Runs";
    headerRow.insertCell().textContent = "Balls";
    headerRow.insertCell().textContent = "4s";
    headerRow.insertCell().textContent = "6s";
    headerRow.insertCell().textContent = "SR";
    headerRow.insertCell().textContent = "Status";

    playerData.forEach(player => {
        const row = table.insertRow();
        row.insertCell().textContent = player.name;
        row.insertCell().textContent = player.runs;
        row.insertCell().textContent = player.balls;
        row.insertCell().textContent = player.fours;
        row.insertCell().textContent = player.sixes;
        row.insertCell().textContent = player.sr;
        row.insertCell().textContent = player.status;
    });
    container.appendChild(table);
   
}
function buildTableBowling(containerSelector, playerData) {
 const container = document.querySelector(containerSelector);
container.innerHTML = 'Bowling';
table = document.createElement('table');
headerRow = table.insertRow();  
headerRow.insertCell().textContent = "Bowler";
headerRow.insertCell().textContent = "Overs";
headerRow.insertCell().textContent = "Maidens";
headerRow.insertCell().textContent = "Runs";
headerRow.insertCell().textContent = "Wickets";
headerRow.insertCell().textContent = "Economy";

playerData.forEach(player => {
   const row = table.insertRow();
   row.insertCell().textContent = player.name;
   row.insertCell().textContent = player.overs;
   row.insertCell().textContent = player.maidens;
   row.insertCell().textContent = player.runs;
   row.insertCell().textContent = player.wickets;
   row.insertCell().textContent = player.economy;
});
container.appendChild(table);
}

const innings1DataBatting = [
    { name: "Player 1", runs: 25, balls: 20, sr: 125, fours: 2, sixes: 1, status: "Out" },

 ];
 const innings2DataBatting = [ 

 ];

const innings1DataBowling=[
    { name:"Player 1", overs:3 , maidens:0 , runs: 25 ,wickets:2, economy:6.9}

];
const innings2DataBowling=[
    { name:"Player 69", overs:4 , maidens:1 , runs: 35 ,wickets:0, economy:7.8}

];