// Toggle between login and signup forms
const loginToggle = document.getElementById('login-toggle');
const signupToggle = document.getElementById('signup-toggle');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');


// Event listener for toggling forms via buttons
loginToggle.addEventListener('click', () => {
   loginToggle.classList.add('active');
   signupToggle.classList.remove('active');
   loginForm.style.display = 'block';
   signupForm.style.display = 'none';
   history.replaceState(null, '', '?form=login'); // Update URL without reload
});


signupToggle.addEventListener('click', () => {
   signupToggle.classList.add('active');
   loginToggle.classList.remove('active');
   signupForm.style.display = 'block';
   loginForm.style.display = 'none';
   history.replaceState(null, '', '?form=signup'); // Update URL without reload
});


// Handle initial form state based on URL parameter
window.addEventListener("DOMContentLoaded", () => {
   const params = new URLSearchParams(window.location.search);
   const formType = params.get("form"); // 'login' or 'signup'


   if (formType === "signup") {
       loginToggle.classList.remove('active');
       signupToggle.classList.add('active');
       loginForm.style.display = 'none';
       signupForm.style.display = 'block';
   } else {
       loginToggle.classList.add('active');
       signupToggle.classList.remove('active');
       loginForm.style.display = 'block';
       signupForm.style.display = 'none';
   }


   // Flash messages fade out
   const flashMessages = document.getElementById("flash-messages");
   if (flashMessages) {
       setTimeout(() => {
           flashMessages.style.transition = "opacity 0.5s";
           flashMessages.style.opacity = "0";
           setTimeout(() => flashMessages.remove(), 500); // Ensure complete removal from DOM
       }, 5000); // Adjust timing as needed
   }
});
