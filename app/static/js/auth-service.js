// Servicio de autenticación para BookMatch
const AuthService = {
    // Almacenamiento de información del usuario actual
    currentUser: null,
    
    // Inicializar el servicio de autenticación
    init: async function() {
        const token = localStorage.getItem('token');
        if (token) {
            try {
                // Verificar si el token es válido obteniendo la información del usuario
                await this.getCurrentUser();
                this.updateUI();
            } catch (error) {
                console.error('Error al verificar la sesión:', error);
                this.logout(); // Token inválido, cerrar sesión
            }
        } else {
            this.updateUI();
        }
    },
    
    // Obtener información del usuario actual
    getCurrentUser: async function() {
        const token = localStorage.getItem('token');
        if (!token) {
            this.currentUser = null;
            return null;
        }
        
        try {
            const response = await fetch('/users/me', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (!response.ok) {
                throw new Error('Error al obtener información del usuario');
            }
            
            const userData = await response.json();
            this.currentUser = userData;
            return userData;
        } catch (error) {
            console.error('Error al obtener información del usuario:', error);
            this.currentUser = null;
            return null;
        }
    },
    
    // Cerrar sesión
    logout: function() {
        localStorage.removeItem('token');
        this.currentUser = null;
        this.updateUI();
        // Si estamos en la página principal, recargar
        if (window.location.pathname === '/') {
            window.location.reload();
        } else {
            // Si no, redirigir a la página principal
            window.location.href = '/';
        }
    },
      // Actualizar la interfaz de usuario basado en el estado de autenticación
    updateUI: function() {
        const authSection = document.getElementById('auth-section');
        if (!authSection) return;
        
        if (this.currentUser) {
            // Usuario autenticado
            authSection.innerHTML = `
                <div class="user-menu">
                    <span class="username">${this.currentUser.username || this.currentUser.email}</span>
                    <div class="dropdown-content">
                        <a href="/profile">Mi perfil</a>
                        <a href="/my-books">Mis libros</a>
                        <a href="#" id="logout-btn">Cerrar sesión</a>
                    </div>
                </div>
            `;
            
            // Agregar evento para cerrar sesión
            const logoutBtn = document.getElementById('logout-btn');
            if (logoutBtn) {
                logoutBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this.logout();
                });
            }
            
            // Inicializar el comportamiento del menú de usuario después de crearlo
            if (typeof setupUserMenu === 'function') {
                setupUserMenu();
            } else {
                // Si la función no está disponible directamente, intentar inicializar manualmente
                const userMenu = authSection.querySelector('.user-menu');
                const username = userMenu?.querySelector('.username');
                const dropdown = userMenu?.querySelector('.dropdown-content');
                
                if (username && dropdown) {
                    username.addEventListener('click', (e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        dropdown.classList.toggle('show');
                    });
                    
                    dropdown.addEventListener('click', (e) => {
                        e.stopPropagation();
                    });
                }
            }
        } else {
            // Usuario no autenticado
            authSection.innerHTML = `<a href="/login" class="login-btn">Iniciar sesión</a>`;
        }
    },
    
    // Verificar si el usuario está autenticado
    isAuthenticated: function() {
        return !!this.currentUser;
    }
};

// Inicializar el servicio de autenticación cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    AuthService.init();
});