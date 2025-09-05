document.addEventListener('DOMContentLoaded', function() {
    const deleteForms = document.querySelectorAll('.delete-form');

    deleteForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const confirmation = confirm('Êtes-vous sûr de vouloir supprimer cette ressource ?');
            if (!confirmation) {
                event.preventDefault();
            }
        });
    });
});
