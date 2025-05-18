/**
 * Configuración de preconexiones para BookMatch.
 * Establece conexiones previas con servicios externos
 * para mejorar el rendimiento de carga.
 */

// Lista de servicios externos a los que nos conectaremos previamente
const EXTERNAL_SERVICES = [
  // CDNs y recursos externos comunes
  'https://cdn.jsdelivr.net',
  'https://fonts.googleapis.com',
  'https://fonts.gstatic.com',
  'https://api.bookcover.longitood.com', // API para portadas de libros
  'https://books.google.com',             // Google Books API
  'https://openlibrary.org',              // Open Library API
  'https://goodreads-covers.firebaseapp.com' // Portadas de Goodreads
];

/**
 * Establece preconexiones con servicios externos para mejorar
 * el rendimiento de carga.
 */
function setupPreconnections() {
  // Verificar si el navegador soporta link rel=preconnect
  const supportsPreconnect = document.createElement('link').relList.supports('preconnect');
  
  EXTERNAL_SERVICES.forEach(url => {
    // Crear link para preconnect
    if (supportsPreconnect) {
      const preconnect = document.createElement('link');
      preconnect.rel = 'preconnect';
      preconnect.href = url;
      preconnect.crossOrigin = 'anonymous';
      document.head.appendChild(preconnect);
    }
    
    // Crear link para dns-prefetch (como fallback o complemento)
    const dnsPrefetch = document.createElement('link');
    dnsPrefetch.rel = 'dns-prefetch';
    dnsPrefetch.href = url;
    document.head.appendChild(dnsPrefetch);
  });
}

// Ejecutar configuración de preconexiones
document.addEventListener('DOMContentLoaded', setupPreconnections);

// Exportar funciones para uso en otros scripts
window.BookMatchResourcePreconnect = {
  setupPreconnections,
  preconnectTo: (url) => {
    if (url && EXTERNAL_SERVICES.indexOf(url) === -1) {
      EXTERNAL_SERVICES.push(url);
      
      const preconnect = document.createElement('link');
      preconnect.rel = 'preconnect';
      preconnect.href = url;
      preconnect.crossOrigin = 'anonymous';
      document.head.appendChild(preconnect);
      
      const dnsPrefetch = document.createElement('link');
      dnsPrefetch.rel = 'dns-prefetch';
      dnsPrefetch.href = url;
      document.head.appendChild(dnsPrefetch);
    }
  }
};