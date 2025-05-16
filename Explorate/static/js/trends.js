document.addEventListener("DOMContentLoaded", function () {
    // Example: Bar chart for age group distribution
    fetch("/api/age-distribution")
        .then(response => response.json())
        .then(data => {
            const ctx = document.createElement("canvas");
            ctx.id = "ageChart";
            document.getElementById("trips-over-time-chart").innerHTML = "";
            document.getElementById("trips-over-time-chart").appendChild(ctx);

            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: Object.keys(data),
                    datasets: [{
                        label: "Users",
                        data: Object.values(data),
                        backgroundColor: "#16a34a"
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(err => console.error("Failed to fetch age data:", err));
});
