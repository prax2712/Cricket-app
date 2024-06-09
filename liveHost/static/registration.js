const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const passwordError = document.getElementById("password_error");

function validateForm() {
    const username = usernameInput.value;
    const password = passwordInput.value;
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    const hasDigit = /\d/.test(password);
    if (username.length < 5) {
        usernameInput.setCustomValidity("Username must be at least 5 characters long.");
    } else {
        usernameInput.setCustomValidity("");
    }

    if (password.length < 8 || !hasSpecialChar || !hasDigit) {
        passwordError.textContent = "Password must contain at least one special character and one digit, and be at least 8 characters long.";
        passwordInput.setCustomValidity("Invalid password");
    } else {
        passwordError.textContent = ""; // Clear any previous error message
        passwordInput.setCustomValidity(""); // Clear the custom validation message
    }
}
usernameInput.addEventListener("input", validateForm);
passwordInput.addEventListener("input", validateForm);