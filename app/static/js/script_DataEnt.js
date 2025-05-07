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
    console.log("hello123")
    // Handle "Next" button click
    
    // nextButton.addEventListener("click", () => {
    //     if (userChoice === "") {
    //       alert("Please make a choice (Yes or No).");
    //       return;
    //     }
    //     const total = counts.adults + counts.children + counts.pets; // Calculate the total
    //     const baseURL = userChoice === "Yes" ? "{{ url_for('email_share') }}" : "{{ url_for('questions') }}";
    //     const url = `${baseURL}?total=${total}`;
    //     window.location.href = url; // Redirect with the total passed as a query parameter
    //   });
    // if (nextButton) {
    //     nextButton.addEventListener("click", () => {
    //         const userChoice = "No"; // Replace with logic to get user choice
    //         const yesUrl = nextButton.dataset.yesUrl;
    //         const noUrl = nextButton.dataset.noUrl;

    //         if (userChoice === "Yes") {
    //             window.location.href = yesUrl; // Redirect to "email_share" page
    //         } else {
    //             window.location.href = noUrl; // Redirect to "questions" page
    //         }
    //     });
    // }
    console.log(nextButton);
    if (nextButton) {
        console.log("hello1234")
        nextButton.addEventListener("click", () => {
            // if (userChoice === "No") {
            //   alert("Please make a choice (Yes or No).");
            //   return;
            // }
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
            console.log("hello12345")
            // Send the trip data to the backend using a POST request
            // fetch("/save_trip", {
            //     method: "POST",
            //     headers: {
            //         "Content-Type": "application/json"
            //     },
            //     body: JSON.stringify(tripData)
            // })
            // .then(response => response.json())
            // .then(data => {
            //     if (data.success) {
            //         // Redirect based on the user's choice
            //         const yesUrl = nextButton.dataset.yesUrl;
            //         const noUrl = nextButton.dataset.noUrl;
            //         console.log("hi");
            //         console.log(nextButton.dataset);

            //         if (userChoice === "Yes") {
            //             window.location.href = yesUrl; // Redirect to "email_share" page
            //         } else {
            //             window.location.href = noUrl; // Redirect to "questions" page
            //         }
            //     } else {
            //         alert("Error saving trip details.");
            //     }
            // })
            // .catch(error => {
            //     console.error("Error:", error);
            //     alert("Something went wrong while saving your trip.");
            // });

            // fetch("/questions", {
            //     method: "POST",
            //     headers: {
            //         "Content-Type": "application/json",
            //     },
            //     body: JSON.stringify(tripData),
            // })
            //     .then((response) => {
            //         if (response.ok) {
            //             return response.text();
            //         } else {
            //             throw new Error("Failed to save trip details.");
            //         }
            //     })
            //     .then((html) => {
            //         document.open();
            //         document.write(html);
            //         document.close();
            //     })
            //     .catch((error) => {
            //         console.error("Error:", error);
            //         alert("Something went wrong while saving your trip.");
            //     });

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
  