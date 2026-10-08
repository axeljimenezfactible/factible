# Fábrica de micro-apps (Fase 2)

Esqueleto ejecutable de la arquitectura modular. Solo biblioteca estándar de Python 3; sin dependencias. **Todavía no construye apps**: define el formato de especificación y valida que cada micro-app cumpla las reglas de la fábrica.

| Archivo | Para qué |
|---|---|
| `catalog.json` | Catálogo de módulos reutilizables. Todos están en estado `planned`; los campos de licencia se rellenan con la investigación de la Fase 2 |
| `specs/` | Una especificación por micro-app candidata (los 4 de confianza media de la pasada 3 y 2 de confianza baja) |
| `spec.py` | Validador de especificaciones e informe de uso de módulos |
| `tests/` | Pruebas unitarias; sus datos son fixtures sintéticos |

```bash
python3 -I -m unittest discover -s tests            # pruebas
python3 spec.py validate specs/*.json                 # valida las especificaciones
python3 spec.py report specs/*.json                   # qué módulos construir primero
```

## Reglas que aplica el validador
- Los módulos del **núcleo** (`core.*`) son implícitos: la especificación no los lista.
- Todo módulo debe existir en el catálogo y cubrir las plataformas de la app.
- La app debe procesar **todo en local**; las únicas llamadas de red permitidas son `license`, `update` y `telemetry_optin`.
- Si usa un módulo de resultado parcial (OCR, detección de nombres, transcripción, modelo de lenguaje), debe marcar `review_required` e incluir `review.ui`: revisión humana antes de guardar.
- Mínimo 3 pruebas de oro, 3 pasos de flujo, un riesgo y una prueba de puerta falsa con precios.
- Precio entre $0 y $200.

## Qué no dice esto
El informe de uso depende de las 6 especificaciones de ejemplo, que escogí yo. Orienta el orden de construcción, pero no es un resultado de mercado.
