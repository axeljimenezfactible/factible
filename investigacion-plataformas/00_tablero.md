# Tablero — Plataforma-PD

Última actualización: 2026-10-27 (cierre de tarea: verificación de herramientas web, Fase 0)

## Estado

| Fase | Avance | Estado |
|---|---|---|
| Diagnóstico (Bloque 3) | 100% | Cerrado |
| Fase 0 — Preparación | 80% | **BLOQUEADA**: lectura web no disponible |
| Fase 1 — Universo y ranking | 0% | No iniciada |
| G1 — Aprobar las 20 plataformas | 0% | Pendiente (depende de Fase 1) |
| Fase 2 — Fichas (20) | 0% | No iniciada |
| Fase 3 — Voz del cliente | 0% | No iniciada |
| Fase 4 — Benchmark y diferenciadores | 0% | No iniciada |
| G2 — Aprobar diferenciadores | 0% | Pendiente |
| Fase 5 — PRD | 0% | No iniciada |
| Fase 6 — Verificación independiente | 0% | No iniciada |

## Tarea actual

Fase 0, punto 2: confirmar búsqueda y lectura web. Resultado al 2026-10-27:

- `WebSearch`: **disponible**. Devuelve títulos y URLs, solo EE. UU.
- `WebFetch` (lectura de páginas): **no disponible**. Falla con `getaddrinfo ENOTFOUND` en los 4 dominios probados (ahrefs.com, roo.beehiiv.com, www.similarweb.com, www.etsy.com).
- Segunda prueba (2026-10-27, a petición del usuario): mismo resultado. WebFetch sigue sin leer ahrefs.com, www.etsy.com, www.similarweb.com ni www.trustpilot.com. El DNS del sistema resuelve github.com pero no ahrefs.com, www.etsy.com ni www.trustpilot.com.
- Diagnóstico: el proxy del entorno está activo y sin fallos de relevo, así que el bloqueo parece ser la política de red del entorno (lista de dominios permitidos), no los sitios.
- Regla aplicada: el prompt manda detenerse si falta lectura web y no investigar de memoria. No se usan `curl`, espejos ni cachés para sortearlo (regla 2.2.5).

## Decisiones tomadas (diagnóstico ligero)

| # | Decisión |
|---|---|
| Q1 | Aplicar los patrones P1 a P5 (opción a). |
| L1 | Criterio del prompt (Hotmart, Etsy, Payhip y Gumroad obligatorias) y además todas las plataformas adicionales que se encuentren. |
| L2 | Sin restricción técnica ni de presupuesto: el PRD recomienda stack y una alternativa. |
| L3 | Nombre "Plataforma-PD", carpeta `./investigacion-plataformas/`. |

## Asunciones

- **[ASUNCIÓN]** El universo no tiene tope superior (≥ 60 es el piso). El análisis profundo se mantiene en 20 fichas.
- **[ASUNCIÓN]** Fecha de referencia de la investigación: 2026-10-27. Una cifra anterior a 2025-04 se marca como "de hace más de 18 meses".

## Gates pendientes

- G1 (lista de 20 + 5 suplentes): pendiente.
- G2 (diferenciadores): pendiente.

## Riesgos

| Riesgo | Efecto | Mitigación |
|---|---|---|
| Sin lectura web, no se pueden verificar tráfico, precios ni reseñas. | La investigación no cumple las reglas de evidencia. | Detener y pedir al dueño que habilite el acceso de red del entorno. |
| Las fuentes de los patrones P1 a P5 no se han reverificado. | Un patrón podría no sostenerse. | Reverificar al inicio de la Fase 1, cuando haya lectura web. |
| Los rankings de "alternativas" de plataformas competidoras son marketing. | Sesgo en el descubrimiento de plataformas. | Usarlos solo para encontrar nombres. |

## Próxima acción

1. El dueño del producto amplía el acceso de red del entorno (ver mensaje al usuario).
2. Reintentar `WebFetch` con un dominio de prueba. Si funciona, cerrar Fase 0 y lanzar los 4 subagentes de la Fase 1 sin pedir más permiso.
