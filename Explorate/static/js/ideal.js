document.addEventListener("DOMContentLoaded", () => {
    const resultsContainer = document.getElementById("results-container");

    // Retrieve the recommendation data from sessionStorage
    const resultData = JSON.parse(sessionStorage.getItem("recommendationResult"));

    console.log("Retrieved data from sessionStorage:", resultData); // Debugging sessionStorage data

    if (!resultData) {
        resultsContainer.innerHTML = "<p>No recommendations found. Please try again.</p>";
        return;
    }

    const { selected_state, recommendations } = resultData;

    if (!selected_state || !recommendations) {
        resultsContainer.innerHTML = "<p>Invalid data received. Please try again.</p>";
        return;
    }

    const recommendationsHtml = `
        <h2>Recommended State: ${selected_state}</h2>
        <ul>
            ${Object.entries(recommendations)
                .map(([category, suggestion]) => 
                    `<li><strong>${category}:</strong> ${suggestion || "No recommendation available"}</li>`)
                .join("")}
        </ul>
    `;

    resultsContainer.innerHTML = recommendationsHtml;
});



