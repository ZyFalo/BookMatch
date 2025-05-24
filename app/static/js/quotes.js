/**
 * Script para mostrar una cita aleatoria en la sección quote-section usando JS nativo
 */
async function loadRandomQuote() {
    try {
        const response = await fetch('/quotes/random');
        if (response.ok) {
            const data = await response.json();

            const quoteText = document.getElementById('quote-text');
            const quoteAuthor = document.getElementById('quote-author');
            const img = document.getElementById('quote-author-img');

            // Limpieza: quitar comillas (“” o ") al inicio/final y coma al final del autor
            if (data.quote && quoteText)
                quoteText.textContent = data.quote.replace(/^["“”]+|["“”]+$/g, '');

            if (data.author && quoteAuthor)
                quoteAuthor.textContent = `- ${data.author.replace(/,+$/, '')}`;

            if (img) {
                img.src = data.image_url || '/static/img/authors/default.webp';
                img.alt = data.author || 'Autor';
                img.width = 80;
                img.height = 80;
            }

        } else {
            console.error("Error al obtener la cita:", response.status, response.statusText);
            const quoteText = document.getElementById('quote-text');
            const quoteAuthor = document.getElementById('quote-author');
            if (quoteText) quoteText.textContent = "No se pudo cargar la cita.";
            if (quoteAuthor) quoteAuthor.textContent = "";
        }
    } catch (e) {
        console.error("Excepción al cargar la cita:", e);
        const quoteText = document.getElementById('quote-text');
        const quoteAuthor = document.getElementById('quote-author');
        if (quoteText) quoteText.textContent = "No se pudo cargar la cita.";
        if (quoteAuthor) quoteAuthor.textContent = "";
    }
}

// Llama a la función al cargar la página
document.addEventListener('DOMContentLoaded', loadRandomQuote);