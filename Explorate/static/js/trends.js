document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/trends")
        .then(response => response.json())
        .then(data => {
            document.getElementById("total-trips").textContent = data.total_trips;
            document.getElementById("trip-duration").textContent = data.trip_duration + " days";
            document.getElementById("top-state").textContent = data.top_state;
            document.getElementById("top-category").textContent = data.top_category;

            // ✅ Chart.js Logic goes here
            const ctx = document.getElementById('trips-over-time-chart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                    datasets: [{
                        label: 'Trips Taken',
                        data: [2, 4, 3, 5, 6], // ← replace with real data later
                        backgroundColor: 'rgba(22, 165, 69, 0.2)',
                        borderColor: '#16a34a',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.3,
                        pointBackgroundColor: '#16a34a'
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error("Error loading trend data:", error));
});

