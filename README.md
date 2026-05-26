# Cita del día para Giovanna

Web app y PWA que muestra cada día una cita literaria o filosófica curada (~180 fragmentos del s. XIII al XXI).

## Uso

Abre [index.html](index.html) en cualquier navegador moderno. La cita del día es determinista por fecha; el botón **Otra cita** muestra una al azar.

Como PWA, se puede instalar en móvil (Safari/Chrome → "Añadir a pantalla de inicio") y funciona offline después de la primera visita.

## Estructura

- [`index.html`](index.html) — app completa (HTML, CSS y JS en línea, incluida la base de citas)
- [`manifest.webmanifest`](manifest.webmanifest) — metadatos PWA
- [`sw.js`](sw.js) — service worker (cache-first)
- `icon-*.png` — íconos PWA

## Desarrollo

- [`serve.py`](serve.py) — servidor local en `:4178` para probar la PWA (las PWAs no funcionan sobre `file://`).
- [`make_icons.py`](make_icons.py) — regenera los íconos PNG con la paleta del proyecto.

Tras cambios en `index.html`/`sw.js`, incrementar la versión de cache en `sw.js` (`cita-diaria-vN`) para que los navegadores instalados reciban la actualización.
