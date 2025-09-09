document.addEventListener('DOMContentLoaded', function() {
    // Éléments du DOM
    const userTypeRadios = document.querySelectorAll('input[name="user_type"]');
    const studentFields = document.getElementById('studentFields');
    const teacherFields = document.getElementById('teacherFields');
    const form = document.querySelector('form');
    
    // Fonction pour basculer entre les champs étudiants et enseignants
    function toggleUserSpecificFields() {
        const selectedUserType = document.querySelector('input[name="user_type"]:checked');
        
        // Masquer tous les champs spécifiques d'abord
        if (studentFields) studentFields.classList.add('hidden');
        if (teacherFields) teacherFields.classList.add('hidden');
        
        // Afficher les champs appropriés selon le type d'utilisateur
        if (selectedUserType) {
            if (selectedUserType.value === 'student' && studentFields) {
                studentFields.classList.remove('hidden');
            } else if (selectedUserType.value === 'teacher' && teacherFields) {
                teacherFields.classList.remove('hidden');
            }
        }
        
        // Mettre à jour les champs requis
        updateFieldRequirements(selectedUserType ? selectedUserType.value : '');
    }
    
    // Fonction pour mettre à jour les attributs required des champs
    function updateFieldRequirements(userType) {
        // Réinitialiser tous les champs requis
        const allRequiredFields = form.querySelectorAll('[required]');
        allRequiredFields.forEach(field => {
            field.removeAttribute('required');
            field.removeAttribute('aria-required');
        });
        
        // Marquer les champs de base comme requis
        const baseRequiredFields = [
            'username', 'email', 'first_name', 'last_name', 
            'password1', 'password2', 'user_type'
        ];
        
        baseRequiredFields.forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                field.required = true;
                field.setAttribute('aria-required', 'true');
            }
        });
        
        // Marquer les champs spécifiques comme requis en fonction du type d'utilisateur
        if (userType === 'student') {
            const studentRequiredFields = ['roll_number', 'niveau', 'filiere'];
            studentRequiredFields.forEach(fieldName => {
                const field = form.querySelector(`[name="${fieldName}"]`);
                if (field) {
                    field.required = true;
                    field.setAttribute('aria-required', 'true');
                }
            });
        } else if (userType === 'teacher') {
            const teacherRequiredFields = ['matricule', 'matieres'];
            teacherRequiredFields.forEach(fieldName => {
                const field = form.querySelector(`[name="${fieldName}"]`);
                if (field) {
                    field.required = true;
                    field.setAttribute('aria-required', 'true');
                }
            });
        }
    }
    
    // Validation personnalisée pour le formulaire
    function validateForm(event) {
        const selectedUserType = document.querySelector('input[name="user_type"]:checked');
        let isValid = true;
        
        // Réinitialiser les messages d'erreur
        const errorMessages = form.querySelectorAll('.field-error');
        errorMessages.forEach(el => el.remove());
        
        // Valider le type d'utilisateur
        if (!selectedUserType) {
            const userTypeContainer = document.querySelector('.radio-group').parentNode;
            const errorElement = document.createElement('div');
            errorElement.className = 'alert alert-error field-error';
            errorElement.textContent = 'Veuillez sélectionner un type de compte';
            userTypeContainer.appendChild(errorElement);
            isValid = false;
        }
        
        // Validation spécifique pour les enseignants
        if (selectedUserType && selectedUserType.value === 'teacher') {
            const matieresCheckboxes = form.querySelectorAll('input[name="matieres"]:checked');
            if (matieresCheckboxes.length === 0) {
                const matieresContainer = form.querySelector('.checkbox-group').parentNode;
                const errorElement = document.createElement('div');
                errorElement.className = 'alert alert-error field-error';
                errorElement.textContent = 'Veuillez sélectionner au moins une matière';
                matieresContainer.appendChild(errorElement);
                isValid = false;
            }
        }
        
        // Validation des champs requis
        const requiredFields = form.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            if (!field.value && field.type !== 'radio' && field.type !== 'checkbox') {
                const fieldContainer = field.closest('.form-group');
                if (fieldContainer) {
                    const errorElement = document.createElement('div');
                    errorElement.className = 'alert alert-error field-error';
                    errorElement.textContent = 'Ce champ est obligatoire';
                    fieldContainer.appendChild(errorElement);
                    isValid = false;
                }
            }
        });
        
        // Empêcher la soumission si le formulaire n'est pas valide
        if (!isValid) {
            event.preventDefault();
            
            // Faire défiler jusqu'au premier champ avec erreur
            const firstError = form.querySelector('.field-error');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            
            return false;
        }
        
        return true;
    }
    
    // Ajouter des écouteurs d'événements
    if (userTypeRadios.length > 0) {
        userTypeRadios.forEach(radio => {
            radio.addEventListener('change', toggleUserSpecificFields);
        });
    }
    
    if (form) {
        form.addEventListener('submit', validateForm);
    }
    
    // Vérification initiale au chargement de la page
    toggleUserSpecificFields();
    
    // Ajouter des classes pour le style des champs
    const style = document.createElement('style');
    style.textContent = `
        .hidden { display: none !important; }
        .form-group { margin-bottom: 1rem; }
        .form-row { display: flex; gap: 1rem; margin: 0 -0.5rem; }
        .half-width { flex: 1; min-width: 0; }
        .radio-group, .checkbox-group { display: flex; flex-direction: column; gap: 0.5rem; }
        .radio-option, .checkbox-option { 
            display: flex; 
            align-items: center; 
            gap: 0.5rem; 
            cursor: pointer;
            padding: 0.5rem 0;
        }
        .radio-custom, .checkbox-custom {
            display: inline-block;
            width: 1.25rem;
            height: 1.25rem;
            border: 2px solid #ccc;
            border-radius: 50%;
            position: relative;
            margin-right: 0.5rem;
        }
        .checkbox-custom { border-radius: 4px; }
        input[type="radio"]:checked + .radio-custom::after,
        input[type="checkbox"]:checked + .checkbox-custom::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #007bff;
            border-radius: 50%;
            width: 0.75rem;
            height: 0.75rem;
        }
        input[type="checkbox"]:checked + .checkbox-custom::after {
            border-radius: 2px;
            width: 0.75rem;
            height: 0.75rem;
        }
        input[type="radio"], 
        input[type="checkbox"] { 
            position: absolute; 
            opacity: 0; 
            width: 0; 
            height: 0; 
        }
        .alert { 
            padding: 0.5rem; 
            margin: 0.5rem 0; 
            border-radius: 4px; 
            font-size: 0.875rem; 
        }
        .alert-error { 
            background-color: #fee2e2; 
            color: #b91c1c; 
            border: 1px solid #fca5a5;
        }
        .alert-success { 
            background-color: #dcfce7; 
            color: #166534; 
            border: 1px solid #86efac;
        }
        .required { color: #dc2626; }
    `;
    document.head.appendChild(style);
});
