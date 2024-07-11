const joinButton = document.querySelector(".join-button");
const closeButton = document.querySelector(".close-button");
const closeButton1 = document.querySelector(".close-button1");
const signUpModal = document.querySelector(".sign-up-modal");
const loginLink = document.querySelector(".login-link");
const loginModal = document.querySelector(".login-modal");
const signUpLink = document.querySelector(".signup-link");

const signUpForm = document.getElementById("signup-form");
const passwordInput = document.getElementById("password");
const confirmPasswordInput = document.getElementById("confirm-password");
const passwordMismatchError = document.getElementById("password-mismatch-error");

const enableModal = document.getElementById("modal-enable");
const enable = enableModal.textContent;

const storedUsername = localStorage.getItem('referralUserneme');
const storedPassword = localStorage.getItem('referralPassword');
// Fill in the password field if it exists
if (storedPassword && storedUsername) {
    document.getElementById('emailId1').value = storedUsername;
    document.getElementById('password1').value = storedPassword;
}

if(enable === "true"){
    signUpModal.style.display = "block";
    loginModal.style.display = "none";
};
if(document.getElementById("modal-enableLogIn").textContent === "true"){
    loginModal.style.display = "block";
    signUpModal.style.display = "none";
};

// Join Button Click
joinButton.addEventListener("click", () => {
    signUpModal.style.display = "block";
});

// Closing The Modals
closeButton.addEventListener("click", () => {
    signUpModal.style.display = "none";
});

closeButton1.addEventListener("click", () => {
    loginModal.style.display = "none";
});

// Click on login text

loginLink.addEventListener("click", () => {
    signUpModal.style.display = "none";
    loginModal.style.display = "block";
});

// Click on sign up text

signUpLink.addEventListener("click", () => {
    signUpModal.style.display = "block";
    loginModal.style.display = "none";
});

// Reset error message on input change
passwordInput.addEventListener("input", () => {
    passwordMismatchError.style.display = "none";
});

confirmPasswordInput.addEventListener("input", () => {
    passwordMismatchError.style.display = "none";
});


// Blur the background

// Add an event listener to the form submission
document.getElementById("signup-form").addEventListener('submit', function (event) {
    if (passwordInput.value !== confirmPasswordInput.value) {
        passwordMismatchError.style.display = "block";
        event.preventDefault();
        return; // Stop form submission if passwords don't match
      }

    // Store the password in local storage
    localStorage.setItem('referralUserneme', document.getElementById('emailId').value);
    localStorage.setItem('referralPassword', document.getElementById('password').value);
});

// Add an event listener to the form submission for login
document.getElementById("loginFrom").addEventListener('submit', function (event) {
    

    // Store the password in local storage
    localStorage.setItem('referralUserneme', document.getElementById('emailId1').value);
    localStorage.setItem('referralPassword', document.getElementById('password1').value);
});