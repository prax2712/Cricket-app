const searchInput = document.getElementById('searchInput');
const suggestionsBox = document.getElementById('suggestions');
const playerStatsTable = document.querySelector('.player-stats');

searchInput.addEventListener('input', async () => {
    console.log('bitch im in');
  const query = searchInput.value;
  if (query.length < 1) {  // Show suggestions only if the query is at least 2 characters long
    suggestionsBox.innerHTML = '';
    return;
  }

  // Fetch suggestions from the server (see Django view below)
  const response = await fetch({% url 'player_suggestions' %}?q=${query}); 
  const data = await response.json();

  // Display suggestions
  suggestionsBox.innerHTML = '';  // Clear previous suggestions
  if (data.length > 0) {
    const suggestionsList = document.createElement('ul');
    data.forEach(player => {
      const listItem = document.createElement('li');
      listItem.textContent = ${player.first_name} ${player.last_name} (${player.username});
      listItem.addEventListener('click', () => {
        searchInput.value = player.username;
        suggestionsBox.innerHTML = ''; // Hide suggestions after selecting
      });
      suggestionsList.appendChild(listItem);
    });
    suggestionsBox.appendChild(suggestionsList);
    
  }
});