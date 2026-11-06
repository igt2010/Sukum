# Sukum

Web de una sola página para Sukum: marca, diario **Sukum 7**, recursos gratuitos, creadoras y newsletter. Sitio **estático** (HTML + CSS + JavaScript nativo), sin dependencias ni compilación.

## Estructura

```
index.html            Página principal (one-page)
styles.css            Sistema visual responsive
scripts/site.js       Menú móvil, enlace activo y diálogo de recursos
aviso-legal.html      Borrador de aviso legal
privacidad.html       Borrador de política de privacidad
cookies.html          Borrador de política de cookies
tests/test_site.py    Contrato automático del sitio
audio/                MP3 de meditaciones (conservados, NO enlazados)
docs/superpowers/     Especificación y plan del rediseño
```

## Secciones

Los enlaces del menú saltan a estas secciones (`id`):

| Menú | `id` | Contenido |
|---|---|---|
| Sukum | `inicio` | Portada |
| — | `filosofia` | Nuestra filosofía y tres pilares |
| El diario | `diario` | Sukum 7 y enlace a Amazon |
| Recursos gratuitos | `recursos` | Tres guías |
| Nosotras | `nosotras` | Las creadoras |
| Contacto | `contacto` | Newsletter y correo |

## Ver la web en local

```bash
python -m http.server 8000
```

Visita http://localhost:8000. Los cambios se ven al recargar.

## Pruebas

```bash
python -m unittest tests.test_site -v
node --check scripts/site.js
```

## Sustituir el contenido provisional

- **Portada**: reemplaza `.hero-visual` en `index.html` por una `<img>` optimizada.
- **Diario**: reemplaza `.journal-visual` por una fotografía real del diario abierto.
- **Creadoras**: en cada `article.creator`, sustituye la foto, el nombre («Nombre pendiente») y la biografía (hay un comentario `Sustituir este texto…`).
- **Portadas de las guías**: sustituye cada `.resource-cover` por la portada definitiva.
- Usa WebP o AVIF, indica `width` y `height` y escribe un `alt` descriptivo.

## Activar Brevo (pendiente)

Ahora mismo los formularios **no recogen ni envían datos**: el campo de correo y el botón están desactivados y los recursos abren un aviso de «próximamente».

Para activarlos:

1. Crea la cuenta de Brevo, una lista para recursos y otra para la newsletter.
2. Crea los formularios con doble confirmación y copia sus enlaces o códigos públicos.
3. Sustituye en `index.html` el formulario `data-brevo-pending` y los botones `data-resource-open`, y ajusta `scripts/site.js`.
4. **Nunca** pongas una clave API privada en el HTML ni en el JavaScript.
5. Completa y haz revisar `privacidad.html` y `cookies.html` **antes** de activar el envío.
6. El consentimiento de la newsletter debe ser independiente de descargar una guía.
7. Comprueba consentimiento, correo de confirmación, baja y entrega de cada guía.

## Antes del lanzamiento definitivo

- Las tres páginas legales son **borradores**: faltan titular, NIF/CIF, domicilio y revisión profesional.
- Confirma que `info@sukum.es` existe y funciona.
- Sustituye los marcadores de fotografía y los textos de las creadoras.
- Si no quieres que Google Fonts se cargue desde Google, aloja las tipografías en el propio sitio.

## Meditaciones guiadas

Por ahora no se muestran. Los MP3 siguen en `audio/` y `scripts/gen_test_audio.py` puede regenerarlos, pero no hay ninguna sección ni enlace que los exponga.

## Despliegue

### Desarrollo

Sirve la carpeta con `python -m http.server 8000` (o `npx serve .`).

### Producción (GitHub Pages)

La rama `main` se publica automáticamente en https://igt2010.github.io/Sukum/. Cada `git push` a `main` actualiza la web en uno o dos minutos.

Otras opciones válidas: Netlify o Cloudflare Pages (sin comando de compilación, directorio de publicación `.`) o cualquier servidor que sirva archivos estáticos.

## Referencias privadas

`diario.pdf` y `diario.pdf.pdf` están en `.gitignore` y no deben subirse nunca.
