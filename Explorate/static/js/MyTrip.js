$(document).ready(function () {
    $.ajax({
        url: '/api/adventures',  // relative URL is better
        type: 'POST',
        contentType: 'application/json',
        data: '{}',  // send empty JSON, or you can omit this line if your Flask can handle no data
        beforeSend: function (xhr) {
                const csrfToken = $('meta[name="csrf-token"]').attr('content');
                xhr.setRequestHeader('X-CSRF-Token', csrfToken); // Include CSRF token in the request header
            },
        success: function (data) {
            if (data.length > 0) {
                const table = $('#adventure-table');
                const tbody = table.find('tbody');
                tbody.empty();

                data.forEach(row => {
                    const tr = `<tr>
                        <td>${row.adventure_name}</td>
                        <td>${row.recommendation_1}</td>
                        <td>${row.recommendation_2}</td>
                        <td>${row.recommendation_3}</td>
                        <td>${row.recommendation_4}</td>
                    </tr>`;
                    tbody.append(tr);
                });

                table.show();
                $('#no-data-message').hide();
            } else {
                $('#adventure-table').hide();
                $('#no-data-message').show();
            }
        },
        error: function () {
            alert('You do not have any data. Please create a trip first.');
        }
    });
});

