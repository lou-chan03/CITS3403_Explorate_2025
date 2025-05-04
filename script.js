
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
  document.addEventListener("DOMContentLoaded", () => {
    const inputField = document.getElementById("guests");
    const popup = document.getElementById("popup");
    const overlay = document.getElementById("overlay");
    const yesButton = document.getElementById("yesButton");
    const noButton = document.getElementById("noButton");
    const nextButton = document.getElementById("nextButton");
    
    let userChoice = "NO"; // Stores user choice ("Yes" or "No")
    const counts = {
      adults: 1,
      children: 0,
      pets: 0,
    };
  
    // Show the popup when the input field is clicked
    inputField.addEventListener("click", () => {
      popup.style.display = "block";
      overlay.style.display = "block";
    });
  
    // Close popup when overlay is clicked
    overlay.addEventListener("click", () => closePopup());
  
    // Increment buttons logic
    document.querySelectorAll(".increment").forEach((button) => {
      button.addEventListener("click", () => {
        const target = button.dataset.target;
        counts[target]++;
        document.getElementById(target).textContent = counts[target];
      });
    });
  
    // Decrement buttons logic
    document.querySelectorAll(".decrement").forEach((button) => {
      button.addEventListener("click", () => {
        const target = button.dataset.target;
        if (counts[target] > 0) {
          counts[target]--;
          document.getElementById(target).textContent = counts[target];
        }
      });
    });
  
    // Handle "Yes" button click
    yesButton.addEventListener("click", () => {
      userChoice = "Yes";
      yesButton.classList.add("bg-green-500");
      noButton.classList.remove("bg-green-500");
      closePopup();
    });
  
    // Handle "No" button click
    noButton.addEventListener("click", () => {
      userChoice = "No";
      noButton.classList.add("bg-green-500");
      yesButton.classList.remove("bg-green-500");
      closePopup();
    });
  
    // Handle "Next" button click
    nextButton.addEventListener("click", () => {
      if (userChoice === "") {
        alert("Please make a choice (Yes or No).");
      } else if (userChoice === "Yes") {
        window.location.href = "Email_Share.html"; // Replace with "Yes" page URL
      } else {
        window.location.href = "Data_Ent_Q1.html"; // Replace with "No" page URL
      }
    });
  
    // Function to close popup
    function closePopup() {
      setTimeout(() => {
        popup.style.display = "none";
        overlay.style.display = "none";
        inputField.value = `${counts.adults} Adults, ${counts.children} Children, ${counts.pets} Pets`;
      }, 200);
    }
  });
  