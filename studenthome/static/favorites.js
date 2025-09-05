document.addEventListener('DOMContentLoaded', function() {
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    const toggleFavoriteUrl = document.body.dataset.toggleFavoriteUrl;
    const csrfToken = document.body.dataset.csrfToken;

    if (!toggleFavoriteUrl || !csrfToken) {
        console.error('CSRF token or toggle favorite URL is not defined in the body dataset.');
        return;
    }

    favoriteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            const resourceId = this.dataset.resourceId;
            const formData = new URLSearchParams();
            formData.append('resource_id', resourceId);

            fetch(toggleFavoriteUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData
            })
            .then(res => {
                if (!res.ok) {
                    throw new Error(`HTTP error! status: ${res.status}`);
                }
                return res.json();
            })
            .then(data => {
                if (data.success) {
                    const icon = this.querySelector('i.fa-heart');
                    if (icon) {
                        icon.classList.toggle('favorite', data.favorited);
                    }
                } else {
                    console.error('Failed to toggle favorite status:', data.error);
                }
            })
            .catch(error => {
                console.error('AJAX error when toggling favorite:', error);
            });
        });
    });
});
