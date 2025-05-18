document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const email = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            const errorMessage = document.getElementById('error-message');
            errorMessage.textContent = '';
            
            try {
                const response = await fetch('/users/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                });
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Error en inicio de sesión');
                }
                  const data = await response.json();
                localStorage.setItem('token', data.access_token);
                
                // Actualizar la UI con el nuevo usuario
                if (typeof AuthService !== 'undefined') {
                    await AuthService.getCurrentUser();
                    AuthService.updateUI();
                }
                
                // Redirigir a la página principal
                window.location.href = '/';
                
            } catch (error) {
                errorMessage.textContent = error.message || 'Error al intentar iniciar sesión';
                errorMessage.style.color = 'red';
            }
        });
    }
      if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('reg-username').value;
            const fullName = document.getElementById('reg-full-name').value;
            const email = document.getElementById('reg-email').value;
            const password = document.getElementById('reg-password').value;
            
            const errorMessage = document.getElementById('reg-error-message');
            errorMessage.textContent = '';
            
            try {
                const response = await fetch('/users/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: username,
                        full_name: fullName,
                        email: email,
                        password: password
                    })
                });
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Error en registro');
                }
                
                // Mostrar mensaje de éxito
                const registerBox = document.querySelector('.register-box');
                const loginBox = document.querySelector('.login-box');
                
                if (registerBox && loginBox) {
                    registerBox.style.display = 'none';
                    loginBox.style.display = 'block';
                    
                    const loginErrorMessage = document.getElementById('error-message');
                    loginErrorMessage.textContent = 'Registro exitoso. Por favor inicia sesión.';
                    loginErrorMessage.style.color = 'green';
                }
                
            } catch (error) {
                errorMessage.textContent = error.message || 'Error al intentar registrarse';
                errorMessage.style.color = 'red';
            }
        });
    }
    
    // Mostrar/ocultar formularios de login y registro
    const showRegisterBtn = document.getElementById('show-register');
    const showLoginBtn = document.getElementById('show-login');
    
    if (showRegisterBtn) {
        showRegisterBtn.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector('.login-box').style.display = 'none';
            document.querySelector('.register-box').style.display = 'block';
        });
    }
    
    if (showLoginBtn) {
        showLoginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector('.register-box').style.display = 'none';
            document.querySelector('.login-box').style.display = 'block';
        });
    }
});