# SCPider BDA
## 3. Instalación y Configuración
Para garantizar un entorno de ejecución controlado y reproducible, se recomienda el uso de entornos virtuales.

### 3.1. Requisitos Previos
*   Python 3.x instalado.
*   Un entorno virtual con scrapy. `pip install scrapy`

### 3.2. Uso y Ejecución
El script principal permite configurar los parámetros de entrada para la tarea 
de extracción en el propio script en forma de lista de diccionarios:

```python
        [{
            "allowed_domains": ["www.eldiario.es", "eldiario.es"],
            "start_urls": ["https://www.eldiario.es/"],
            "output_file": "eldiario.csv",
            "noticias_link": "h2>a::attr(href)",
            "fields": {
                "title": "h1.title::text",
                "description": "ul.footer h2::text",
                "autor": "p.authors>a::text",
                "date": "div.date>span.day::text",
                "hour": "div.date>span.hour::text"
            }
        },
        {
            "allowed_domains": ["elpais.com", "www.elpais.com", "cincodisas.es"],
            "start_urls": ["https://elpais.com/"],
            "output_file": "elpais.csv",
            "noticias_link": "article *.c_t>a::attr(href)",
            "fields": {
                "title": "h1.a_t::text",
                "description": "p.a_st::text",
                "autor": "div[data-dtm-region=articulo_firma] > a::text",
                "date": "a[data-date]::attr(data-date)"
            }
        }]
```

El script se ejecuta como cualquier otro script python
```bash
python3 noticiasspider.py
```

