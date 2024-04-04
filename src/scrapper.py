import requests
from bs4 import BeautifulSoup
import re 
from libro import Libro
import threading 
import json 
import pandas as pd 
import csv 
import shutil
import datetime
from datetime import datetime as dt
import os
import config 
class Scrapper:
    books = {}
    book_names = []
    book_categories = {}
    def __init__(self, target_url='http://books.toscrape.com/'):
        self.target_url = target_url
        # Create a new directory with the current date and time
        current_time = dt.now().strftime('%Y%m%d-%H%M')
        self.output_dir = fr'resultados/{current_time}'
        self.output_dir_images = fr'resultados/{current_time}/imagenes'
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.output_dir_images, exist_ok=True)


    def descarga_simple(self, element,soup, output_format, min_price = None,  max_price = None, min_rating = None,  max_rating = None, specific_name = None):
        """Descarga solo la ficha visible en el catágolo de libros."""
        link = element.find('a').get('href')
        book_name = element.find('h3').get_text()
        price = element.find(class_='price_color').get_text()
        price = re.sub(r'[^0-9.]', '', price)
        price = float(price)
        rating_element = soup.find(class_=re.compile('star-rating*'))
        rating = ''.join(rating_element.get('class')).replace('star-rating','')
        
        # Bloque de control sobre rating precios y nombre. 
        if min_price and max_price:
            if price < float(min_price) or price > float(max_price):
                return
        if min_rating and max_rating:
            rating_numerico = self.rating_to_number(rating)
            if rating_numerico < int(min_rating) or rating_numerico > int(max_rating):
                return
        if specific_name:   
            if specific_name.lower() not in book_name.lower():
                return

        for name in self.book_names:
            if book_name in name:
                nombre_inferido = name
                return
            else:
                book_name = re.sub(r'\W+', '_', book_name)
                
        if not self.book_names:
            nombre_inferido = re.sub(r'\W+', '_', book_name)
        data = {
                'nombre': nombre_inferido,
                'ruta_ficha': link,
                'precio': price,
                'rating': rating,
                'id': None,
                'categoria': None,
                'imagen': None
        }
        libro = Libro(data)
        self.books[book_name] = libro
        self.descargar_ficha_libro(libro,output_format)


    def descarga_completa(self, element,soup, output_format, min_price = None,  max_price = None, min_rating = None,  max_rating = None, specific_name = None):
            """Descarga la ficha completa de un libro."""
            book_name = element.find('h3').get_text()
            link = element.find('a').get('href')
            price = element.find(class_='price_color').get_text()
            price = re.sub(r'[^0-9.]', '', price)
            price = float(price)
            rating_element = soup.find(class_=re.compile('star-rating*'))
            rating = ''.join(rating_element.get('class')).replace('star-rating','') 

            # Bloque de control sobre rating precios y nombre. 
            if min_price and max_price:
                if price < float(min_price) or price > float(max_price):
                    return
            if min_rating and max_rating:
                rating_numerico = self.rating_to_number(rating)
                if rating_numerico < min_rating or rating_numerico > max_rating:
                    return

        # Go to the book's URL
            book_url = '/'.join(self.target_url.split('/')[:-1]) + '/' + link
            book_response = requests.get(book_url)
            book_soup = BeautifulSoup(book_response.text, 'html.parser')

        # Find the image element
            div_img = book_soup.find('div', class_='item active')
            img = div_img.find('img')
            img_url_cruda = img.get('src')
            img_url = img_url_cruda.replace('../../','http://books.toscrape.com/')

        # Nombre completo del libro
            # Find the div with class "col-sm-6 product_main"
            div_nombre = book_soup.find('div', class_='col-sm-6 product_main')

            # Find the h1 tag inside this div
            nombre_completo = div_nombre.find('h1').text
            nombre_completo_limpio = re.sub(r'\W+', '_', nombre_completo)
            if specific_name:   
                if specific_name.lower() not in nombre_completo_limpio.lower():
                    return
        # Download the image
            response = requests.get(img_url, stream=True)
            if response.status_code == 200:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                response.raw.decode_content = True

            img_path = str(os.path.join(self.output_dir_images, f'{nombre_completo_limpio}_image.jpg')).replace('\\\\','\\')
            with open(f'{img_path}', 'wb') as f:
                shutil.copyfileobj(response.raw, f)  

        # Get the UPC from the table
            upc = book_soup.find('table', class_='table table-striped').find('td').get_text()

        # Get the category from the breadcrumb
            breadcrumb = book_soup.find(class_='breadcrumb').find_all('a')
            category = breadcrumb[2].get_text() if len(breadcrumb) > 2 else None

            data = {
                'nombre': nombre_completo_limpio,
                'ruta_ficha': link,
                'precio': price,
                'rating': rating,
                'id': upc,
                'categoria': category,
                'imagen': f'{nombre_completo_limpio}_image.jpg'
            }
            libro = Libro(data)
            self.books[book_name] = libro

            self.descargar_ficha_libro(libro,output_format)

    def mapear(self,output_format, completo=False, min_price = None,  max_price = None, min_rating = None,  max_rating = None, specific_name = None):
        """Parses all books from the website. If completo is True, also downloads the book details."""
        contador = 0
        self.target_url = config.target_url
        print(f'Iniciando mapeo de libros en {self.target_url}')
        while self.target_url:
            response = requests.get(self.target_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            elements = soup.find_all(class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

            threads = []

            if completo:
                for element in elements:
                    t = threading.Thread(target=self.descarga_completa, args=(element,soup,output_format, min_price,  max_price, min_rating,  max_rating, specific_name))
                    t.start()
                    threads.append(t)
            else:
                for element in elements:
                    t = threading.Thread(target=self.descarga_simple, args=(element,soup,output_format, min_price,  max_price , min_rating,  max_rating, specific_name))
                    t.start()
                    threads.append(t)

            # Wait for all threads to finish
            for t in threads:
                t.join()

            next_page = soup.find(class_='next')
            if next_page:
                self.target_url = '/'.join(self.target_url.split('/')[:-1]) + '/' + next_page.find('a').get('href')
                contador = contador + 1
                print(f'Página {contador} mapeada')
            else:
                self.target_url = None


#             print(Fore.GREEN + "1- Descargar una lista con los libros disponibles")
    def get_nombre_libros(self):
        """Returns a list of all books available in the website."""
        while self.target_url:
            response = requests.get(self.target_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            elements = soup.find_all(class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

            threads = []
            for element in elements:
                link = element.find('a').get('href')
                t = threading.Thread(target=self.sacar_nombre_libro, args=(link,))
                t.start()
                threads.append(t) 

            # Wait for all threads to finish        
            for t in threads:
                t.join()

            next_page = soup.find(class_='next')
            if next_page:
                self.target_url = '/'.join(self.target_url.split('/')[:-1]) + '/' + next_page.find('a').get('href')
            else:
                self.target_url = None

    def get_categorias_libros(self):
            """Returns a list of all book categories available in the website."""
            print("SE HA EJECUTADO EL MÉTODO")
            response = requests.get(self.target_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the div with class "side_categories"
            side_categories = soup.find('div', class_='side_categories')

            # Find the ul tag beneath this div
            ul = side_categories.find('ul')

            # Find all li tags nested under this ul
            list_items = ul.find_all('li')
            for li in list_items:
                link = li.find('a')
                if link:
                    category_name = link.get_text().replace(' ', '').replace('\n', '').lower()
                    self.book_categories[category_name] = f'{self.target_url}{link.get("href")}'
            print(self.book_categories)



    def sacar_nombre_libro(self, link):
        """Returns the name of a book from an element."""
        book_url = '/'.join(self.target_url.split('/')[:-1]) + '/' + link
        book_response = requests.get(book_url)
        book_soup = BeautifulSoup(book_response.text, 'html.parser')
        # Nombre completo del libro
        # Find the div with class "col-sm-6 product_main"
        div_nombre = book_soup.find('div', class_='col-sm-6 product_main')
        # Find the h1 tag inside this div
        nombre_completo = div_nombre.find('h1').text
        nombre_completo_limpio = re.sub(r'\W+', '_', nombre_completo).lower()
        if nombre_completo_limpio not in self.book_names:
            self.book_names.append(nombre_completo_limpio)
        print(f'Found book: {nombre_completo}, parseado a {nombre_completo_limpio}')
        
    def get_categoria(self, categoria, completo=False, output_format='json'):
        """Downloads all books from the specified category. If completo is True, also downloads the book details"""
        self.target_url = self.book_categories[f'{categoria}']
        while self.target_url:
            response = requests.get(self.target_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.find_all(class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
            threads = []
            if completo:
                for element in elements:
                    t = threading.Thread(target=self.descarga_completa, args=(element,soup,output_format))
                    t.start()
                    threads.append(t)
            else:
                for element in elements:
                    t = threading.Thread(target=self.descarga_simple, args=(element,soup,output_format))
                    t.start()
                    threads.append(t)
            # Wait for all threads to finish
            for t in threads:
                t.join()
            next_page = soup.find(class_='next')
            if next_page:
                self.target_url = '/'.join(self.target_url.split('/')[:-1]) + '/' + next_page.find('a').get('href')
            else:
                self.target_url = None



    def rating_to_number(self, rating):
        """Converts a rating string to a number. If the string is not a valid rating, returns 0."""
        if rating == 'One':
            return 1
        elif rating == 'Two':
            return 2
        elif rating == 'Three':
            return 3
        elif rating == 'Four':
            return 4
        elif rating == 'Five':
            return 5
        else:
            return 0
        
    def descargar_ficha_libro(self, libro, output_format):
        """Downloads a book's details to a file in the specified format. If the file already exists, it is overwritten."""
        # Determine the output path
        output_path = fr'{self.output_dir}/{libro.nombre}.{output_format}'
        print(f'Downloading book details to {output_path}')
        if output_format == 'json':
            with open(f'{output_path}','w') as f:
                json.dump(libro.__dict__, f, indent=4)
        elif output_format == 'csv':
            with open(f'{output_path}','w') as f:
                writer = csv.writer(f)
                writer.writerow(['nombre', 'ruta_ficha', 'precio', 'rating', 'id', 'categoria', 'imagen'])
                writer.writerow(libro.to_list())
        elif output_format == 'html':
            with open(f'{output_path}','w') as f:
                libro_df = pd.DataFrame([libro.__dict__])
                f.write(libro_df.to_html())
        else:
            raise ValueError(f'Invalid output format: {output_format}')
