document.addEventListener("DOMContentLoaded", () => {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const inputField = document.getElementById("guests");
    const popup = document.getElementById("popup");
    const overlay = document.getElementById("overlay");
    const yesButton = document.getElementById("yesButton");
    const noButton = document.getElementById("noButton");
    const nextButton = document.getElementById("next-button");
    const prevButton = document.getElementById("prev-button");
    const buttonsContainer = document.querySelector('.buttons-container');
    const contentBox = document.querySelector('.content-box');
    const progressBar = document.getElementById('progress-bar');
    let currentQuestionIndex = 0;
    let progressPercentage = 20;

    const questions = [
        {
            question: 'What climate do you like?',
            options: ['Hot', 'Cold', 'Tropical'],
            image: 'https://i.postimg.cc/NjhF7F5L/Gemini-Generated-Image-gw1crzgw1crzgw1c-1.png'
        },
        {
            question: 'Choose your interest!',
            options: ['Nature', 'Outback', 'Beaches'],
            image: 'https://i.postimg.cc/8cz8shWq/accommodation-image.png'
        },
        {
            question: 'Choose your scenery!',
            options: ['Wildlife', 'Mountain', 'Coastal/Scenic Drive'],
            image: 'https://i.postimg.cc/jdD8PFL9/activities-image.png'
        },
        {
            question: 'Choose your activities!',
            options: ['Adventure', 'Family', 'Sports'],
            image: 'https://i.postimg.cc/jdD8PFL9/activities-image.png'
        },
        {
            question: 'Anything interest you?',
            options: ['Heritage', 'Art', 'Landmarks'],
            image: 'https://i.postimg.cc/jdD8PFL9/activities-image.png'
        }
    ];

    const userSelections = []; // Store the selected answers for each question

    // Function to update the content box
    function updateContent() {
        const currentQuestion = questions[currentQuestionIndex];

        // Update the question and options
        contentBox.querySelector('.question').textContent = currentQuestion.question;
        buttonsContainer.innerHTML = '';
        currentQuestion.options.forEach(option => {
            const button = document.createElement('button');
            button.classList.add('climate-button');
            button.textContent = option;
            button.addEventListener('click', () => {
                // If the button already has the "pressed" class, remove it
                if (button.classList.contains('pressed')) {
                    button.classList.remove('pressed');
                } else {
                    // Otherwise, remove "pressed" from all buttons and add it to the clicked one
                    document.querySelectorAll('.climate-button').forEach(btn => btn.classList.remove('pressed'));
                    button.classList.add('pressed');
                    userSelections[currentQuestionIndex] = option; // Store the selected option
                }
            });
            buttonsContainer.appendChild(button);
        });

        // Update the image
        const image = contentBox.querySelector('.climate-image');
        image.src = currentQuestion.image;

        // Update the Next button to Finish on the last question
        if (currentQuestionIndex === questions.length - 1) {
            nextButton.textContent = 'Finish';
            nextButton.removeEventListener('click', nextButtonHandler);  // Remove previous next button event
            nextButton.addEventListener('click', finishButtonHandler);  // Add finish button event
        } else {
            nextButton.textContent = 'Next';
            nextButton.removeEventListener('click', finishButtonHandler);  // Remove finish button event
            nextButton.addEventListener('click', nextButtonHandler);  // Add next button event
        }
    }

    // Next button handler
    function nextButtonHandler() {
        if (currentQuestionIndex < questions.length - 1) {
            currentQuestionIndex++;
            updateContent();  // Change content
            updateProgress(20); // Increase progress
        }
    }

    // Finish button handler (send data to backend)
    // 
    
    function finishButtonHandler() {
    // Ensure all questions have been answered before proceeding
    if (userSelections.length < questions.length || userSelections.some(selection => !selection)) {
        alert("Please answer all questions before proceeding.");
        return;
    }

    // Retrieve adventure_id from the hidden input field
    var adventure_id = document.getElementById('adventure-id').value;
    var user_id = document.getElementById('user-id').value;
    console.log("Adventure ID:", adventure_id); // Verify it's being retrieved

    // Check if the loading indicator exists
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.style.display = 'block'; // Show loading indicator
    } else {
        console.warn("Loading indicator element is missing from the DOM.");
    }

    // Send the selected options to the backend
    fetch('/save_selections', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': csrfToken // Include CSRF token for security
        },
        body: JSON.stringify({ selections: userSelections, adventure_id: adventure_id ,user_id:user_id}) // Send the adventure_id along
    })
    .then(response => {
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none'; // Hide loading indicator
        }
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.message === 'Data saved successfully') {
            sessionStorage.setItem("recommendationResult", JSON.stringify(data));
            alert('Selections saved successfully! Redirecting...');

            window.location.href = "/index"; // Redirect or perform any other action
        } else {
            alert(`Error saving data: ${data.message || 'Unknown error.'}`);
        }
    })
    .catch(error => {
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none'; // Hide loading indicator
        }
        console.error("Error:", error);
        alert('An error occurred while saving your data. Please try again.');
    });
}


    

    // Previous button handler
    prevButton.addEventListener('click', () => {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            updateContent();  // Change content
            updateProgress(-20); // Decrease progress
        }
    });

    // Update progress bar and button layout
    function updateProgress(increment) {
        // Update progress percentage
        progressPercentage += increment;
        if (progressPercentage < 0) progressPercentage = 0;
        if (progressPercentage > 100) progressPercentage = 100;

        // Update progress bar width and text
        progressBar.style.width = progressPercentage + '%';
        progressBar.textContent = progressPercentage + '%';

        // Show/Hide Previous Button
        if (progressPercentage > 20) {
            prevButton.style.display = 'inline-block';
        } else {
            prevButton.style.display = 'none';
        }
    }

    // Add event listener for the next button (initially)
    nextButton.addEventListener('click', nextButtonHandler);

    // Initialize with the first question
    updateContent();
});