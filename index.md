# El Shop de Ariana — Estado del proyecto

Última actualización: 2026-05-19

Sitio público: https://elshopdeariana.com
Repo: https://github.com/Neofox8/elshopdeariana (main)
Netlify site: `stirring-hotteok-88d5d5` (custom domain `elshopdeariana.com`)

---

## Stack técnico actual

- HTML single-file (`index.html`, ~600 líneas).
- Tailwind CDN (`https://cdn.tailwindcss.com`) — sin build step.
- Google Fonts: Fredoka (headings) + Nunito (body) + Material Symbols Outlined.
- **Supabase JS v2 vía CDN** (`@supabase/supabase-js@2`) — agregado el 2026-05-19.
- Tipografía y paleta de marca: `#E8317A` (rosa), `#F47C3C` (naranja), `#F5C842` (amarillo), `#6DBF67` (verde), `#9B6DB5` (púrpura), fondo `#FFFDF8`, texto `#2B1704`.
- Sin frameworks JS, sin bundler, sin CI. Deploy manual con Netlify CLI.

Carpetas relevantes en el repo:
- `index.html` — el sitio.
- `Imagenes/` — fotos legacy del catálogo hardcodeado (anteriores al switch a Supabase). Hoy solo se usan como fallback histórico; las imágenes nuevas viven en el bucket `piezas-3d` de Supabase (subidas desde la calculadora).
- `new products/` — fotos pendientes de catalogar / reemplazar.
- `Videos de Tiktok/` + `PIPELINE_ElShopDeAriana_TikTok.md` — flujo de creación de contenido (no toca el sitio).
- `code.html` — legacy, marcado para borrar.

---

## Supabase

- Project ref: `oanyupbncimhrljlnhck`
- URL: `https://oanyupbncimhrljlnhck.supabase.co`
- Tablas usadas por el Shop: **`catalog_items`** (shared con `p7-calculadora-3d`).

### `catalog_items` — esquema

| Columna | Tipo | Default / Constraints | Uso en el Shop |
|---|---|---|---|
| `id` | `uuid` | `gen_random_uuid()` PK | clave del producto |
| `nombre` | `text` | NOT NULL | `name` en la card |
| `impresora` | `text` | — | no se usa en el Shop |
| `gramos` | `numeric` | — | no se usa en el Shop |
| `horas` | `numeric` | — | no se usa en el Shop |
| `costo_total` | `numeric` | — | interno (calculadora) |
| `precio_venta` | `numeric` | — | interno (calculadora) |
| `fecha` | `timestamptz` | `now()` | `ORDER BY fecha DESC` |
| `imagen_url` | `text` | — | `img` en la card (storage público bucket `piezas-3d`) |
| `shop_published` | `boolean` | NOT NULL DEFAULT false | filtro: solo se muestran los `true` |
| `shop_price` | `numeric` | — | `price` mostrado en el Shop (distinto del `precio_venta` interno) |

RLS habilitada, policy `allow_all` (`for all using (true)`) — la anon key lee y escribe. App personal.

Query que ejecuta el Shop al cargar:

```sql
SELECT id, nombre, shop_price, imagen_url
FROM catalog_items
WHERE shop_published = true
ORDER BY fecha DESC;
```

---

## Flujo de publicación de productos (calculadora → shop)

Ecosistema de dos sitios sobre la misma tabla:

