document.addEventListener("DOMContentLoaded", function () {
    // Pie chart showing travel preferences (based on survey answers)
    fetch("/api/survey-answers")
        .then(response => response.json())
        .then(data => {
            const ctx = document.createElement("canvas");
            ctx.id = "preferencesChart";
            const container = document.querySelector(".chart-container");
            container.innerHTML = "";
            container.appendChild(ctx);

            new Chart(ctx, {
                type: "pie",
                data: {
                    labels: Object.keys(data),
                    datasets: [{
                        label: "Preferences",
                        data: Object.values(data),
                        backgroundColor: [
                            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
                            "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
                        ]
                    }]
                },
                options: {
                    responsive: true
                }
            });
        })
        .catch(err => console.error("Failed to fetch survey answers:", err));
});
