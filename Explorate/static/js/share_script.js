// Object to store all user-selected ratings by block ID
const ratings = {};

document.addEventListener('DOMContentLoaded', () => {
    const ratingBlocks = document.querySelectorAll('.rate');

    ratingBlocks.forEach(block => {
        const ratingId = block.getAttribute('data-rating-id');
        const stars = block.querySelectorAll('.star');
        const output = block.querySelector('.output');
        let selectedRating = 0;

        stars.forEach((star, index) => {
            // Highlight stars on hover
            star.addEventListener('mouseover', () => {
                highlightStars(index + 1, stars);
            });

            // Restore stars on mouseout
            star.addEventListener('mouseout', () => {
                highlightStars(selectedRating, stars);
            });

            // Set rating on click
            star.addEventListener('click', () => {
                selectedRating = index + 1;
                ratings[ratingId] = selectedRating; // Store rating
                highlightStars(selectedRating, stars);
                if (output) {
                    output.innerText = `Rating is: ${selectedRating}/5`;
                }
            });
        });
    });
    // submit ratings when user clicks submit button
    document.querySelector('#submit-rating-btn').addEventListener('click', function(){
        submitRatings();
        updateOverallRating();
    });
});

// Function to update the overall rating based on selected ratings
function updateOverallRating() {
    const requiredIds = ['1', '2', '3', '4']; // Correspond to Location, Food, Attractions, Accommodation
    let sum = 0;
    let count = 0;

    requiredIds.forEach(id => {
        if (ratings[id]) {
            sum += ratings[id];
            count++;
        }
    });

    const avg = count > 0 ? (sum / count).toFixed(1) : 0;
    const overallOutput = document.getElementById('overall-rating');
    if (overallOutput) {
        overallOutput.innerText = `Overall Rating: ${avg}/5`;
    }
}

// Function to submit ratings to server
function submitRatings(){
    //const adventureId = document.getElementById('adventure-id').value;
    //const userID = document.getElementById('user-id').value;

    // Prepare the rating data to send to the server
    const ratingData = {
        //user_id: userID,
        //adventure_id: adventureId,
        location_rating: ratings['1'] || 0,
        food_rating: ratings['2'] || 0,
        attractions_rating: ratings['3'] || 0,
        accommodation_rating: ratings['4'] || 0
    };

    fetch('/submit_rating', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(ratingData)
    })
    .then(response => {
        if (response.ok) {
            alert("Ratings submitted!");
        } else {
            alert("Failed to submit ratings.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Error submitting ratings.");
    });
}

// Utility function to highlight stars up to selected rating
function highlightStars(rating, stars) {
    stars.forEach((star, index) => {
        star.style.color = index < rating ? 'orange' : 'black';
    });
}

// Optional: expose ratings globally for access in forms or AJAX
window.getRatings = function() {
    return ratings;
}

