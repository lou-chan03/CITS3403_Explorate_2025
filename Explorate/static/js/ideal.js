document.addEventListener("DOMContentLoaded", () => {
    const resultsContainer = document.getElementById("results-container");

    const resultData = JSON.parse(sessionStorage.getItem("recommendationResult"));

    if (!resultData) {
        resultsContainer.innerHTML = "<p>No recommendations found. Please try again.</p>";
        return;
    }

    const { selected_state, recommendations } = resultData;

    if (!selected_state || !recommendations) {
        resultsContainer.innerHTML = "<p>Invalid data received. Please try again.</p>";
        return;
    }

    // Create the heading
    const heading = document.createElement("h2");
    heading.classList.add("text-center", "mb-4");
    heading.textContent = `Recommended State: ${selected_state}`;
    resultsContainer.appendChild(heading);

    // Create a container for cards or rows
    const recGrid = document.createElement("div");
    recGrid.classList.add("row", "g-3");

    // Loop through recommendations and create styled cards
    Object.entries(recommendations).forEach(([category, suggestion]) => {
        const col = document.createElement("div");
        col.classList.add("col-md-6");

        const card = document.createElement("div");
        card.classList.add("p-3", "rounded", "shadow-sm", "adventure-card");

        const catElem = document.createElement("h5");
        catElem.textContent = category;
        catElem.classList.add("fw-bold", "custom-category");

        const suggestionElem = document.createElement("p");
        suggestionElem.textContent = suggestion || "No recommendation available";
        suggestionElem.classList.add("mb-0");

        card.appendChild(catElem);
        card.appendChild(suggestionElem);
        col.appendChild(card);
        recGrid.appendChild(col);
    });

    resultsContainer.appendChild(recGrid);
});
