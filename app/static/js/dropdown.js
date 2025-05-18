// Función global para configurar menús desplegables en toda la aplicación
function setupUserMenu() {
    const userMenus = document.querySelectorAll('.user-menu');
    
    userMenus.forEach(menu => {
        const usernameElement = menu.querySelector('.username');
        const dropdownContent = menu.querySelector('.dropdown-content');
        
        if (usernameElement && dropdownContent) {
            // Asegurarnos de que no añadimos listeners duplicados
            usernameElement.removeEventListener('click', toggleDropdown);
            usernameElement.addEventListener('click', toggleDropdown);
            
            function toggleDropdown(e) {
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
            }
            
            // Evitar que los clics dentro del menú desplegable lo cierren
            dropdownContent.removeEventListener('click', stopPropagation);
            dropdownContent.addEventListener('click', stopPropagation);
            
            function stopPropagation(e) {
                e.stopPropagation();
            }
        }
    });
}

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

// Ejecutar la función cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', setupUserMenu);