1. **`p7-calculadora-3d`** (https://p7-calculadora-3d.netlify.app) — la calculadora donde se ingresan piezas, se calcula costo, se sube la foto al bucket `piezas-3d`, y se guarda el row en `catalog_items` con `shop_published = false`.
2. En el tab Catálogo, cada card muestra el botón **"Publicar en Shop 🛍️"** (rosa `#E8317A`). Al hacer click se abre un modal vanilla con:
   - Nombre del producto (solo lectura).
   - Input numérico vacío para el precio de venta del Shop (no se pre-rellena con `precio_venta`: el dueño decide el precio público).
   - Botones Publicar / Cancelar.
3. Al confirmar: `UPDATE catalog_items SET shop_published = true, shop_price = <precio> WHERE id = …` con `.select()` para detectar denegaciones RLS silenciosas.
4. La card publicada muestra badge verde **"En Shop ✓"** (`#6DBF67`) + botón **"Quitar del Shop"** (texto sutil) que hace `UPDATE shop_published = false`.
5. **El Shop** (`elshopdeariana.com`) consume la tabla al cargar (`loadProducts()`), filtrando `shop_published = true`. Lo que ves en el Shop es exactamente lo que está marcado como publicado en la calculadora.

Cualquier cambio (publicar, despublicar, ajustar `shop_price`) se refleja en el Shop al próximo reload — no hay redeploy, no hay cache.

---

## Decisiones técnicas tomadas hoy (2026-05-19)

1. **Una sola tabla compartida** (`catalog_items`) en lugar de duplicar productos en una tabla `shop_products` separada. Las columnas `shop_published` + `shop_price` viven en la misma fila que `costo_total` / `precio_venta` interno. Razón: simplicidad operativa; no hay sync entre tablas.
2. **`shop_price` es un campo aparte de `precio_venta`** y no se pre-rellena en el modal. El precio público al cliente puede diferir del precio sugerido por la calculadora. Esto evita que cualquier cambio interno de costos modifique automáticamente el precio del Shop.
3. **Badge rotativo por índice** en el Shop (`Nuevo / Personalizable / Más vendido / Edición especial`) en lugar de un campo `badge` en la DB. Razón: no vale la pena un campo dedicado todavía; los badges son decorativos y rotar por índice es suficiente.
4. **Placeholder SVG inline** (`data:image/svg+xml` con fondo `#FFE4F0` + 🛍️) cuando `imagen_url` es null o el `<img>` da 404. No depende de assets externos.
5. **UUIDs como strings en handlers inline** (`addToCart('${p.id}')`, `changeQty('${id}',-1)`). El código previo asumía IDs numéricos; con UUIDs sin quotes el JS template literal generaba código inválido. Cambiado a strings en todo el cart.
6. **`fmtPrice()` en lugar de `S/ ${p.price}.00`** en el render. Antes, precios decimales tipo `12.5` imprimían "S/ 12.5.00" (bug latente que no se manifestaba con el catálogo hardcodeado de enteros). Ahora `toFixed(2)` los formatea como "S/ 12.50".
7. **MCP de Supabase está en modo lectura** — no pude aplicar la migración (`ADD COLUMN shop_published, shop_price`) vía `apply_migration` ni `execute_sql`. El usuario debe correr el SQL manualmente en el SQL editor. `supabase/setup.sql` en `p7-calculadora-3d` ya incluye las nuevas columnas en el `CREATE TABLE` y un bloque `ALTER TABLE … ADD COLUMN IF NOT EXISTS` para tablas existentes.

---

## Pendientes confirmados para próxima sesión

1. **Aplicar la migración SQL en Supabase** — bloqueante hasta que se corra:
   ```sql
   ALTER TABLE catalog_items
     ADD COLUMN IF NOT EXISTS shop_published boolean NOT NULL DEFAULT false,
     ADD COLUMN IF NOT EXISTS shop_price numeric;
   ```
   Sin esto el filtro `eq('shop_published', true)` falla y el Shop muestra "No hay productos disponibles en este momento".
2. **Calidad de fotos de productos**. Las fotos actuales en `Imagenes/nuevos/` y `new products/` no tienen consistencia visual (fondo, iluminación, ángulo). Definir guía de producto (fondo claro neutro, plano cenital + plano lateral, resolución mínima 1080×1440) y reemplazar las que ya están publicadas en `catalog_items.imagen_url`. Decidir si las fotos se siguen tomando con celular o si vale invertir en setup mínimo (lightbox + tripod).
3. **Modal / card de detalle con galería de fotos**. Hoy cada producto tiene una sola `imagen_url`. Próximo paso:
   - Al click en la card, abrir un modal con título, precio, descripción y galería navegable (2-4 fotos por producto).
   - Requiere decidir esquema: ¿columna `imagen_urls text[]` en `catalog_items`, o tabla nueva `catalog_item_images (item_id, url, orden)`?
   - Agregar también campo `descripcion text` (hoy no existe).
   - El admin (calculadora) necesita UI para subir múltiples fotos por pieza y reordenarlas.

### Pendientes previos del proyecto (vigentes)

- localStorage cart persistence (hoy el carrito se pierde al recargar).
- Borrar `code.html` legacy.
- Dedup del `PIPELINE_ElShopDeAriana_TikTok.md` que quedó duplicado en root y en `Videos de Tiktok/`.
