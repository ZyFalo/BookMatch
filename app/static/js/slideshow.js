/**
 * Slideshow automático para la sección hero de BookMatch
 * Cambia las imágenes cada cierto tiempo con una transición suave
 * Implementa lazy loading para cargar imágenes solo cuando son necesarias
 */
document.addEventListener('DOMContentLoaded', function() {
    // Obtener el contenedor del slideshow
    const slideshow = document.getElementById('hero-slideshow');
    if (!slideshow) return;

    // Obtener todas las imágenes dentro del slideshow
    const images = slideshow.querySelectorAll('img');
    if (images.length <= 1) return; // No hay suficientes imágenes para hacer un slideshow

    let currentImageIndex = 0;
    let nextImageIndex = 1; // Para precargar la siguiente imagen
    
    // Función para cargar una imagen usando su atributo data-src
    function loadImage(img) {
        const dataSrc = img.getAttribute('data-src');
        if (dataSrc) {
            img.setAttribute('src', dataSrc);
            img.removeAttribute('data-src');
            return true;
        }
        return false;
    }
    
    // Precargar la siguiente imagen
    function preloadNextImage() {
        const nextIndex = (currentImageIndex + 1) % images.length;
        if (images[nextIndex] && images[nextIndex].hasAttribute('data-src')) {
            loadImage(images[nextIndex]);
        }
    }
    
    // Función para cambiar a la siguiente imagen
    function nextImage() {
        // Quitar la clase active de la imagen actual
        images[currentImageIndex].classList.remove('active');
        
        // Calcular el índice de la siguiente imagen
        currentImageIndex = (currentImageIndex + 1) % images.length;
        
        // Cargar la imagen si aún no está cargada
        loadImage(images[currentImageIndex]);
        
        // Añadir la clase active a la nueva imagen actual
        images[currentImageIndex].classList.add('active');
        
        // Precargar la imagen que vendrá después
        preloadNextImage();
    }
    
    // Cargar inicialmente la primera imagen activa y la siguiente
    for (let i = 0; i < Math.min(2, images.length); i++) {
        if (i > 0 && images[i].hasAttribute('data-src')) {
            loadImage(images[i]);
        }
    }
    
    // Cambiar la imagen cada 5 segundos
    setInterval(nextImage, 5000);
});