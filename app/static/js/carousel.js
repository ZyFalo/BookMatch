/**
 * Carrusel de imágenes automático para BookMatch
 * Maneja la rotación automática de imágenes en la página principal
 */
document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar elementos del carrusel
    const carouselContainer = document.querySelector('.carousel-container');
    if (!carouselContainer) return;

    const slides = document.querySelectorAll('.carousel-slide');
    const indicatorsContainer = document.querySelector('.carousel-indicators');
    
    // Variables de control
    let currentSlide = 0;
    const slideCount = slides.length;
    let interval;
    let isHovering = false;
    
    // Crear indicadores dinámicamente
    if (indicatorsContainer) {
        for (let i = 0; i < slideCount; i++) {
            const indicator = document.createElement('div');
            indicator.classList.add('carousel-indicator');
            if (i === 0) indicator.classList.add('active');
            indicator.dataset.slideIndex = i;
            
            // Agregar evento para cambiar al hacer clic en indicador
            indicator.addEventListener('click', () => {
                goToSlide(i);
                resetInterval();
            });
            
            indicatorsContainer.appendChild(indicator);
        }
    }
    
    // Función para mostrar una diapositiva específica
    function goToSlide(slideIndex) {
        // Ocultar todas las diapositivas
        slides.forEach((slide, index) => {
            slide.style.opacity = 0;
            slide.style.visibility = 'hidden';
            
            // Actualizar indicadores si existen
            if (indicatorsContainer) {
                const indicators = indicatorsContainer.querySelectorAll('.carousel-indicator');
                if (indicators[index]) {
                    indicators[index].classList.remove('active');
                }
            }
        });
        
        // Mostrar la diapositiva actual
        slides[slideIndex].style.opacity = 1;
        slides[slideIndex].style.visibility = 'visible';
        
        // Actualizar el indicador actual
        if (indicatorsContainer) {
            const indicators = indicatorsContainer.querySelectorAll('.carousel-indicator');
            if (indicators[slideIndex]) {
                indicators[slideIndex].classList.add('active');
            }
        }
        
        // Actualizar el índice actual
        currentSlide = slideIndex;
    }
    
    // Función para pasar a la siguiente diapositiva
    function nextSlide() {
        if (isHovering) return;
        const next = (currentSlide + 1) % slideCount;
        goToSlide(next);
    }
    
    // Función para pasar a la diapositiva anterior
    function prevSlide() {
        if (isHovering) return;
        const prev = (currentSlide - 1 + slideCount) % slideCount;
        goToSlide(prev);
    }
    
    // Función para reiniciar el intervalo de rotación
    function resetInterval() {
        clearInterval(interval);
        interval = setInterval(nextSlide, 5000); // Cambiar cada 5 segundos
    }
    
    // Configurar eventos de hover para pausar la rotación
    carouselContainer.addEventListener('mouseenter', () => {
        isHovering = true;
    });
    
    carouselContainer.addEventListener('mouseleave', () => {
        isHovering = false;
    });
    
    // Configurar navegación con teclado
    document.addEventListener('keydown', (e) => {
        // Solo funciona si el carrusel está en el viewport
        const rect = carouselContainer.getBoundingClientRect();
        const isInViewport = (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
        
        if (!isInViewport) return;
        
        if (e.key === 'ArrowLeft') {
            prevSlide();
            resetInterval();
        } else if (e.key === 'ArrowRight') {
            nextSlide();
            resetInterval();
        }
    });
    
    // Configurar navegación por gestos táctiles (swipe)
    let touchStartX = 0;
    let touchEndX = 0;
    
    carouselContainer.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    
    carouselContainer.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });
    
    function handleSwipe() {
        const swipeThreshold = 50; // Píxeles mínimos para considerar un swipe
        
        if (touchEndX - touchStartX > swipeThreshold) {
            // Swipe a la derecha - diapositiva anterior
            prevSlide();
            resetInterval();
        } else if (touchStartX - touchEndX > swipeThreshold) {
            // Swipe a la izquierda - siguiente diapositiva
            nextSlide();
            resetInterval();
        }
    }
    
    // Inicializar: mostrar la primera diapositiva
    goToSlide(0);
    
    // Iniciar la rotación automática
    resetInterval();
});