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
});

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
