/**
 * Optimización del Largest Contentful Paint (LCP) para BookMatch
 * 
 * Este script se enfoca en optimizar el LCP, una métrica crítica para Core Web Vitals
 * que mide el tiempo que tarda en renderizarse el elemento más grande del viewport inicial.
 */

// Lógica para informar sobre el rendimiento del LCP
const reportLCP = () => {
  // Verificar si la API de Web Vitals está disponible
  if ('PerformanceObserver' in window) {
    // Crear un observer para el LCP
    const lcpObserver = new PerformanceObserver((entryList) => {
      const entries = entryList.getEntries();
      const lastEntry = entries[entries.length - 1];
      
      // Reportar el LCP a la consola (en desarrollo)
      if (lastEntry) {
        console.log('LCP:', lastEntry.startTime);
        console.log('LCP Element:', lastEntry.element);
        
        // Aquí podrías enviar los datos a un servicio de analítica
        // si estuvieras en producción
      }
    });
    
    // Observar el LCP
    lcpObserver.observe({ type: 'largest-contentful-paint', buffered: true });
  }
};

// Optimizador del LCP
const optimizeLCP = () => {
  // Incluir el logo junto con las imágenes LCP
  const lcpElements = document.querySelectorAll('.lcp-image, .logo-img');
  lcpElements.forEach(img => {
    img.setAttribute('fetchpriority', 'high');
    
    if (img.style.opacity === '0' || img.style.visibility === 'hidden') {
      img.style.opacity = '1';
      img.style.visibility = 'visible';
    }
    
    if (!img.src && img.dataset.src) {
      img.src = img.dataset.src;
    }
  });
};

// Ejecutar las optimizaciones lo antes posible
document.addEventListener('DOMContentLoaded', () => {
  optimizeLCP();
  reportLCP();
});

// También intentar ejecutar antes de DOMContentLoaded si es posible
if (document.readyState === 'loading') {
  // Documento aún cargando, usar la primera oportunidad
  document.addEventListener('readystatechange', () => {
    if (document.readyState === 'interactive') {
      optimizeLCP();
    }
  });
} else {
  // Documento ya ha sido cargado (navegación de historial o carga diferida)
  optimizeLCP();
}

// Exportar para uso externo
window.BookMatchLCPOptimizer = {
  optimizeLCP,
  reportLCP
};