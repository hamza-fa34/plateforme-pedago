document.addEventListener('DOMContentLoaded', function() {
    // Fonction utilitaire pour afficher une notification
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} notification`;
        notification.setAttribute('role', 'alert');
        notification.textContent = message;
        
        // Style de la notification
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.zIndex = '9999';
        notification.style.opacity = '0';
        notification.style.transition = 'opacity 0.3s ease-in-out';
        
        document.body.appendChild(notification);
        
        // Animation d'apparition
        setTimeout(() => {
            notification.style.opacity = '1';
        }, 100);
        
        // Disparaît après 3 secondes
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    // Récupération des éléments du DOM
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    const toggleFavoriteUrl = document.body.dataset.toggleFavoriteUrl;
    const csrfToken = document.body.dataset.csrfToken;

    // Vérification des éléments requis
    if (!toggleFavoriteUrl || !csrfToken) {
        console.error('CSRF token or toggle favorite URL is not defined in the body dataset.');
        return;
    }

    // Gestion des clics sur les boutons de favori
    favoriteButtons.forEach(btn => {
        btn.addEventListener('click', async function(e) {
            e.preventDefault();
            e.stopPropagation();

            const resourceId = this.dataset.resourceId;
            const icon = this.querySelector('i.fa-heart');
            const isCurrentlyFavorite = icon && icon.classList.contains('favorite');
            
            // Mise à jour visuelle immédiate pour un meilleur ressenti utilisateur
            if (icon) {
                icon.style.transition = 'all 0.3s ease';
                icon.style.transform = 'scale(1.2)';
                setTimeout(() => {
                    icon.style.transform = 'scale(1)';
                }, 300);
            }

            try {
                // Désactiver le bouton pendant la requête
                this.disabled = true;
                
                const formData = new URLSearchParams();
                formData.append('resource_id', resourceId);

                const response = await fetch(toggleFavoriteUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: formData,
                    credentials: 'same-origin'
                });

                if (!response.ok) {
                    throw new Error(`Erreur HTTP! Statut: ${response.status}`);
                }

                const data = await response.json();

                if (data.success) {
                    // Mise à jour de l'icône
                    if (icon) {
                        icon.classList.toggle('favorite', data.favorited);
                        
                        // Feedback visuel
                        if (data.favorited) {
                            showNotification('Ajouté aux favoris', 'success');
                        } else {
                            showNotification('Retiré des favoris', 'info');
                        }
                    }
                } else {
                    showNotification(data.error || 'Une erreur est survenue', 'danger');
                    console.error('Échec du changement de statut de favori:', data.error);
                }
            } catch (error) {
                console.error('Erreur lors de la modification du favori:', error);
                showNotification('Erreur de connexion au serveur', 'danger');
                
                // Annuler le changement visuel en cas d'erreur
                if (icon) {
                    icon.classList.toggle('favorite', isCurrentlyFavorite);
                }
            } finally {
                // Réactiver le bouton
                this.disabled = false;
            }
        });
    });

    // Style pour les notifications
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            padding: 15px 20px;
            border-radius: 4px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 300px;
        }
        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-info {
            background-color: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .favorite {
            color: #dc3545 !important;
        }
    `;
    document.head.appendChild(style);
});
