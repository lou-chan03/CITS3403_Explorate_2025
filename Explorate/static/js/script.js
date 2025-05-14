
const loginToggle = document.getElementById('login-toggle');
const signupToggle = document.getElementById('signup-toggle');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
        
loginToggle.addEventListener('click', () => {
    loginToggle.classList.add('active');
    signupToggle.classList.remove('active');
    loginForm.style.display = 'block';
    signupForm.style.display = 'none';
});
        
signupToggle.addEventListener('click', () => {
    signupToggle.classList.add('active');
    loginToggle.classList.remove('active');
    signupForm.style.display = 'block';
    loginForm.style.display = 'none';
});


window.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const formType = params.get("form"); // 'login' or 'signup'
  
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");
  
    if (formType === "signup") {
      loginForm.style.display = "none";
      signupForm.style.display = "block";
    } else {
      loginForm.style.display = "block";
      signupForm.style.display = "none";
    }
  });
  
  document.addEventListener("DOMContentLoaded", function () {
        const flashMessages = document.getElementById("flash-messages");
        if (flashMessages) {
            setTimeout(() => {
                flashMessages.style.transition = "opacity 0.5s";
                flashMessages.style.opacity = "0";
                setTimeout(() => flashMessages.remove(), 500); // Ensure complete removal from DOM
            }, 5000); // Adjust timing as needed (5000ms = 5 seconds)
        }
    });
