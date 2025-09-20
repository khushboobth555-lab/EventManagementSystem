// Automatically update age field when birth date changes

document.addEventListener('DOMContentLoaded', function() {
    var birthDateInput = document.getElementById('id_profile-birth_date');
    var ageInput = document.getElementById('id_profile-age');

    if (birthDateInput && ageInput) {
        birthDateInput.addEventListener('change', function() {
            var birthDate = new Date(this.value);
            var today = new Date();
            if (!isNaN(birthDate.getTime())) {
                var age = today.getFullYear() - birthDate.getFullYear();
                var m = today.getMonth() - birthDate.getMonth();
                if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
                    age--;
                }
                ageInput.value = age;
                // Age check for 18+
                var errorMsgId = 'dob-age-error';
                var existingError = document.getElementById(errorMsgId);
                if (age < 18) {
                    if (!existingError) {
                        var error = document.createElement('div');
                        error.id = errorMsgId;
                        error.className = 'text-danger';
                        error.style.marginTop = '5px';
                        error.textContent = 'You must be at least 18 years old to register.';
                        birthDateInput.parentNode.appendChild(error);
                    }
                } else {
                    if (existingError) {
                        existingError.remove();
                    }
                }
            } else {
                ageInput.value = '';
                var errorMsgId = 'dob-age-error';
                var existingError = document.getElementById(errorMsgId);
                if (existingError) {
                    existingError.remove();
                }
            }
        });
    }
});
