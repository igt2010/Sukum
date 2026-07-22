# Sukum

Web sencilla y serena para meditación guiada. Sitio **estático** (solo HTML + CSS), sin dependencias ni pasos de compilación.

## Estructura

```
index.html      Página única con las secciones
styles.css      Estilos (paleta pastel, responsive)
audio/          Archivos .mp3 de las meditaciones
```

## Secciones

- **Inicio**: portada con bienvenida.
- **Quiénes somos**: presentación del proyecto.
- **Meditaciones**: tarjetas con reproductor de audio nativo (`<audio>`).
- **Noticias**: anuncios e información.

## Despliegue en desarrollo

Es un sitio estático, así que abrir `index.html` en el navegador ya funciona. Para que el audio y las rutas relativas se comporten como en producción, sirve la carpeta con un servidor local:

```bash
# Opción 1: Python (viene con casi cualquier sistema)
python -m http.server 8000

# Opción 2: Node (si lo tienes instalado)
npx serve .
```

Luego visita http://localhost:8000 (o el puerto que indique el comando).

Cualquier cambio en `index.html` / `styles.css` se ve al recargar la página; no hay compilación.

## Despliegue en producción

Al ser 100% estático puedes publicarlo gratis en cualquier hosting de estáticos. Opciones recomendadas:

### GitHub Pages (más directo, ya está en GitHub)

1. Sube el proyecto a GitHub (ya hecho si seguiste los pasos de instalación).
2. En el repo: **Settings → Pages**.
3. En *Source* elige **Deploy from a branch**, rama `main` y carpeta `/ (root)`.
4. Guarda. En 1-2 minutos estará en `https://<usuario>.github.io/<repo>/`.

O por línea de comandos:

```bash
gh api -X POST repos/<usuario>/<repo>/pages -f "source[branch]=main" -f "source[path]=/"
```

### Netlify / Cloudflare Pages (dominio propio y HTTPS automático)

1. Conecta el repositorio desde su panel web.
2. **Build command:** *(vacío)* · **Publish directory:** `.`
3. Deploy. Cada `git push` a `main` vuelve a desplegar automáticamente.

### Servidor propio (Nginx)

Copia los archivos a la raíz del sitio y sirve la carpeta como estática:

```nginx
server {
    listen 80;
    server_name sukum.com;
    root /var/www/sukum;   # aquí van index.html, styles.css y audio/
    index index.html;
}
```

Recuerda subir también la carpeta `audio/` con los `.mp3`.

## Añadir una meditación

1. Copia el `.mp3` dentro de `audio/`.
2. Duplica una tarjeta `<article class="card">` en `index.html` y ajusta título, texto y `src` del `<source>`.

## Añadir una noticia

Duplica un `<article class="news-item">` en `index.html` y edita fecha, título y texto.
