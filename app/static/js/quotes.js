/**
 * Script para manejar el cambio de frases en la sección quote-section
 */
document.addEventListener('DOMContentLoaded', function() {
    const quoteSlider = document.getElementById('quote-slider');
    if (!quoteSlider) return;
    
    const quotes = quoteSlider.querySelectorAll('.quote-slide');
    if (quotes.length <= 1) return;
    
    let currentQuoteIndex = 0;
    
    // Función para cambiar a la siguiente frase
    function nextQuote() {
        // Quitar la clase active de la frase actual
        quotes[currentQuoteIndex].classList.remove('active');
        
        // Calcular el índice de la siguiente frase
        currentQuoteIndex = (currentQuoteIndex + 1) % quotes.length;
        
        // Añadir la clase active a la nueva frase actual
        quotes[currentQuoteIndex].classList.add('active');
    }
    
    // Cambiar la frase cada 8 segundos
    setInterval(nextQuote, 8000);
});