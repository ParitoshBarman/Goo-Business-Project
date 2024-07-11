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

// Join Button Click
joinButton.addEventListener("click", () => {

    if(enable === "false")
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

// submit on signup

signUpForm.addEventListener("submit", (event) => {
    event.preventDefault();
    
    if (passwordInput.value !== confirmPasswordInput.value) {
      passwordMismatchError.style.display = "block";
      return; // Stop form submission if passwords don't match
    }

    const formData = new FormData(signUpForm);
    const email = formData.get("email");
    const password = formData.get("password");

    // Storing username and password in local storage
    localStorage.setItem("refusername", email);
    localStorage.setItem("refpassword", password);

    // Clearing the form
    // signUpForm.submit();
      
    // Closing the signup modal
    // const signUpModal = document.querySelector(".sign-up-modal");
    // const modalOverlay = document.querySelector(".modal-overlay");
    signUpModal.style.display = "none";
    modalOverlay.style.display = "none";

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
document.querySelector("form").addEventListener('submit', function (event) {
    // Store the password in local storage
    localStorage.setItem('employeeUserneme', document.getElementById('username').value);
    localStorage.setItem('employeePassword', document.getElementById('password').value);
});