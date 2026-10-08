---
tags: [proyecto, productos-digitales, fase-1]
creado: 2026-10-08
estado: en-curso
---

# Fase 1 — Minería de Datos Exhaustiva (Global Trend Engine)

Volver al [[00 - Indice]] · Anterior: [[02 - Fase 0 - Diagnostico y Herramientas]] · Siguiente: [[04 - Fase 2 - Fabrica de Micro-Apps]]

## Objetivo (del brief)
- Búsqueda exhaustiva en EE.UU., Europa, Asia y LatAm de los puntos de dolor más buscados hoy.
- Modelos estadísticos para filtrar necesidades que la gente pagaría por resolver a $20 USD. Sirven 10, 100 o 1,000 nichos.

## Estado y límites honestos de esta primera pasada

> [!warning] Esta pasada es cualitativa y de bajo costo, no la minería estadística final
> La Fase 0 sigue sin aprobarse (presupuesto, claves de API). Por eso esta pasada **no gasta dinero** y usa solo búsqueda web. Genera **hipótesis de nichos con evidencia citada**, no volúmenes de búsqueda ni tendencias medidas.

**Hosts bloqueados por la política de red de este entorno** (probados el 2026-10-08, el proxy responde 403 a la conexión):
- `hn.algolia.com` (Hacker News)
- `api.stackexchange.com` (Stack Exchange)
- `trends.google.com` (Google Trends)
- `reddit.com`

No los rodeé. Para desbloquearlos hay que añadirlos en *Network access* del entorno (menú del entorno en la barra del título → Edit → Allowed domains). `api.github.com` sí responde.

**Pendiente de claves (Fase 0):** volúmenes y CPC reales (DataForSEO), serie de tendencia (Google Trends API alpha). Hasta entonces la señal de demanda del puntaje es un *proxy débil* y cada candidato lo marca como hueco (`no_search_volume`).

## Método

1. **Cinco agentes en paralelo**, uno por región (EE.UU./angloparlante, Europa, Asia, LatAm) buscando en idiomas locales, y uno que calibra qué categorías de herramientas ya se venden a ~$10–$40 en pago único. Regla: nada de datos inventados; lo no observado va como `null`.
2. **Puntaje v0** (`global-trend-engine/score.py`): media geométrica ponderada, 0–100.

| Componente | Peso | Cómo se mide |
|---|---|---|
| Evidencia | 0.15 | Dominios independientes que citan el dolor (tope 4) |
| Pago | 0.30 | Alternativas de pago con precio en rango creíble (pago único $8–$50, mensual $2–$12, anual $15–$100; tope 3) + evidencia explícita de que $20 es plausible |
| Urgencia | 0.20 | Escala 1–5 del agente, con su justificación |
| Construibilidad | 0.20 | Escala 1–5: ¿una micro-app autónoma lo resuelve sin datos propietarios ni cumplimiento pesado? |
| Demanda | 0.15 | **Proxy**: frases de búsqueda reales (tope 5) + volumen observado con fuente |

Se multiplica por la confianza del agente (baja 0.6, media 0.8, alta 1.0). La media geométrica evita que un nicho con un componente casi nulo salga bien por compensar con otros. Los pesos son un punto de partida mío y se recalibran con datos reales.

3. **Validación estadística antes de construir** (`global-trend-engine/faketest.py`): para los finalistas, landing con precio visible + anuncio. Modelo Beta-Binomial: se estima la probabilidad de que la tasa de intención supere la mínima que paga el CAC objetivo.
   - Tasa mínima = CPC ÷ CAC objetivo ÷ *haircut*. Con CPC $0.30, CAC objetivo $9 y *haircut* 0.3, sale ≈ 11%.
   - Regla: GO si P ≥ 0.90 con al menos 300 visitas, DESCARTAR si P ≤ 0.10, CONTINUAR en otro caso.
   - Supuestos a calibrar con las primeras pruebas reales: el *haircut* (qué fracción de la intención mide compras reales) y el prior Beta(1, 30).

## Resultados
_En curso. Se llena cuando terminen los agentes._
