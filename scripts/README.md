# Scripts de Citas para BookMatch

Este directorio contiene scripts para extraer, mostrar e importar citas de Goodreads a la aplicación BookMatch.

## Descripción de los Scripts

### 1. `goodreads_quotes_scraper.py`

Extrae citas de la página de Goodreads (https://www.goodreads.com/quotes) y las guarda en un archivo JSON.

**Características:**
- Simula un navegador web para evitar bloqueos
- Extrae texto de la cita, autor e imagen
- Maneja múltiples páginas
- Guarda los resultados en formato JSON

### 2. `view_quotes.py`

Muestra las citas extraídas en un formato agradable en la consola.

**Características:**
- Carga automáticamente el archivo JSON más reciente
- Muestra las citas con formato legible
- Permite seleccionar cuántas citas mostrar

### 3. `import_quotes_to_db.py`

Importa las citas extraídas a la base de datos MongoDB de BookMatch.

**Características:**
- Conecta con la base de datos de BookMatch
- Añade metadatos adicionales a cada cita
- Previene duplicados con identificadores únicos

## Requisitos

Estos scripts requieren las siguientes dependencias:

```bash
pip install requests beautifulsoup4 motor
```

## Uso

### Extraer citas

```bash
cd /ruta/a/BookMatch
python scripts/goodreads_quotes_scraper.py
```

Las citas se guardarán en el directorio `data` con un nombre basado en la fecha y hora.

### Ver citas extraídas

```bash
python scripts/view_quotes.py
```

### Importar citas a la base de datos

```bash
python scripts/import_quotes_to_db.py
```

## Notas

- El scraper respeta los tiempos entre solicitudes para evitar sobrecargar el servidor de Goodreads
- Por defecto, el scraper está configurado para extraer solo 3 páginas para pruebas
- Los archivos JSON se guardan en el directorio `data` con marcas de tiempo

## Advertencia

Este scraper se proporciona solo con fines educativos. El scraping de sitios web puede estar sujeto a restricciones legales y condiciones de servicio específicas. Asegúrese de revisar y cumplir con los términos de servicio de Goodreads antes de utilizar este scraper. El uso excesivo o agresivo del scraper puede resultar en la prohibición de su dirección IP.