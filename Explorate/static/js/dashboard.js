
document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/age-distribution")
        .then(res => res.json())
        .then(data => {
            const ctx = document.createElement("canvas");
            ctx.id = "ageChart";
            const container = document.querySelector(".charts-grid .chart-card:first-child .chart-container");
            if (container) {
                container.innerHTML = "";
                container.appendChild(ctx);

                new Chart(ctx, {
                    type: "bar",
                    data: {
                        labels: Object.keys(data),
                        datasets: [{
                            label: "Your Age Group",
                            data: Object.values(data),
                            backgroundColor: "#3b82f6"
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
            }
        });
});
