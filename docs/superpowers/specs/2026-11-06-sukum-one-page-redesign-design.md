# Rediseño one-page de Sukum

## Objetivo

Transformar la web estática actual de Sukum en una experiencia editorial de una sola página que presente la filosofía de la marca, el diario Sukum 7, los recursos gratuitos, sus creadoras y la newsletter. La estructura y el ritmo visual tomarán como referencia `thewisewellness.com`, pero todo el contenido, los componentes y la identidad serán propios de Sukum.

## Alcance

La primera versión incluye:

- Cabecera fija con navegación por anclas y sección activa subrayada.
- Portada de marca con dos llamadas a la acción.
- Sección de filosofía con tres pilares.
- Sección extensa de Sukum 7 con enlace de compra en Amazon.
- Tres recursos gratuitos preparados para conectarse a Brevo.
- Sección de las dos creadoras con contenido provisional explícito.
- Newsletter y vía de contacto.
- Aviso legal, política de privacidad y política de cookies en páginas separadas.
- Diseño responsive, accesible y compatible con GitHub Pages.

Las meditaciones guiadas no aparecerán en esta versión. Sus MP3 permanecerán en el repositorio para una fase posterior.

## Restricciones y decisiones

- La aplicación seguirá siendo estática: HTML, CSS y JavaScript nativo.
- No habrá framework, proceso de compilación ni backend.
- GitHub Pages seguirá siendo el entorno de producción.
- No se copiarán código, imágenes, textos ni identidad de The Wise Wellness.
- No se publicarán imágenes extraídas del documento de requisitos; solo sirven como referencia.
- Las fotografías definitivas de Sukum 7 y de las creadoras se incorporarán más adelante.
- Market Pro Regular no se utilizará hasta que se aporte un archivo de fuente con licencia web. Cormorant Garamond cubrirá el tono editorial y Montserrat la interfaz y el texto funcional.
- Brevo no puede activarse hasta que exista una cuenta, listas y formularios. La web incluirá formularios y puntos de integración claramente documentados, pero no fingirá envíos.
- Los textos legales serán borradores orientativos, identificados como tales y sujetos a revisión profesional antes de activar captación de datos.

## Arquitectura de información

### Cabecera

- Logo textual `SUKUM` a la izquierda.
- Enlaces: `Sukum`, `El diario`, `Recursos gratuitos`, `Nosotras`, `Contacto`.
- La navegación será fija y translúcida.
- `IntersectionObserver` actualizará `aria-current="page"` y el subrayado según la sección visible.
- En móvil se utilizará un menú desplegable controlado por un botón real.

### 1. Sukum

La portada tendrá una composición asimétrica inspirada en fotografía editorial:

- Área visual izquierda con un marcador de fotografía claramente sustituible.
- Contenido a la derecha.
- Antetítulo de marca.
- Titular: «La vida cambia cuando empiezas a mirarla de otra manera».
- Texto: «Sukum nace para ayudarte a cultivar una mirada más positiva y agradecida, encontrar calma en medio del ruido y vivir tu día a día con más ligereza, presencia y paz.»
- Botones: `Descubre Sukum 7` y `Explora recursos gratuitos`.

### 2. Nuestra filosofía

- Fondo blanco roto o beige cálido.
- Introducción completa del documento.
- Tres pilares sin tarjetas decorativas pesadas:
  - `Una mirada más agradecida`.
  - `Más calma, menos ruido`.
  - `Amabilidad que se comparte`.
- Cada pilar tendrá una ilustración SVG lineal propia.
- Cierre: «Pequeños gestos. Una mirada diferente. Una forma más amable de vivir.»

### 3. Sukum 7 · Nuestro diario

- Composición de fotografía y texto en dos columnas.
- Marcador visual preparado para una fotografía real del diario abierto.
- Titular: «7 minutos al día para darle más espacio a lo bueno».
- Subtítulo: «Mucho más que un diario de gratitud».
- Texto editorial completo adaptado del documento.
- Botón externo a `https://www.amazon.es/dp/B0HQ4X8MDZ`, abierto en una pestaña nueva con atributos seguros.
- Cuatro bloques de beneficios:
  - `7 minutos para ti`.
  - `24 semanas para cambiar tu mirada`.
  - `Mucho más que escribir`.
  - `Herramientas para observar tu evolución`.
- Cierre y segunda llamada a Amazon.

### 4. Recursos gratuitos

- Titular: «Pequeñas guías para una vida más ligera».
- Tres tarjetas:
  - `Ritual de Luz · Mañanas`.
  - `Ritual de Luz · Noches`.
  - `Soplo de Luz · Respiración consciente`.
