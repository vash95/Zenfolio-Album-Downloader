# Zenfolio Album Downloader - Modified Version

Script en Python para descargar imágenes de álbumes de Zenfolio.

Este proyecto está basado en el repositorio original de Nicholas Dawson:

https://github.com/NicholasDawson/Zenfolio-Album-Downloader

## Créditos

La idea y versión inicial del script pertenecen a Nicholas Dawson.  
Esta versión ha sido modificada para funcionar mejor con álbumes de Zenfolio que cargan imágenes dinámicamente mediante scroll.

## Cambios realizados

- Sustituido el parser `lxml` por `html.parser`.
- Añadido soporte con Selenium.
- Añadido scroll automático para cargar más miniaturas.
- Añadido control de errores.
- Añadido timeout en las peticiones.
- Evita que el programa se pare si una foto falla.

## Instalación

```bash
pip install requests beautifulsoup4 selenium
