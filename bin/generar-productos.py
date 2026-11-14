#!/usr/bin/env python3
"""Regenera public/productos.js desde la base de la calculadora.

Por qué existe: la tienda NO debe depender de la base en vivo. El proyecto Supabase
es gratuito y se pausa solo tras una semana sin uso — eso dejó elshopdeariana.com
mostrando "No hay productos disponibles" desde ~mayo hasta el 2026-08-28, sin que
nadie se enterara. Con el catálogo escrito en un archivo del repo, la tienda sigue
en pie aunque la base esté dormida.

La base sigue siendo la FUENTE (ahí publica la calculadora); productos.js es una
copia generada. Se corre cuando Ariana publica o despublica algo:

    python3 bin/generar-productos.py           # regenera productos.js + baja fotos
    python3 bin/generar-productos.py --check    # solo avisa si quedó desactualizado

Sale con código != 0 si no pudo leer la base o si --check encuentra diferencias:
un "no pude medir" nunca se reporta como OK.
"""
import json
import os
import sys
import urllib.request

SUPABASE_URL = "https://oanyupbncimhrljlnhck.supabase.co"

# La clave de abajo YA es pública: estuvo en public/index.html —repo público y sitio
# servido— desde 2026-05-19, así que dejarla acá no expone nada nuevo. Pero la tabla
# tiene RLS `allow_all`, o sea que con esa clave cualquiera puede ESCRIBIR el catálogo
# y los pedidos. Cuando se rote en el panel, la nueva se pasa por variable de entorno
# y NO vuelve a entrar al repo:
#     export ELSHOP_SUPABASE_ANON_KEY='...'
ANON_KEY = os.environ.get("ELSHOP_SUPABASE_ANON_KEY") or (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9hbnl1cGJuY2ltaHJsamxuaGNrIiwicm9sZSI6ImFub24i"
    "LCJpYXQiOjE3Nzg2MjE3MzksImV4cCI6MjA5NDE5NzczOX0."
    "wF2Qa-6B3NONKvXyVlQ9a2dMZZCWeviO6Xid3OrSAZU"
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JS = os.path.join(ROOT, "public", "productos.js")
IMG_DIR = os.path.join(ROOT, "public", "Imagenes", "catalogo")
IMG_REL = "./Imagenes/catalogo"
BACKUP_DIR = os.path.join(ROOT, "datos")


def fetch(table, query=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?select=*{query}"
    req = urllib.request.Request(
        url, headers={"apikey": ANON_KEY, "Authorization": f"Bearer {ANON_KEY}"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        if r.status != 200:
            raise RuntimeError(f"{table}: HTTP {r.status}")
        return json.load(r)


def local_path(url):
    """Ruta local que le corresponde a una foto del bucket."""
    return f"{IMG_REL}/{url.rsplit('/', 1)[-1]}"


def photo_urls(row):
    """La foto principal MÁS las de la galería. Las de galería también se bajan:
    si quedan apuntando al bucket, la tienda vuelve a depender de la base."""
    urls = []
    if row.get("imagen_url"):
        urls.append(row["imagen_url"])
    for u in row.get("imagen_urls") or []:
        if isinstance(u, str) and u.strip() and u not in urls:
            urls.append(u)
    return urls


def media_urls(row):
    """Todo lo que hay que bajar: fotos y, si lo hubiera, el video."""
    urls = list(photo_urls(row))
    if row.get("video_url") and row["video_url"] not in urls:
        urls.append(row["video_url"])
    return urls


EXT_OK = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif", ".mp4", ".webm"}


def url_permitida(url):
    """Solo baja del almacén de la propia base y solo imágenes o video.
    Sin esto, un texto escrito en la base podría hacer que se publique un
    archivo cualquiera dentro del sitio (hallazgo S3 de la revisión de Fable)."""
    from urllib.parse import urlparse
    u = urlparse(url)
    host_ok = u.scheme == "https" and u.hostname == urlparse(SUPABASE_URL).hostname
    name = u.path.rsplit("/", 1)[-1]
    ext_ok = os.path.splitext(name)[1].lower() in EXT_OK
    name_ok = bool(name) and name == os.path.basename(name) and ".." not in name
    return host_ok and ext_ok and name_ok


def download_photos(rows):
    """Baja cada foto del bucket al repo. Sin esto la tienda pierde las imágenes
    cuando la base se pausa, aunque los nombres y precios sigan en el archivo."""
    os.makedirs(IMG_DIR, exist_ok=True)
    for row in rows:
        for url in media_urls(row):
            if not url_permitida(url):
                raise RuntimeError(f"dirección no permitida, no se baja: {url[:120]}")
            name = url.rsplit("/", 1)[-1]
            dest = os.path.join(IMG_DIR, name)
            if not os.path.exists(dest) or os.path.getsize(dest) < 1000:
                urllib.request.urlretrieve(url, dest)
                if os.path.getsize(dest) < 1000:
                    raise RuntimeError(f"foto sospechosamente chica: {name}")
                print(f"  bajada  {name}")


def js_str(value):
    return json.dumps(value if value is not None else "", ensure_ascii=False)


def render(rows):
    sin_precio = [r.get("nombre") or r.get("id") for r in rows
                  if not isinstance(r.get("shop_price"), (int, float)) or r["shop_price"] <= 0]
    if sin_precio:
        raise RuntimeError("producto publicado sin precio, no se genera: " + ", ".join(map(str, sin_precio)))
    lines = [
        "/* ══════════════════════════════════════════════════════════════════════",
        "   ARCHIVO GENERADO — no editar a mano.",
        "",
        "   Sale de la base de la calculadora 3D (tabla catalog_items, lo que está",
        "   marcado como 'Publicar en Shop'). Para cambiar el catálogo se publica o",
        "   se despublica desde la calculadora y después se corre, en este repo:",
        "",
        "       python3 bin/generar-productos.py",
        "",
        "   La tienda lee ESTE archivo y no la base: así sigue en pie aunque el",
        "   proyecto Supabase gratuito esté pausado por falta de uso.",
        "   ══════════════════════════════════════════════════════════════════════ */",
        "",
        "window.PRODUCTOS = [",
    ]
    for row in rows:
        fotos = [local_path(u) for u in photo_urls(row)]
        lines.append("  {")
        lines.append(f"    id: {js_str(row['id'])},")
        lines.append(f"    nombre: {js_str(row['nombre'])},")
        lines.append(f"    precio: {json.dumps(row.get('shop_price'))},")
        lines.append(f"    imagen: {js_str(fotos[0] if fotos else '')},")
        if row.get("descripcion"):
            lines.append(f"    descripcion: {js_str(row['descripcion'])},")
        if len(fotos) > 1:
            lines.append(f"    imagenes: {json.dumps(fotos[1:], ensure_ascii=False)},")
        if row.get("video_url"):
            lines.append(f"    video: {js_str(local_path(row['video_url']))},")
        lines.append("  },")
    lines.append("];")
    lines.append("")
    return "\n".join(lines)


def main():
    check_only = "--check" in sys.argv
    try:
        # Mismo filtro y mismo orden que usaba la tienda cuando leía en vivo.
        rows = fetch("catalog_items", "&shop_published=eq.true&order=fecha.desc")
    except Exception as exc:  # noqa: BLE001 — "no pude medir" no es "está OK"
        print(f"ERROR: no se pudo leer la base ({exc}).", file=sys.stderr)
        print("Si el proyecto Supabase está pausado, reactivarlo en el panel.", file=sys.stderr)
        return 2

    if not rows:
        print("ERROR: la base respondió pero no hay ningún producto publicado.", file=sys.stderr)
        print("No se pisa productos.js con una lista vacía.", file=sys.stderr)
        return 2

    if check_only:
        actual = open(OUT_JS, encoding="utf-8").read() if os.path.exists(OUT_JS) else ""
        if render(rows) != actual:
            print(f"productos.js está desactualizado ({len(rows)} publicados en la base).")
            return 1
        print(f"productos.js al día ({len(rows)} productos).")
        return 0

    download_photos(rows)
    with open(OUT_JS, "w", encoding="utf-8") as fh:
        fh.write(render(rows))
    print(f"productos.js escrito con {len(rows)} productos.")

    # Respaldo de las 3 tablas: que perder la base no vuelva a ser perder la data.
    os.makedirs(BACKUP_DIR, exist_ok=True)
    for table in ("catalog_items", "orders", "order_items"):
        data = fetch(table)
        with open(os.path.join(BACKUP_DIR, f"{table}.json"), "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=1)
        print(f"respaldo {table}: {len(data)} filas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
