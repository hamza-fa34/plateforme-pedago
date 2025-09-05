document.addEventListener('DOMContentLoaded', function() {
    const userTypeRadios = document.querySelectorAll('input[name="user_type"]');
    const rollNumberSection = document.getElementById('rollNumberSection');
    const niveauSection = document.getElementById('niveauSection');
    const filiereSection = document.getElementById('filiereSection');

    function toggleStudentFields() {
        const selectedUserType = document.querySelector('input[name="user_type"]:checked');
        if (selectedUserType && selectedUserType.value === 'student') {
            rollNumberSection.classList.remove('hidden');
            niveauSection.classList.remove('hidden');
            filiereSection.classList.remove('hidden');
        } else {
            rollNumberSection.classList.add('hidden');
            niveauSection.classList.add('hidden');
            filiereSection.classList.add('hidden');
        }
    }

    userTypeRadios.forEach(radio => {
        radio.addEventListener('change', toggleStudentFields);
    });

    // Initial check
    toggleStudentFields();
});
