// Verificar si el token JWT existe en el almacenamiento local
document.addEventListener('DOMContentLoaded', function() {
    // Elementos comunes
    const loginBtn = document.getElementById('login-btn');
    const logoutBtn = document.getElementById('logout-btn');
    
    if (loginBtn && logoutBtn) {
        const token = localStorage.getItem('access_token');
        
        if (token) {
            // Usuario autenticado
            document.querySelectorAll('.auth-link')[0].style.display = 'none';
            document.querySelectorAll('.auth-link')[1].style.display = 'block';
            
            // Cargar libros
            loadBooks();
        } else {
            // Usuario no autenticado
            document.querySelectorAll('.auth-link')[0].style.display = 'block';
            document.querySelectorAll('.auth-link')[1].style.display = 'none';
        }
        
        // Manejar el cierre de sesión
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            localStorage.removeItem('access_token');
            window.location.href = '/login';
        });
    }
    
    // Formulario de inicio de sesión
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            login(username, password);
        });
    }
    
    // Formulario de registro
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const username = document.getElementById('reg-username').value;
            const email = document.getElementById('reg-email').value;
            const fullName = document.getElementById('reg-full-name').value;
            const password = document.getElementById('reg-password').value;
            
            register(username, email, fullName, password);
        });
    }
    
    // Alternar entre los formularios de inicio de sesión y registro
    const showRegister = document.getElementById('show-register');
    const showLogin = document.getElementById('show-login');
    
    if (showRegister && showLogin) {
        showRegister.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector('.login-box').style.display = 'none';
            document.querySelector('.register-box').style.display = 'block';
        });
        
        showLogin.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector('.register-box').style.display = 'none';
            document.querySelector('.login-box').style.display = 'block';
        });
    }
    
    // Inicializar el servicio de autenticación si existe
    if (typeof AuthService !== 'undefined') {
        AuthService.init();
    }
    
    // Mostrar mensajes de alerta temporales
    const showAlert = (message, type = 'info') => {
        const alertContainer = document.createElement('div');
        alertContainer.className = `alert alert-${type}`;
        alertContainer.textContent = message;
        
        document.body.appendChild(alertContainer);
        
        // Mostrar la alerta con animación
        setTimeout(() => {
            alertContainer.classList.add('show');
        }, 10);
        
        // Eliminar la alerta después de 3 segundos
        setTimeout(() => {
            alertContainer.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(alertContainer);
            }, 300);
        }, 3000);
    };
    
    // Exponer la función de alerta globalmente
    window.showAlert = showAlert;
    
    // Manejar búsqueda de libros (si existe el formulario)
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const query = document.getElementById('search-input').value.trim();
            
            if (query.length < 2) {
                showAlert('Por favor, ingresa al menos 2 caracteres para buscar', 'warning');
                return;
            }
            
            // Redirigir a la página de resultados de búsqueda
            window.location.href = `/books/search?q=${encodeURIComponent(query)}`;
        });
    }
    
    // Configurar tooltips (si existen)
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function() {
            const message = this.getAttribute('data-tooltip');
            
            const tooltipElement = document.createElement('div');
            tooltipElement.className = 'tooltip';
            tooltipElement.textContent = message;
            
            const rect = this.getBoundingClientRect();
            tooltipElement.style.top = `${rect.top - 35}px`;
            tooltipElement.style.left = `${rect.left + (rect.width / 2) - 100}px`;
            
            document.body.appendChild(tooltipElement);
            
            setTimeout(() => {
                tooltipElement.classList.add('show');
            }, 10);
            
            this.addEventListener('mouseleave', function onMouseLeave() {
                tooltipElement.classList.remove('show');
                setTimeout(() => {
                    document.body.removeChild(tooltipElement);
                }, 300);
                this.removeEventListener('mouseleave', onMouseLeave);
            });
        });
    });
    
    // Detectar si es la primera visita para mostrar un tutorial (usando localStorage)
    const hasVisitedBefore = localStorage.getItem('hasVisitedBookMatch');
    if (!hasVisitedBefore && window.location.pathname === '/') {
        // Mostrar tutorial o mensaje de bienvenida
        showAlert('¡Bienvenido a BookMatch! Descubre tu próxima lectura favorita.', 'success');
        localStorage.setItem('hasVisitedBookMatch', 'true');
    }
});

// Función para iniciar sesión
async function login(username, password) {
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = '';
    
    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch('/users/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Guardar el token en el almacenamiento local
            localStorage.setItem('access_token', data.access_token);
            
            // Redirigir a la página principal
            window.location.href = '/';
        } else {
            // Mostrar mensaje de error
            errorMessage.textContent = data.detail || 'Error de autenticación. Verifica tus credenciales.';
        }
    } catch (error) {
        errorMessage.textContent = 'Error al conectar con el servidor. Inténtalo de nuevo.';
        console.error('Error:', error);
    }
}

// Función para registrar un usuario
async function register(username, email, fullName, password) {
    const errorMessage = document.getElementById('reg-error-message');
    errorMessage.textContent = '';
    
    try {
        const response = await fetch('/users/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                email,
                full_name: fullName,
                password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Mostrar formulario de inicio de sesión
            document.querySelector('.register-box').style.display = 'none';
            document.querySelector('.login-box').style.display = 'block';
            
            // Mostrar mensaje de éxito
            document.getElementById('error-message').textContent = '¡Registro exitoso! Ahora puedes iniciar sesión.';
        } else {
            // Mostrar mensaje de error
            errorMessage.textContent = data.detail || 'Error al registrar. Inténtalo de nuevo.';
        }
    } catch (error) {
        errorMessage.textContent = 'Error al conectar con el servidor. Inténtalo de nuevo.';
        console.error('Error:', error);
    }
}

// Función para cargar libros
async function loadBooks() {
    const booksContainer = document.getElementById('books-container');
    if (!booksContainer) return;
    
    try {
        const token = localStorage.getItem('access_token');
        
        if (!token) {
            booksContainer.innerHTML = '<p>Inicia sesión para ver los libros disponibles.</p>';
            return;
        }
        
        const response = await fetch('/users/books/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const books = await response.json();
            
            if (books.length === 0) {
                booksContainer.innerHTML = '<p>No hay libros disponibles en este momento.</p>';
                return;
            }
            
            let booksHTML = '';
            books.forEach(book => {
                booksHTML += `
                <div class="book-card">
                    <div class="book-image">
                        <img src="/static/placeholder-book.jpg" alt="${book.title}">
                    </div>
                    <div class="book-info">
                        <h3>${book.title}</h3>
                        <p>Por: ${book.author}</p>
                        <p>${book.genre ? book.genre.join(', ') : 'Sin género'}</p>
                    </div>
                </div>
                `;
            });
            
            booksContainer.innerHTML = booksHTML;
        } else {
            // Manejar error de autenticación
            if (response.status === 401) {
                localStorage.removeItem('access_token');
                booksContainer.innerHTML = '<p>Tu sesión ha expirado. Por favor, <a href="/login">inicia sesión</a> de nuevo.</p>';
            } else {
                booksContainer.innerHTML = '<p>Error al cargar los libros. Por favor, intenta de nuevo más tarde.</p>';
            }
        }
    } catch (error) {
        console.error('Error:', error);
        booksContainer.innerHTML = '<p>Error al conectar con el servidor. Por favor, intenta de nuevo más tarde.</p>';
    }
}