async function fetchData() {
    try {
        const response = await fetch('/fetch-adventure-data', {
            method: 'GET', // Or 'POST' if required
            headers: {
                "Content-Type": "application/json",
                "X-CSRF-Token": document.querySelector('meta[name="csrf-token"]').content, // Include CSRF token
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        const tableBody = document.getElementById('data-table');

        data.forEach(row => {
            const tr = document.createElement('tr');

            tr.innerHTML = `
                <td class="py-2 px-4 border-b">${row.username}</td>
                <td class="py-2 px-4 border-b">${row.adventure_name}</td>
                <td class="py-2 px-4 border-b">${row.recommendation_1 || 'N/A'}</td>
                <td class="py-2 px-4 border-b">${row.recommendation_2 || 'N/A'}</td>
                <td class="py-2 px-4 border-b">${row.recommendation_3 || 'N/A'}</td>
                <td class="py-2 px-4 border-b">${row.recommendation_4 || 'N/A'}</td>
            `;

            tableBody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

fetchData();