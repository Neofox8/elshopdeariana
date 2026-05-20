# 🎬 Pipeline IA — Canal TikTok El Shop de Ariana
> **Versión:** 1.2 | **Actualizado:** Mayo 2026  
> **Stack confirmado:** Claude → GPT Image 2 (Thinking) → Google Flow / Veo 3.1 → CapCut → TikTok + Instagram Reels + YouTube Shorts

---

## 🧠 Principio del sistema

**Claude = Cerebro / Hub central**  
Todo video nace aquí. Claude genera el concepto, el script, el brief de imágenes, el brief de video y el caption para TikTok. Las otras herramientas ejecutan lo que Claude define.

```
Claude (concepto + script + briefs)
    ↓
GPT Image 2 Thinking (escenas producto + cover)
    ↓
Google Flow — Veo 3.1 Fast (animar imágenes → video clips 9:16)
    ↓
CapCut (ensamblar clips, captions, música, export)
    ↓
TikTok (principal) → Instagram Reels → YouTube Shorts (mismo archivo 9:16)
```

---

## 📋 PASO 1 — Concepto & Brief (Claude)

### Prompt maestro — pégalo en este chat cada vez:

```
Proyecto: El Shop de Ariana — canal TikTok/Reels
Formato objetivo: vertical 9:16, duración 30–45 segundos
Producto de este video: [NOMBRE DEL PRODUCTO]
Ángulo creativo sugerido: [idea tuya o "sugiéreme tú"]

Genera:
1. CONCEPTO: título del video + gancho (hook) de los primeros 3 segundos
2. SCRIPT: narración off o texto en pantalla, escena por escena (máx 6 escenas)
3. BRIEF DE IMÁGENES: prompt exacto para GPT Image 2 por cada escena
4. BRIEF DE VIDEO: prompt para Veo 3.1 por cada imagen (qué movimiento, cámara, duración)
5. CAPTION TIKTOK: texto del post + 10 hashtags en español orientados a Perú

Tono de marca: colorido, juguetón, cálido, peruano — como el logo (niña feliz, letras vibrantes)
Paleta: rosa #E8317A, amarillo #F5C842, verde #6DBF67, violeta #9B6DB5, naranja #F47C3C
```

---

## 🖼️ PASO 2 — Generación de imágenes (GPT Image 2 — Thinking Mode)

### Cómo activar Thinking Mode:
- Abre ChatGPT → selecciona modelo **o4** o **GPT-5.5 Thinking**
- La imagen se planifica antes de renderizar → mucho mejor resultado para producto

### Capacidades clave para El Shop:
| Feature | Uso en El Shop |
|---|---|
| Image-to-image | Sube foto real del producto → genera escena lifestyle |
| 8 imágenes coherentes por prompt | Genera toda la secuencia de un video de una sola vez |
| Texto dentro de la imagen | Cover TikTok con precios, nombres, emojis legibles |
| 4K resolution | Export limpio y nítido en móvil |
| Character/object consistency | El mismo producto se ve igual en todas las escenas |

### Prompt base para escenas de producto:
```
[Pega el brief que generó Claude para esta escena]

Estilo visual: colorido, luminoso, alegre. Paleta: rosa vibrante, amarillo, verde menta, violeta suave.
Fondo: [habitación peruana acogedora / escritorio ordenado / mesa con flores / etc.]
Iluminación: natural, cálida, tipo lifestyle foto de producto.
El producto debe verse claramente: [nombre y color del producto].
Sin texto en la imagen (el texto va en CapCut), salvo que el brief diga lo contrario.
Aspecto: 9:16 vertical para TikTok/Reels.
```

### Para cover de TikTok (con texto):
```
Cover para TikTok de [producto].
Texto en la imagen: "[TÍTULO]" en letras grandes y legibles, estilo pop colorido.
Fondo: gradiente vibrante en tonos rosa-violeta o amarillo-naranja.
El producto ocupa el 60% de la imagen, centrado.
Tipografía: gruesa, redondeada, estilo Fredoka o similar.
Resolución: 1080x1920 (9:16).
```

---

## 🎬 PASO 3 — Video IA (Google Flow — Veo 3.1)

### Acceso:
- **flow.google.com** → requiere plan Google One Plus o superior
- Christian tiene plan Plus con acceso a Veo 3.1 ✅

### Configuración confirmada:
| Parámetro | Valor |
|---|---|
| Tipo | Video → Fotogramas (Image-to-Video) |
| Ratio | 9:16 (vertical TikTok) |
| Modelo | Veo 3.1 Fast |
| Outputs | x2 (genera dos variantes, elige la mejor) |
| Créditos por generación | ~40 créditos |

### Workflow por escena:
1. Abre Google Flow → proyecto del video
2. Arrastra la imagen de la escena al canvas
3. Selector de modelo → **Video → Fotogramas → 9:16 → Veo 3.1 Fast → x2**
4. Pega el prompt de movimiento de esa escena
5. Genera → elige la mejor variante → descarga
6. Repite para las 6 escenas

