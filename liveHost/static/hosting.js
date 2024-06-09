const team1Input = document.getElementById("team1Name");
const team2Input = document.getElementById("team2Name");
const messageElement = document.getElementById("message");

function validateTeamNames() {
    const team1 = team1Input.value.trim();
    const team2 = team2Input.value.trim();
    let isValid = true;  // Flag to track overall validity

    if (team1.length < 3) {
        team1Input.setCustomValidity("Team 1 name must be at least 3 characters long.");
        messageElement.textContent = "Team 1 name must be at least 3 characters long.";
        messageElement.style.color = "red";
        isValid = false;  // Set the flag to false if validation fails
    } else {
        team1Input.setCustomValidity("");
    }

    if (team2.length < 3) {
        team2Input.setCustomValidity("Team 2 name must be at least 3 characters long.");
        messageElement.textContent = "Team 2 name must be at least 3 characters long.";
        messageElement.style.color = "red";
        isValid = false;  // Set the flag to false if validation fails
    } else {
        team2Input.setCustomValidity("");
    }

    if (team1 === team2) {
        team2Input.setCustomValidity("Team names must not be the same.");
        messageElement.textContent = "Team names must not be the same.";
        messageElement.style.color = "red";
        isValid = false;  // Set the flag to false if validation fails
    } else {
        if (team1.length >= 3 && team2.length >= 3 && team1 !== team2) {
            messageElement.textContent = ""; // Clear message if names are valid
        }
        team2Input.setCustomValidity("");
    }

    return isValid;  // Return the overall validity status
}

team1Input.addEventListener("input", validateTeamNames);
team2Input.addEventListener("input", validateTeamNames);

document.getElementById('teamForm').addEventListener('submit', function(event) {
    if (!validateTeamNames()) {  // Check overall validity status
        event.preventDefault();  // Prevent form submission if invalid
    }
});