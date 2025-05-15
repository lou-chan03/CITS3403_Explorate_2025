document.addEventListener("DOMContentLoaded", () => {
  const inputField = document.getElementById("guests");
  const popup = document.getElementById("popup");
  const overlay = document.getElementById("overlay");
  const yesButton = document.getElementById("yesButton");
  const noButton = document.getElementById("noButton");
  const nextButton = document.getElementById("nextButton");
  const adventureNameInput = document.getElementById("adventure_name");

  
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
    userChoice = "YES";
    yesButton.classList.add("bg-green-500");
    noButton.classList.remove("bg-green-500");
    closePopup();
  });

  // Handle "No" button click
  noButton.addEventListener("click", () => {
    userChoice = "NO";
    noButton.classList.add("bg-green-500");
    yesButton.classList.remove("bg-green-500");
    closePopup();
  });
  console.log("hello123")
  
  console.log(nextButton);
  if (nextButton) {
      console.log("hello1234")
      nextButton.addEventListener("click", () => {
          
          console.log("hello")
          const adventureName = adventureNameInput.value;
          // Prepare the data to be sent to the server
          const tripData = {
              adults: counts.adults,
              children: counts.children,
              pets: counts.pets,
              choice: userChoice,
              adventure_name: adventureName
          };
          const yesUrl = nextButton.dataset.yesUrl;
          const noUrl = nextButton.dataset.noUrl;
         
        
          fetch("/questions", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
              },
              body: JSON.stringify(tripData),
          })
              .then((response) => {
                  if (response.ok) {
                      return response.text();
                  } else {
                      throw new Error("Failed to save trip details.");
                  }
              })
              .then((html) => {
                document.open();
                document.write(html);
                document.close();

                // Redirect based on the user's choice
                console.log("Redirecting based on user choice...");
                if (userChoice === "Yes" && yesUrl) {
                    window.location.href = yesUrl;
                } else if (userChoice === "No" && noUrl) {
                    window.location.href = noUrl;
                } else {
                    console.warn("No valid redirection URL provided.");
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Something went wrong while saving your trip.");
            });
      });
  }


  // Function to close popup
  function closePopup() {
    setTimeout(() => {
      popup.style.display = "none";
      overlay.style.display = "none";
      inputField.value = `${counts.adults} Adults, ${counts.children} Children, ${counts.pets} Pets`;
    }, 200);
  }
});

  