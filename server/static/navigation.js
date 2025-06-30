// Navigation JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const header = document.querySelector('.main-header');
    const nav = document.querySelector('.nav');
    
    // Gestion du menu mobile
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            header.classList.toggle('mobile-menu-open');
            mobileMenuToggle.classList.toggle('active');
            
            // Animation de l'icône
            const icon = mobileMenuToggle.querySelector('i');
            if (header.classList.contains('mobile-menu-open')) {
                icon.style.transform = 'rotate(90deg)';
            } else {
                icon.style.transform = 'rotate(0deg)';
            }
        });
    }
    
    // Fermer le menu mobile en cliquant à l'extérieur
    document.addEventListener('click', function(event) {
        if (header.classList.contains('mobile-menu-open') && 
            !header.contains(event.target)) {
            header.classList.remove('mobile-menu-open');
            mobileMenuToggle.classList.remove('active');
            const icon = mobileMenuToggle.querySelector('i');
            icon.style.transform = 'rotate(0deg)';
        }
    });
    
    // Marquer la page active dans la navigation
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href.replace(/^\/+/, ''))) {
            link.classList.add('active');
        }
    });
    
    // Gestion des tooltips pour mobile
    if (window.innerWidth <= 768) {
        const navLinksWithIcons = document.querySelectorAll('.nav-link i');
        navLinksWithIcons.forEach(icon => {
            const link = icon.closest('.nav-link');
            const span = link.querySelector('span');
            if (span) {
                const text = span.textContent;
                link.setAttribute('title', text);
            }
        });
    }
    
    // Animation d'apparition des éléments de navigation
    const navElements = document.querySelectorAll('.nav-link, .user-info, .guest-menu a');
    navElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(10px)';
        
        setTimeout(() => {
            element.style.transition = 'all 0.3s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 50);
    });
    
    // Gestion du scroll pour l'effet sticky
    let lastScrollTop = 0;
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scroll vers le bas
            header.style.transform = 'translateY(-100%)';
        } else {
            // Scroll vers le haut
            header.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
    
    // Amélioration de l'accessibilité
    const focusableElements = header.querySelectorAll('a, button, [tabindex]:not([tabindex="-1"])');
    focusableElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.style.outline = '2px solid var(--color-accent)';
            this.style.outlineOffset = '2px';
        });
        
        element.addEventListener('blur', function() {
            this.style.outline = 'none';
        });
    });
    
    // Gestion des raccourcis clavier
    document.addEventListener('keydown', function(event) {
        // Échap pour fermer le menu mobile
        if (event.key === 'Escape' && header.classList.contains('mobile-menu-open')) {
            header.classList.remove('mobile-menu-open');
            mobileMenuToggle.classList.remove('active');
            const icon = mobileMenuToggle.querySelector('i');
            icon.style.transform = 'rotate(0deg)';
        }
        
        // Alt + M pour ouvrir/fermer le menu mobile
        if (event.altKey && event.key === 'm') {
            event.preventDefault();
            mobileMenuToggle.click();
        }
    });

    const burger = document.querySelector('.burger-menu');
    const mobileMenu = document.getElementById('mobileMenu');
    const closeBtn = document.querySelector('.close-menu');
    const overlay = document.querySelector('.mobile-menu-overlay');

    function openMenu() {
        mobileMenu.classList.add('open');
        overlay.classList.add('open');
        burger.setAttribute('aria-expanded', 'true');
        mobileMenu.focus();
    }
    function closeMenu() {
        mobileMenu.classList.remove('open');
        overlay.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
        burger.focus();
    }
    burger && burger.addEventListener('click', openMenu);
    closeBtn && closeBtn.addEventListener('click', closeMenu);
    overlay && overlay.addEventListener('click', closeMenu);
    // Accessibilité : fermer avec Echap
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileMenu.classList.contains('open')) {
            closeMenu();
        }
    });
}); 