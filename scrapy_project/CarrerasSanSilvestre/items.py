# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarrerassansilvestreItem(scrapy.Item):
    nombre = scrapy.Field()
    tiempo = scrapy.Field()
    sexo = scrapy.Field()
    edicion = scrapy.Field()
    categoria = scrapy.Field()
    posicion = scrapy.Field()
    distancia = scrapy.Field()
    location = scrapy.Field()
    date = scrapy.Field() 