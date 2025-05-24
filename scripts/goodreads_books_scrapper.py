import os
import json
import glob
import time
import random
import hashlib
import requests
from bs4 import BeautifulSoup

class GoodreadsBookScraper:
    def __init__(self, delay_between_requests=(1, 2)):
        self.list_url = "https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century?page={}"
        self.base_url = "https://www.goodreads.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        self.delay = delay_between_requests
        self.books = []
        self.data_dir = os.path.join(os.getcwd(), "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self.existing_hashes = set()
        self.max_pages = None
        self._load_existing_books()

    def _generate_hash(self, title, author):
        combo = f"{title.strip().lower()}|{author.strip().lower()}"
        return hashlib.md5(combo.encode('utf-8')).hexdigest()

    def _load_existing_books(self):
        json_files = glob.glob(os.path.join(self.data_dir, "goodreads_books_*.json"))
        for file in json_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for book in data:
                        h = self._generate_hash(book['titulo'], book['autor'])
                        self.existing_hashes.add(h)
            except:
                continue
        print(f"Libros previos cargados: {len(self.existing_hashes)}")

    def _get_detail_data(self, relative_url):
        full_url = self.base_url + relative_url
        try:
            # print(f"\n Accediendo a detalles del libro: {full_url}")
            r = requests.get(full_url, headers=self.headers)
            soup = BeautifulSoup(r.text, "html.parser")

            # Descripción
            resumen_tag = soup.select_one('div[data-testid="description"] span.Formatted')
            resumen = resumen_tag.get_text(" ", strip=True) if resumen_tag else ""
            if not resumen:
                print(f"[WARN] No se encontró resumen en: {full_url}")
            # else:
            #     print(f"[INFO] Resumen encontrado ({len(resumen)} caracteres)")

            # Géneros basados en el DOM
            tags = []
            genre_section = soup.select_one('div[data-testid="genresList"]')
            if genre_section:
                genre_spans = genre_section.select('span.BookPageMetadataSection__genreButton')
                # print(f"[INFO] Se encontraron {len(genre_spans)} contenedores de género.")
                for i, span_wrap in enumerate(genre_spans):
                    label = span_wrap.select_one('span.Button__labelItem')
                    if label:
                        genre_text = label.get_text(strip=True)
                        # print(f"[INFO] Género {i+1}: {genre_text}")
                        tags.append(genre_text)
                    else:
                        print(f"[WARN] Contenedor {i+1} no tiene span.Button__labelItem")
            else:
                print(f"[WARN] No se encontró div[data-testid='genresList'] en: {full_url}")

            return resumen, tags

        except Exception as e:
            print(f"Error al acceder a detalle {relative_url}: {e}")
            return "", []

    def _get_max_pages(self, soup):
        pagination_links = soup.select(".pagination a[href*='page=']")
        pages = []
        for link in pagination_links:
            try:
                page_number = int(link.text.strip())
                pages.append(page_number)
            except:
                continue
        return max(pages) if pages else 1

    def scrape_books(self):
        page = 1
        # max_books = 101  # <-- Comenta o elimina esta línea
        # books_scraped = 0  # <-- Comenta o elimina esta línea
        while True:
            print(f"\nScrapeando página {page}...")
            try:
                r = requests.get(self.list_url.format(page), headers=self.headers)
                soup = BeautifulSoup(r.text, "html.parser")
    
                if self.max_pages is None:
                    self.max_pages = self._get_max_pages(soup)
                    print(f"Total de páginas detectadas: {self.max_pages}")
    
                books_html = soup.select("tr[itemtype='http://schema.org/Book']")
    
                for row in books_html:
                    # if books_scraped >= max_books:
                    #     print(f"Límite de {max_books} libros alcanzado. Deteniendo scrapeo.")
                    #     self._save_books()
                    #     return
                    try:
                        # Extraer título
                        title_tag = row.select_one("a.bookTitle span")
                        title = title_tag.get_text(strip=True) if title_tag else "Sin título"

                        # Extraer autor
                        author_tag = row.select_one("a.authorName span")
                        author = author_tag.get_text(strip=True) if author_tag else "Desconocido"

                        # Extraer enlace de detalles
                        detail_link_tag = row.select_one("a.bookTitle")
                        detail_link = detail_link_tag['href'] if detail_link_tag and 'href' in detail_link_tag.attrs else None

                        # Generar hash para evitar duplicados
                        h = self._generate_hash(title, author)
                        if h in self.existing_hashes:
                            print(f"[SKIP] Libro duplicado: {title} - {author}")
                            continue

                        # Obtener resumen y géneros
                        resumen, tags = self._get_detail_data(detail_link) if detail_link else ("", [])

                        # Crear diccionario del libro
                        book = {
                            "titulo": title,
                            "autor": author,
                            "resumen": resumen,
                            "generos": tags,
                            "detalle_url": self.base_url + detail_link if detail_link else ""
                        }

                        self.books.append(book)
                        self.existing_hashes.add(h)
                        # books_scraped += 1  # <-- Comenta o elimina esta línea
                        print(f"Añadido: {title} ({len(tags)} géneros)")
    
                        time.sleep(random.uniform(*self.delay))
    
                    except Exception as inner_e:
                        print(f"Error en fila: {inner_e}")
                        continue
    
                page += 1
                if page > self.max_pages:
                    print("Fin del paginado.")
                    break
    
            except Exception as e:
                print(f"Error en la página {page}: {e}")
                break
    
        self._save_books()

    def _save_books(self):
        if not self.books:
            print("No hay libros nuevos para guardar.")
            return

        timestamp = int(time.time())
        path = os.path.join(self.data_dir, f"goodreads_books_{timestamp}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=2)
        print(f"\nGuardado {len(self.books)} libros nuevos en {path}")


if __name__ == "__main__":
    scraper = GoodreadsBookScraper()
    scraper.scrape_books()
