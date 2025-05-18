#!/usr/bin/env python3
"""
Goodreads Quote Scraper

Este script extrae citas de la página de Goodreads (https://www.goodreads.com/quotes)
simulando un navegador web y recorriendo múltiples páginas.

Las citas extraídas incluyen:
- Texto de la cita
- Autor de la cita
- URL de la imagen (si está disponible)

Características:
- Evita duplicados verificando los archivos JSON previos
- Continúa desde donde se quedó la última ejecución
- Guarda los resultados en la carpeta 'data'
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import json
import os
import glob
from datetime import datetime
import hashlib

class GoodreadsQuoteScraper:
    def __init__(self, max_pages=5, delay_between_requests=(1, 3)):
        """
        Inicializa el scraper de citas de Goodreads.
        
        Args:
            max_pages: Número máximo de páginas a scrapear
            delay_between_requests: Rango de tiempo (min, max) entre solicitudes
        """
        self.base_url = "https://www.goodreads.com/quotes"
        self.max_pages = max_pages
        self.delay_range = delay_between_requests
        self.quotes = []
        self.existing_quotes_hashes = set()  # Para evitar duplicados
        self.starting_page = 1  # Página desde la que comenzamos a scraper
        
        # Headers para simular un navegador
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'https://www.goodreads.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        
        # Cargar citas existentes para evitar duplicados
        self._load_existing_quotes()
    
    def _generate_quote_hash(self, quote, author):
        """
        Genera un hash único para una cita basado en su texto y autor.
        
        Args:
            quote: Texto de la cita
            author: Nombre del autor
            
        Returns:
            String con el hash que identifica la cita
        """
        # Normalizar texto para comparación consistente
        quote_text = quote.lower().strip()
        author_text = author.lower().strip()
        
        # Crear hash combinado
        combined = f"{quote_text}|{author_text}"
        return hashlib.md5(combined.encode('utf-8')).hexdigest()
    
    def _load_existing_quotes(self):
        """
        Carga las citas existentes de todos los archivos JSON generados
        para evitar duplicados y determinar desde qué página continuar.
        """
        # Directorio de datos relativo a la ubicación del script
        data_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
        
        # Asegurarse de que el directorio exista
        os.makedirs(data_dir, exist_ok=True)
        
        # Buscar todos los archivos JSON de citas anteriores
        json_files = glob.glob(os.path.join(data_dir, "goodreads_quotes_*.json"))
        
        if not json_files:
            print("No se encontraron archivos JSON previos. Comenzando desde la página 1.")
            return
        
        total_quotes = 0
        total_files = len(json_files)
        
        print(f"Verificando {total_files} archivos JSON existentes...")
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    existing_quotes = json.load(f)
                    
                # Guardar hashes de todas las citas existentes
                file_quotes = 0
                for quote in existing_quotes:
                    quote_hash = self._generate_quote_hash(quote['quote'], quote['author'])
                    self.existing_quotes_hashes.add(quote_hash)
                    file_quotes += 1
                    
                total_quotes += file_quotes
                print(f"  - {os.path.basename(json_file)}: {file_quotes} citas procesadas")
                    
            except Exception as e:
                print(f"  - Error al cargar citas de {os.path.basename(json_file)}: {e}")
        
        print(f"Se cargaron {len(self.existing_quotes_hashes)} citas únicas de {total_quotes} citas totales en {total_files} archivos.")
    
    def _get_page(self, page_num=1):
        """
        Obtiene el HTML de una página específica.
        
        Args:
            page_num: Número de página a obtener
            
        Returns:
            BeautifulSoup object del HTML analizado
        """
        url = f"{self.base_url}?page={page_num}"
        print(f"Obteniendo página {page_num}...")
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Lanza excepción si no es 200 OK
            
            # Esperamos un tiempo aleatorio para evitar detección
            delay = random.uniform(*self.delay_range)
            time.sleep(delay)
            
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener la página {page_num}: {e}")
            return None
    
    def _extract_quotes_from_page(self, soup, check_duplicates=False):
        """
        Extrae todas las citas de una página.
        
        Args:
            soup: BeautifulSoup object de la página
            check_duplicates: Si es True, verifica duplicados para determinar 
                             la página desde la que continuar
            
        Returns:
            Lista de citas extraídas y un valor booleano que indica si todas las citas eran duplicadas
        """
        if not soup:
            return [], False
        
        page_quotes = []
        all_duplicate = True  # Asumimos que todas son duplicadas inicialmente
        quotes_divs = soup.find_all("div", class_="quote")
        
        for quote_div in quotes_divs:
            try:
                # Extraer el texto de la cita
                quote_text_div = quote_div.find("div", class_="quoteText")
                if not quote_text_div:
                    continue
                
                # Extraer texto de la cita correctamente y eliminar comillas
                quote_content = quote_text_div.get_text(strip=True)
                try:
                    if '"' in quote_content:
                        parts = quote_content.split('"')
                        if len(parts) >= 3:  # Asegurarse de que hay texto entre comillas
                            quote_text = parts[1].strip()
                        else:
                            quote_text = quote_content.strip()
                    else:
                        quote_text = quote_content.strip()
                    
                    # Eliminar cualquier comilla restante y limpiar el texto
                    quote_text = quote_text.replace('"', '').replace('"', '')
                    
                    # Si hay un guión seguido por el autor, eliminar esa parte
                    if "―" in quote_text:
                        quote_text = quote_text.split("―")[0].strip()
                except:
                    quote_text = quote_content.strip()
                
                # Extraer el autor
                author_span = quote_text_div.find("span", class_="authorOrTitle")
                author = author_span.get_text(strip=True) if author_span else "Desconocido"
                
                # Verificar si esta cita ya existe
                quote_hash = self._generate_quote_hash(quote_text, author)
                
                if quote_hash in self.existing_quotes_hashes and check_duplicates:
                    continue  # Saltar esta cita si estamos verificando duplicados
                
                # Si llegamos aquí, al menos una cita no es duplicada
                all_duplicate = False
                
                # Añadir a la lista de hashes existentes para evitar duplicados en la misma ejecución
                self.existing_quotes_hashes.add(quote_hash)
                
                # Extraer URL de la imagen correctamente (del atributo src)
                img_tag = quote_div.find("img")
                img_url = img_tag.get("src") if img_tag else None
                
                # Extraer tags (los tres primeros)
                tags = []
                quote_footer = quote_div.find("div", class_="quoteFooter")
                if quote_footer:
                    tag_links = quote_footer.find_all("a")
                    for i, tag_link in enumerate(tag_links):
                        if i < 3:  # Tomar solo los tres primeros tags
                            tag_text = tag_link.get_text(strip=True)
                            # Verificar que el tag no sea demasiado largo (evitar tags incorrectos)
                            if tag_text and len(tag_text) < 30:
                                tags.append(tag_text)
                
                page_quotes.append({
                    "quote": quote_text,
                    "author": author,
                    "image_url": img_url,
                    "tags": tags
                })
                
            except Exception as e:
                print(f"Error al procesar una cita: {e}")
                continue
        
        return page_quotes, all_duplicate
    
    def find_starting_page(self):
        """
        Determina desde qué página comenzar el scraping basado en las citas existentes.
        Busca la primera página que contenga citas que no hayamos recopilado previamente.
        """
        if not self.existing_quotes_hashes:
            return 1  # Si no hay citas previas, comenzar desde la página 1
            
        max_check_pages = 10  # Límite para no verificar demasiadas páginas
        
        for page_num in range(1, max_check_pages + 1):
            print(f"Verificando página {page_num} para encontrar nuevas citas...")
            soup = self._get_page(page_num)
            if not soup:
                break
                
            # Verificar si esta página contiene citas nuevas
            _, all_duplicate = self._extract_quotes_from_page(soup, check_duplicates=True)
            
            if not all_duplicate:
                print(f"Página {page_num} contiene nuevas citas. Comenzando desde aquí.")
                return page_num
        
        print(f"No se encontraron nuevas citas en las primeras {max_check_pages} páginas.")
        return max_check_pages + 1  # Comenzar desde la siguiente página después de las verificadas
    
    def scrape(self):
        """
        Realiza el scraping de múltiples páginas de citas.
        
        Returns:
            Lista de citas extraídas
        """
        self.quotes = []
        
        # Determinar desde qué página comenzar (si hay archivos previos)
        if self.existing_quotes_hashes:
            self.starting_page = self.find_starting_page()
        
        pages_processed = 0
        current_page = self.starting_page
        
        while pages_processed < self.max_pages:
            soup = self._get_page(current_page)
            if not soup:
                break
                
            page_quotes, _ = self._extract_quotes_from_page(soup)
            
            if page_quotes:
                self.quotes.extend(page_quotes)
                print(f"Página {current_page}: {len(page_quotes)} citas extraídas")
                pages_processed += 1
            else:
                print(f"No se encontraron citas en la página {current_page}")
            
            current_page += 1
            
            # Verificamos si hay más páginas
            next_page = soup.find("a", class_="next_page")
            if not next_page:
                print("No hay más páginas disponibles.")
                break
        
        print(f"Total: {len(self.quotes)} nuevas citas extraídas comenzando desde la página {self.starting_page}")
        return self.quotes
    
    def save_to_json(self, filename=None):
        """
        Guarda las citas extraídas en un archivo JSON.
        
        Args:
            filename: Nombre del archivo JSON a crear
        """
        if not self.quotes:
            print("No hay citas para guardar.")
            return
            
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"goodreads_quotes_{timestamp}.json"
        
        # Directorio de datos relativo a la ubicación del script
        data_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
        output_path = os.path.join(data_dir, filename)
        
        # Asegurarse de que el directorio exista
        os.makedirs(data_dir, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.quotes, f, ensure_ascii=False, indent=2)
        
        print(f"Citas guardadas en: {output_path}")

# Ejecutar el scraper si se ejecuta directamente
if __name__ == "__main__":
    print("=== Iniciando Goodreads Quote Scraper ===")
    
    # Configuración
    max_pages = 5
    
    # Iniciar el scraper
    scraper = GoodreadsQuoteScraper(max_pages=max_pages)
    quotes = scraper.scrape()
    
    if quotes:
        # Mostrar algunas citas de ejemplo
        print("\n=== Ejemplos de citas extraídas ===")
        for i, quote in enumerate(quotes[:5], 1):  # Mostrar las primeras 5 citas
            print(f"\nCita #{i}:")
            print(f"{quote['quote'][:100]}..." if len(quote['quote']) > 100 else f"{quote['quote']}")
            print(f"Autor: {quote['author']}")
            print(f"Imagen: {quote['image_url']}")
            if quote['tags']:
                print(f"Tags: {', '.join(quote['tags'])}")
        
        # Guardar resultados
        scraper.save_to_json()
    else:
        print("No se encontraron nuevas citas para guardar.")
    
    print("\n=== Scraping completado ===")