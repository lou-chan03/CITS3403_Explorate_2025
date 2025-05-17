const ratings = {};

document.addEventListener('DOMContentLoaded', () => {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const ratingBlocks = document.querySelectorAll('.rate');

    // Validate recommendation ID
    const recommendationInput = document.getElementById('recommendation-id');
    if (!recommendationInput) {
        console.error('Error: Recommendation ID input not found in the DOM.');
        alert('Recommendation ID is missing. Please check your setup.');
        return; // Exit early if the ID is not found
    }
    const recommendationId = recommendationInput.value;

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

    // Submit ratings when user clicks submit button
    document.querySelector('#submit-rating-btn').addEventListener('click', function () {
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
        ratings['overall'] = avg; // Store overall rating
    }
}

// Function to submit ratings to the server
function submitRatings() {
    const recommendationInput = document.getElementById('recommendation-id');
    const useridinput = document.getElementById('user-id');
    const submitButton = document.querySelector('#submit-rating-btn');
    const redirectUrl = submitButton.getAttribute('data-share-url');
    console.log("useridinput", useridinput);
    if (!recommendationInput) {
        console.error('Error: Recommendation ID input not found in the DOM.');
        alert('Recommendation ID is missing. Please check your setup.');
        return; // Exit early if the ID is not found
    }

    const recommendationId = recommendationInput.value;

    // Prepare the rating data to send to the server
    const ratingData = {
        recommendation_id: recommendationId,
        location_rating: ratings['1'] || 0,
        food_rating: ratings['2'] || 0,
        attractions_rating: ratings['3'] || 0,
        accommodation_rating: ratings['4'] || 0,
        overall_rating: ratings['overall'] || 0,
    };
    console.log("hellooooo", recommendationInput, "1", recommendationInput.value);

    console.log('Submitting data:', ratingData); // For debugging
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch('/submit_rating', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': csrfToken, // Include CSRF token for security
        },
        body: JSON.stringify(ratingData),
    })
        .then((response) => {
            if (response.ok) {
                alert('Ratings submitted successfully!');
                
                window.location.href =  redirectUrl;
            } else {
                alert('Failed to submit ratings.');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Error submitting ratings.');
        });
}

// Utility function to highlight stars up to selected rating
function highlightStars(rating, stars) {
    stars.forEach((star, index) => {
        star.style.color = index < rating ? 'orange' : 'black';
    });
}

// Optional: expose ratings globally for access in forms or AJAX
window.getRatings = function () {
    return ratings;
};