- Las portadas serán marcadores visuales de marca, no copias de las imágenes del DOCX.
- Cada tarjeta tendrá descripción breve y botón.
- Mientras Brevo no esté configurado, el botón abrirá un panel accesible que explica que el recurso estará disponible próximamente; no solicitará ni almacenará datos.
- La integración futura se realizará mediante formularios alojados o endpoints públicos de Brevo. Nunca se incluirá una clave API privada en el navegador.

### 5. Detrás de Sukum

- Titular: «Dos mujeres, una misma manera de ver la vida».
- Dos perfiles simétricos.
- Cada perfil tendrá marcador de fotografía, etiqueta `Creadora de Sukum` y texto provisional neutral.
- Los textos se identificarán en el HTML con comentarios de sustitución y en el README con instrucciones exactas.

### 6. Sigamos conectadas

- Titular: «Un poquito de Sukum, también en tu bandeja de entrada».
- Subtexto del documento.
- Formulario visual de correo con consentimiento de privacidad.
- Hasta configurar Brevo, el formulario mostrará un estado informativo y no enviará datos.
- Contacto visible mediante `info@sukum.es`, marcado en documentación como dirección que debe existir antes de publicación definitiva.

### Pie y páginas legales

- Enlaces a `aviso-legal.html`, `privacidad.html` y `cookies.html`.
- Enlace de contacto y copyright.
- Los tres documentos se presentarán como borradores orientativos.
- La política de cookies indicará que la versión inicial no instala analítica ni publicidad. Si se añade seguimiento, se requerirá revisar la política e implementar consentimiento antes de cargarlo.

## Identidad visual

### Paleta

- Verde Sukum: `#5F938D`.
- Verde oscuro: `#315E58`.
- Beige cálido: `#EAE1D2`.
- Blanco roto: `#F8F5EF`.
- Dorado suave: `#B79A62`.
- Marrón tinta: `#4A3D36`.

### Tipografía

- Cormorant Garamond para titulares y citas.
- Montserrat para navegación, etiquetas, botones y cuerpo.
- Cormorant Garamond en cursiva para detalles de tono manual.

### Composición

- Mucho espacio negativo.
- Alternancia de bloques fotográficos y editoriales.
- Bordes suaves solo donde ayuden a jerarquizar.
- Botones redondeados con contraste suficiente.
- Ilustraciones lineales y motivos orgánicos propios.
- Movimiento mínimo: aparición suave y navegación fluida, desactivados con `prefers-reduced-motion`.

## Comportamiento y estados

- JavaScript progresivo: la navegación y el contenido serán utilizables si falla.
- El menú móvil controlará `aria-expanded` y se cerrará al seleccionar un enlace.
- Los paneles de recursos se abrirán y cerrarán con teclado, devolverán el foco al disparador y responderán a `Escape`.
- Los formularios pendientes nunca mostrarán un éxito falso.
- Los enlaces externos tendrán indicación semántica y atributos `target="_blank"` y `rel="noopener noreferrer"`.
- Las imágenes futuras utilizarán dimensiones reservadas para evitar saltos de diseño.

## Estructura de archivos

- `index.html`: estructura y contenido de la página principal.
- `styles.css`: sistema visual responsive compartido.
- `scripts/site.js`: navegación activa, menú móvil y paneles de recursos.
- `aviso-legal.html`: borrador de aviso legal.
- `privacidad.html`: borrador de política de privacidad.
- `cookies.html`: borrador de política de cookies.
- `README.md`: edición de contenido, sustitución de fotografías, activación de Brevo y despliegue.
- `audio/`: se conserva sin exponerse desde la navegación.

## Accesibilidad y SEO

- Un único `h1` y jerarquía de encabezados coherente.
- Enlace para saltar al contenido.
- Contraste mínimo WCAG AA.
- Foco visible y orden de tabulación natural.
- Iconos decorativos ocultos a tecnologías de asistencia.
- Metadatos Open Graph básicos y descripción orientada a Sukum 7.
- Datos estructurados `Organization` y `Product` sin inventar precio, reseñas o disponibilidad.

## Verificación

- Validar que todos los enlaces internos llegan a su sección.
- Verificar el estado activo de la navegación durante el desplazamiento.
- Probar menú y paneles con ratón y teclado.
- Comprobar 320 px, 768 px, 1024 px y escritorio ancho.
- Confirmar que no existen errores de JavaScript.
- Confirmar que Amazon abre la URL correcta.
- Confirmar que ningún formulario envía datos antes de integrar Brevo.
- Confirmar que los MP3 y el DOCX no se enlazan desde la página.
- Servir localmente con `python -m http.server 8000` y comprobar respuesta HTTP 200.
