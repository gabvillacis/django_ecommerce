// static/js/auth.js

// Función para manejar el envío del formulario de registro vía AJAX
function submitSignupForm() {
    const form = document.getElementById('signup-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        // Limpiar errores anteriores
        document.querySelectorAll('.error').forEach(el => el.innerText = '');
        const formData = new FormData(form);

        axios.post(ajaxSignupUrl, formData, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => {
            if(response.data.success) {
                alert(response.data.message);
                window.location.href = signinUrl;
            } else {
                // Mostrar errores en cada campo
                const errors = response.data.errors;
                for(let field in errors) {
                    const errorElem = document.getElementById('error-' + field);
                    if (errorElem) {
                        errorElem.innerText = errors[field];
                    }
                }
            }
        })
        .catch(error => console.error('Error:', error));
    });
}

// Función para manejar el envío del formulario de inicio de sesión vía AJAX
function submitSigninForm() {
    const form = document.getElementById('signin-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        document.querySelectorAll('.error').forEach(el => el.innerText = '');
        const formData = new FormData(form);

        axios.post(ajaxSigninUrl, formData, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => {
            if(response.data.success) {
                window.location.href = homeUrl;
            } else {
                if(response.data.errors.__all__){
                    alert(response.data.errors.__all__);
                } else {
                    const errors = response.data.errors;
                    for(let field in errors) {
                        const errorElem = document.getElementById('error-' + field);
                        if (errorElem) {
                            errorElem.innerText = errors[field];
                        }
                    }
                }
            }
        })
        .catch(error => console.error('Error:', error));
    });
}

// Función para cerrar sesión vía AJAX
function logoutUser() {
    axios.get(ajaxLogoutUrl, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => {
        if(response.data.success){
            window.location.href = homeUrl;
        }
    })
    .catch(error => console.error('Error:', error));
}


// Inicialización: se ejecuta cuando la página carga
document.addEventListener('DOMContentLoaded', function() {
    if(document.getElementById('signup-form')) {
        submitSignupForm();
    }
    if(document.getElementById('signin-form')) {
        submitSigninForm();
    }
});