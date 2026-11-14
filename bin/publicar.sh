#!/usr/bin/env bash
# Publica la tienda en UN paso: genera el catálogo, guarda en git, sube y despliega.
# Se detiene si algo falla (X7 de la revisión de Fable). Además, el commit mantiene
# vivo el repo, que es lo que evita que GitHub apague la consulta diaria a los 60 días.
set -euo pipefail
cd "$(dirname "$0")/.."
SITE=388bab81-2d90-4c5a-81e5-f78e3e9dda10

python3 bin/generar-productos.py
git add bin/generar-productos.py bin/publicar.sh public/index.html public/productos.js public/Imagenes/catalogo datos 2>/dev/null || true
if ! git diff --cached --quiet; then
  git commit -q -m "chore(catalogo): publicar $(date +%F) [sin-novedad]"
fi
git push -q origin main
netlify deploy --dir public --prod --site "$SITE" | grep -i 'unique deploy' || true
code=$(curl -s -o /dev/null -w '%{http_code}' https://elshopdeariana.com/)
[ "$code" = "200" ] || { echo "ERROR: la tienda responde $code"; exit 1; }
echo "Publicado. La tienda responde 200."