### Prompt base para animación:
```
[Pega el brief de video que generó Claude para esta escena]

Movimiento de cámara: [slow zoom in / parallax suave / travelling lateral]
Estilo: cinematográfico, luminoso, limpio. Sin movimientos bruscos.
El producto no debe distorsionarse ni perder forma.
```

### Tipos de movimiento por escena:
| Escena | Movimiento recomendado |
|---|---|
| Producto solo en mesa | Slow zoom in + luz que baila suave |
| Producto en habitación | Parallax 3D — profundidad de campo |
| Manos usando el producto | Travelling lateral de derecha a izquierda |
| Antes/Después | Corte directo, no animación |
| Producto con precio/texto | Cámara estática, texto animado en CapCut |

---

## ✂️ PASO 4 — Edición (CapCut — gratuito)

### Checklist por video:
- [ ] Importar los 6 clips descargados de Google Flow
- [ ] Ordenar según el script de Claude
- [ ] Agregar subtítulos automáticos (Auto Caption → español peruano)
- [ ] Música: buscar "upbeat latin pop" en librería gratuita de CapCut
- [ ] Overlay de precio/nombre del producto (font redondeada, color rosa #E8317A)
- [ ] Hook visual en los primeros 1–2 segundos (texto grande: la pregunta o promesa)
- [ ] CTA final: "Escríbenos por WhatsApp 💬" + número en pantalla
- [ ] Export: 1080x1920 (9:16), 30fps, MP4

### Plantilla de estructura (30–45 seg):
```
[0–3 seg]   HOOK — pregunta o afirmación que para el scroll
[3–8 seg]   Mostrar el problema o el deseo
[8–20 seg]  Mostrar el producto en acción / en escena
[20–30 seg] Detalle del producto + precio
[30–40 seg] CTA — "Escríbenos por WhatsApp"
[40–45 seg] Logo + nombre de tienda
```

---

## 📤 PASO 5 — Publicación

### Destinos (mismo archivo, orden de prioridad):
| Plataforma | Rol | Formato | Duración ideal | Frecuencia meta |
|---|---|---|---|---|
| **TikTok** | **Principal** | 9:16 | 30–45 seg | 3–5x semana |
| Instagram Reels | Secundario | 9:16 | 30–45 seg | 3x semana |
| YouTube Shorts | Terciario | 9:16, < 60 seg | 30–45 seg | 3x semana |

### Checklist de publicación:
- [ ] Cover custom (generado en GPT Image 2, 1080x1920)
- [ ] Caption: el que generó Claude en el Paso 1
- [ ] Hashtags: los que generó Claude (mezcla ES + producto + Perú)
- [ ] Sonido TikTok: usar trending sound si aplica, o música original de CapCut
- [ ] Programar publicación: 7pm–9pm hora Lima (pico de audiencia local)
- [ ] Publicar en TikTok primero → luego subir mismo archivo a Reels y Shorts

---

## 🗂️ IDEAS DE VIDEOS — Backlog

### Categoría: Producto
- "¿Tu Stanley… pero en miniatura?" → Llavero Stanley lip balm ✅ (primer video)
- "3 formas de organizar tu escritorio con esto" → Organizador Lego
- "El regalo que TODOS quieren" → Bandejas de Colores
- "Antes vs después de tener uno en casa" → Pequeño Closet
- "Cómo lo personalizo con tu nombre" → proceso de pintura

### Categoría: Educativo / Behind the scenes
- "Así nace un producto en El Shop de Ariana"
- "¿De qué está hecho? MDF pintado a mano"
- "Colores disponibles este mes"

### Categoría: Social proof / Fechas especiales
- "Idea de regalo Día de la Madre bajo S/50"
- "Lo que compran más nuestros clientes"
- "Unboxing sorpresa de un pedido personalizado"

---

## ⚙️ ESTÁNDARES DE MARCA

| Elemento | Especificación |
|---|---|
| Paleta principal | Rosa #E8317A, Amarillo #F5C842, Verde #6DBF67 |
| Paleta secundaria | Violeta #9B6DB5, Naranja #F47C3C, Celeste #AEE0F5 |
| Fondo neutro | #FFFDF8 (crema cálido) |
| Tipografía en video | Fredoka (headings) / Nunito (body) — disponibles en CapCut |
| Tono de voz | Cercano, alegre, peruano. Nada formal. Emojis permitidos. |
| CTA siempre | WhatsApp → wa.me/51967771823 |
| Handle TikTok | @elshopdeariana (por confirmar) |
| Handle IG | @elshopdeariana |
| Dominio | elshopdeariana.com |

---

## 🚀 Flujo por video (validado en producción)

```
1. Claude → Prompt Maestro → concepto + script + 6 briefs imagen + 6 briefs video + caption
2. ChatGPT Plus Thinking → genera 6 imágenes lifestyle del producto
3. Google Flow → Veo 3.1 Fast → 9:16 → x2 por escena → elige mejor → descarga
4. CapCut → ensambla 6 clips → captions → música → texto overlay → CTA → export MP4
5. TikTok → Instagram Reels → YouTube Shorts (mismo archivo)

Tiempo estimado: 60–90 minutos por video
```

---

*Documento vivo — actualizar cuando cambie el stack o se agregue nueva herramienta.*
