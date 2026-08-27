# Design System: Confetti Drop

## 1. Creative North Star
**"Confetti Drop"** — Esto no es editorial artisan. Es una tienda de una niña de 10 años. Debe verse como una fiesta de cumpleaños bien organizada: explosión de color controlada, alegre, llena de energía, pero legible.

Rechaza el minimalismo cremoso. Abraza la intensidad cromática. Cada sección debe sentirse como abrir una caja de sorpresas.

---

## 2. Paleta — Extraída del Logo Real

| Token       | Hex       | Uso                                               |
|-------------|-----------|---------------------------------------------------|
| `--pink`    | `#E8317A` | Primario · botones principales · bordes de cards  |
| `--yellow`  | `#F5C842` | Highlights · badges · detalles decorativos         |
| `--green`   | `#6DBF67` | Acentos positivos · badge "Personalizable"         |
| `--purple`  | `#9B6DB5` | Headers secundarios · decoración · pasos           |
| `--orange`  | `#F47C3C` | Hover states · CTA secundario                     |
| `--sky`     | `#AEE0F5` | Fondos de sección alternados                      |
| `--bg`      | `#FFFDF8` | Fondo base (casi blanco, no crema)                |
| `--text`    | `#2B1704` | Texto principal                                   |

### Rotación de fondos de sección
1. `#FFFDF8` — blanco base
2. `#AEE0F5` — celeste
3. `#FFE4F0` — rosa claro
4. `#FFF8DC` — amarillo claro
5. Repite

---

## 3. Tipografía
- **Headlines:** Fredoka · tamaños grandes y festivos · H1 mínimo 3rem mobile, 5rem desktop
- **Body/UI:** Nunito · weights 400–700 · alta legibilidad
- **Regla:** Todo lo que sea precio, nombre de producto, o CTA va en Fredoka o Nunito Bold.

---

## 4. Componentes

### Header sticky
- Fondo: `#FFFDF8`
- `border-bottom: 3px solid #E8317A`
- Logo en Fredoka rosa fuerte

### Product Cards
- Fondo blanco
- `border-top: 4px solid [color rotativo]`
- Sombra tintada del color del borde (no gris)
- Colores de borde rotan: pink → yellow → green → purple → repite
- Hover: `translateY(-8px)` suave

### Botón primario
- Background: `#E8317A`
- Text: blanco
- `border-radius: 999px` (pill)
- Hover: `#F47C3C`

### Botón outline
- Border: color correspondiente
- Hover: rellena con ese color

### Badges de producto
- Rotan: amarillo (`#F5C842`, texto oscuro) · verde (`#6DBF67`, texto blanco) · violeta (`#9B6DB5`, texto blanco)
- Siempre `border-radius: 999px`

### Benefits Pills
- Cada uno en un color distinto de la paleta
- Fondo del color, texto blanco (excepto amarillo → texto oscuro)

### CTA Final
- `background: linear-gradient(135deg, #E8317A 0%, #9B6DB5 100%)`
- NO coral apagado

### Hero Decorations
- SVG confetti posicionado absolute: estrellas, círculos, rectángulos rotados
- Colores: yellow, green, purple, pink, sky
- Animaciones: float suave (translateY loop)

---

## 5. Secciones
1. Nav
2. Hero (blanco)
3. Benefits Pills (celeste)
4. Product Catalog — grid con JS carrito (blanco)
5. Cómo comprar (rosa claro)
6. Conoce a Ariana (amarillo claro)
7. Galería clientes (celeste)
8. FAQ (blanco)
9. Final CTA (gradiente)
10. Footer (oscuro `#2B1704`)

---

## 6. JS — Carrito WhatsApp
- Productos como array JS con `id, name, price, img, badge, badgeColor`
- Cards renderizadas dinámicamente desde el array
- Carrito como objeto `{ [id]: qty }`
- Panel lateral con qty +/- y total
- `sendWhatsApp()` construye mensaje con líneas del pedido y total
- Toast de confirmación al agregar
