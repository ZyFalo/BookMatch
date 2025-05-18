/**
 * Optimización de recursos para BookMatch
 * 
 * Este script realiza precarga de recursos críticos y gestiona la 
 * conexión con recursos de terceros para mejorar el rendimiento.
 */

// Recursos que se precargarán cuando el navegador esté inactivo
const resourcesToPrefetch = [
  // Iconos y recursos estáticos comunes
  '/static/img/logo.webp',
  'https://cdn.jsdelivr.net/npm/remixicon@2.5.0/fonts/remixicon.woff2',
  '/static/css/styles.min.css',
  
  // Imágenes que pueden usarse en diferentes páginas
  '/static/img/book1.webp',
  '/static/img/authors/george-martin.webp'
];

// Precarga recursos importantes usando requestIdleCallback
if ('requestIdleCallback' in window) {
  requestIdleCallback(() => {
    resourcesToPrefetch.forEach(resource => {
      const hint = document.createElement('link');
      hint.rel = 'prefetch';
      hint.href = resource;
      document.head.appendChild(hint);
    });
  });
}

// Establece conexión en paralelo para recursos que se usarán pronto
function preconnectTo(url) {
  if (!url || typeof url !== 'string') return;
  
  // Verificar si ya existe un preconnect para este origen
  const existingPreconnect = document.querySelector(`link[rel="preconnect"][href="${url}"]`);
  
  if (!existingPreconnect) {
    const link = document.createElement('link');
    link.rel = 'preconnect';
    link.href = url;
    link.crossOrigin = 'anonymous';
    document.head.appendChild(link);
    
    // Agregar también dns-prefetch como fallback para navegadores antiguos
    const dns = document.createElement('link');
    dns.rel = 'dns-prefetch';
    dns.href = url;
    document.head.appendChild(dns);
  }
}

// Monitorea las interacciones con los enlaces y precarga destinos
document.addEventListener('DOMContentLoaded', () => {
  // Monitorear hover en enlaces de navegación para precargar destinos
  const navLinks = document.querySelectorAll('.nav-links a');
  
  navLinks.forEach(link => {
    link.addEventListener('mouseenter', () => {
      // Precargar página al pasar el mouse
      const href = link.getAttribute('href');
      if (href && !href.startsWith('#') && href !== '/') {
        const preloadLink = document.createElement('link');
        preloadLink.rel = 'prefetch';
        preloadLink.href = href;
        document.head.appendChild(preloadLink);
      }
    });
  });
});