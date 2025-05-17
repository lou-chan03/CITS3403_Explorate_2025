
document.addEventListener("DOMContentLoaded", function () {
    // Example: Color states based on popular destinations data
    fetch("/api/popular-destinations")
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                const state = document.querySelector(`[data-state="${item.state}"]`);
                if (state) {
                    state.classList.add("visited");
                    state.setAttribute("data-visited", "true");
                }
            });
        })
        .catch(err => console.error("Failed to fetch popular destinations:", err));
});



