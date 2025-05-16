$(document).ready(function() {
    // Fetch existing friends + adventures on page load
    fetchFriendsAdventures();

    $('#friend-adventure-form').on('submit', function(e) {
        e.preventDefault();

        const frd_username = $('#frd_username').val();
        const adv_name = $('#adv_name').val();

        $.ajax({
            url: '/add_friend_adventure',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ frd_username, adv_name }),
            success: function(response) {
                alert(response.message);
                fetchFriendsAdventures();
                $('#friend-adventure-form')[0].reset();
            },
            error: function(xhr) {
                alert(xhr.responseJSON?.message || 'An error occurred');
            }
        });
    });

    function fetchFriendsAdventures() {
        $.ajax({
            url: '/get_friends_adventures',
            method: 'GET',
            success: function(response) {
                const list = $('#friends-adventures-list');
                list.empty();
                response.friends_adventures.forEach(item => {
                    list.append(`<li>${item.friend_username} — ${item.adventure_name}</li>`);
                });
            },
            error: function() {
                alert('Failed to load friends and adventures.');
            }
        });
    }
});

