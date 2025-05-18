/**
 * Manejo del menú desplegable de usuario en BookMatch
 * Permite que el menú permanezca abierto al hacer clic y se cierre al hacer clic fuera de él
 */
document.addEventListener('DOMContentLoaded', function() {
    // Manejador para el menú desplegable de usuario
    function setupUserMenu() {
        const userMenus = document.querySelectorAll('.user-menu');
        
        userMenus.forEach(menu => {
            const usernameElement = menu.querySelector('.username');
            const dropdownContent = menu.querySelector('.dropdown-content');
            
            if (usernameElement && dropdownContent) {
                // Alternar menú al hacer clic en el nombre de usuario
                usernameElement.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Si ya está abierto, lo cerramos
                    if (dropdownContent.classList.contains('show')) {
                        dropdownContent.classList.remove('show');
                    } else {
                        // Cerrar cualquier otro menú abierto primero
                        const openDropdowns = document.querySelectorAll('.dropdown-content.show');
                        openDropdowns.forEach(dropdown => {
                            dropdown.classList.remove('show');
                        });
                        
                        // Abrir este menú
                        dropdownContent.classList.add('show');
                    }
                });
                
                // Evitar que los clics dentro del menú desplegable lo cierren
                dropdownContent.addEventListener('click', function(e) {
                    e.stopPropagation();
                });
            }
        });
        
        // Cerrar todos los menús desplegables al hacer clic en cualquier parte del documento
        document.addEventListener('click', function(e) {
            // Solo cerrar si el clic no fue en algún botón del menú
            if (!e.target.closest('.user-menu')) {
                const openDropdowns = document.querySelectorAll('.dropdown-content.show');
                openDropdowns.forEach(dropdown => {
                    dropdown.classList.remove('show');
                });
            }
        });
    }
    
    // Inicializar el manejo del menú de usuario
    setupUserMenu();
});