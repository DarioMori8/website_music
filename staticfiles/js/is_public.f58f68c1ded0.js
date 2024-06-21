
document.addEventListener('DOMContentLoaded', function() {
    const toggles = document.querySelectorAll('.toggle-public');
    toggles.forEach(function(toggle) {
        toggle.addEventListener('change', function() {
            const playlistId = this.getAttribute('data-id');
            const form = this.closest('form');
            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ is_public: this.checked })
            });
        });
    });
});
