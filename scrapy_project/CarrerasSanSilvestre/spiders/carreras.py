import scrapy
from CarrerasSanSilvestre.items import CarrerassansilvestreItem

class CarrerasSpider(scrapy.Spider):
    name = "carrera"
    allowed_domains = ["sansilvestrecoruna.com"]
    
    # Debido a que en algunas páginas de resultados de la San Silvestre no viene indicado el año lo mapeo de forma manual:
    ediciones = {
        2010: "https://sansilvestrecoruna.com/es/web/resultado/competicion--435",
        2011: "https://sansilvestrecoruna.com/es/web/resultado/competicion--603",
        2012: "https://sansilvestrecoruna.com/es/web/resultado/competicion--836",
        # 2013 lo saltamos ya que no hay datos de la edición de este año
        2014: "https://sansilvestrecoruna.com/es/web/resultado/competicion-899",
        2015: "https://sansilvestrecoruna.com/es/web/resultado/competicion-5000",
        2016: "https://sansilvestrecoruna.com/es/web/resultado/competicion-6273",
        2017: "https://sansilvestrecoruna.com/es/web/resultado/competicion-7799",
        2018: "https://sansilvestrecoruna.com/es/web/resultado/competicion-9310",
        2019: "https://sansilvestrecoruna.com/es/web/resultado/competicion-10910",
        # 2020 saltado por COVID
        2021: "https://sansilvestrecoruna.com/es/web/resultado/competicion-11984",
        2022: "https://sansilvestrecoruna.com/es/web/resultado/competicion-13121",
        2023: "https://sansilvestrecoruna.com/es/web/resultado/competicion-14359",
        2024: "https://sansilvestrecoruna.com/es/web/resultado/competicion-15442",
        2025: "https://sansilvestrecoruna.com/es/web/resultado/competicion-16683",
    }

    # Esta función sustituye a start_urls
    def start_requests(self):
        for anio, url in self.ediciones.items():
            # Enviamos la petición y pasamos el año en "meta"
            yield scrapy.Request(url, callback=self.parse, meta={'anio_carrera': anio})

    def parse(self, response):
        # RECUPERAMOS EL AÑO de la etiqueta "meta"
        anio = response.meta['anio_carrera']
        
        # Selectores (Ajusta esto según lo que veas al inspeccionar elementos)
        filas = response.css('table tbody tr')

        for fila in filas:
            item = CarrerassansilvestreItem()
            
            # Datos fijos y calculados
            item['location'] = "A Coruña"
            item['date'] = f"31-12-{anio}"
            item['edicion'] = anio
            item['distancia'] = "7.5 km"

            # Hay 8 columnas en total en las páginas de la San Silvestre:
            # Col 1: Vacía (Invisible)
            # Col 2: Puesto
            # Col 3: Dorsal
            # Col 4: Nombre
            # Col 5: Apellidos
            # Col 6: P. Sexo
            # Col 7: P. Categoría
            # Col 8: Tiempo

            # Extracción de datos
            item['posicion'] = fila.css('td:nth-child(2)::text').get()

            # Unir nombre y apellidos
            # Usamos " *::text" y .getall() para pillar el texto aunque esté dentro de un enlace <a> o <b>
            # .join() une los trozos si hay varios
            nombre_parts = fila.css('td:nth-child(4) *::text').getall()
            nombre_limpio = " ".join(nombre_parts).strip()
            
            apellidos_parts = fila.css('td:nth-child(5) *::text').getall()
            apellidos_limpio = " ".join(apellidos_parts).strip()
            
            # Guardamos Nombre completo formateado (Ej: "Diego Becerra")
            nombre_completo = f"{nombre_limpio} {apellidos_limpio}".strip()
            item['nombre'] = nombre_completo.title() if nombre_completo else "Anonimo"

            # Conseguir el sexo del participante (Limpieza: "M-94" -> "Hombre"):
            sexo_raw = fila.css('td:nth-child(6) ::text').get()
            # Limpiamos espacios y miramos la primera letra
            if sexo_raw:
                letra = sexo_raw.strip().upper() # Quitamos espacios y ponemos mayúsculas por si acaso
                if letra.startswith('M'):
                    item['sexo'] = "Hombre"
                elif letra.startswith('F'):
                    item['sexo'] = "Mujer"
                else:
                    item['sexo'] = "Desconocido" # Por si sale algo raro
            else:
                item['sexo'] = "Desconocido"

            # Limpiar categorías: "SNM-3" -> "SNM"
            # Usamos extracción robusta (*::text)
            cat_parts = fila.css('td:nth-child(7) *::text').getall()
            cat_raw = "".join(cat_parts).strip()

            if not cat_raw or cat_raw.isdigit():
                # Si está vacío o es solo un número
                item['categoria'] = "Categoría Desconocida"
            elif '-' in cat_raw:
                # Si tiene guion (ej: "VETERANOS-7"), intentamos separar el número final
                # rsplit('-', 1) corta desde la derecha una sola vez
                parte_texto, parte_numero = cat_raw.rsplit('-', 1)
                
                if parte_numero.isdigit():
                    # Si lo que hay tras el guion es un número, nos quedamos con el texto
                    item['categoria'] = parte_texto.strip()
                else:
                    # Si tras el guion hay letras (ej: "SUB-23"), no cortamos nada
                    item['categoria'] = cat_raw
            else:
                # Si no tiene guion ni es número, se queda como está
                item['categoria'] = cat_raw

            
            item['tiempo'] = fila.css('td:nth-child(8)::text').get()

            yield item

        # Selector de paginación
        # Usamos XPath para buscar un enlace (a) que contenga la palabra "Siguiente"
        next_page = response.xpath('//a[contains(text(), "Siguiente")]/@href').get()
        
        if next_page:
            # response.follow fusiona automáticamente la URL actual con "?page=x"
            yield response.follow(next_page, callback=self.parse, meta={'anio_carrera': anio})