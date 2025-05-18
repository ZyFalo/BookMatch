/**
 * Módulo de lazy loading para BookMatch
 * Carga imágenes solo cuando están cerca de entrar en el viewport
 */
document.addEventListener('DOMContentLoaded', function() {
    // Solo inicializar si IntersectionObserver está disponible
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                // Si la imagen está en o cerca del viewport
                if (entry.isIntersecting) {
                    const img = entry.target;
                    const src = img.getAttribute('data-src');
                    
                    if (src) {
                        img.src = src;
                        img.removeAttribute('data-src');
                        img.classList.add('loaded');
                    }
                    
                    // Dejar de observar la imagen una vez que está cargada
                    imageObserver.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px 0px', // Cargar imágenes cuando están a 50px de entrar en el viewport
            threshold: 0.01 // Umbral bajo para iniciar la carga pronto
        });
        
        // Observar todas las imágenes con atributo data-src
        lazyImages.forEach(function(img) {
            imageObserver.observe(img);
        });
    } else {
        // Fallback para navegadores que no admiten IntersectionObserver
        document.querySelectorAll('img[data-src]').forEach(function(img) {
            img.src = img.getAttribute('data-src');
            img.removeAttribute('data-src');
        });
    }
});