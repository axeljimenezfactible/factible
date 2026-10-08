---
tags: [proyecto, productos-digitales, fase-0]
creado: 2026-10-08
estado: borrador-para-aprobacion
---

# Fase 0 — Diagnóstico Inicial y Desbloqueo de Herramientas

Volver al [[00 - Indice]] · Brief: [[01 - Brief Maestro]] · Siguiente: [[03 - Fase 1 - Global Trend Engine]]

> [!important] Cómo leer los precios
> Los precios salen de búsquedas web del 2026-10-08, casi todas de blogs de terceros, no de las páginas oficiales de cada proveedor. Se marcan **(verificar)** donde las fuentes se contradicen. Confirma cada precio en la página oficial antes de pagar.

## 1. Diagnóstico en una frase

Con una meta de **1,000,000 × $20 = $20M brutos**, lo difícil no es crear los productos. Lo difícil es **distribuirlos a un costo de adquisición (CAC) menor que lo que deja cada venta**. Por eso las herramientas de la Fase 0 sirven para tres cosas: encontrar demanda real, validarla barato antes de construir, y cobrar a nivel mundial sin pelear con impuestos.

## 2. Economía unitaria de un ticket de $20

Comisión de un Merchant of Record (MoR). Lemon Squeezy cobra **5% + $0.50** por transacción. Recargos: **+1.5%** fuera de EE.UU., **+1.5%** por PayPal. El porcentaje se aplica sobre el total con impuestos incluidos. Paddle publica el mismo 5% + $0.50, pero una fuente le suma +2% internacional **(verificar)**.

| Escenario | Comisión | Neto por venta |
|---|---|---|
| Tarjeta, EE.UU. (5% + $0.50) | $1.50 | **$18.50** |
| Tarjeta, internacional (6.5% + $0.50) | $1.80 | **$18.20** |
| PayPal, internacional (8% + $0.50) | $2.10 | **$17.90** |

Reglas de diseño que salen de esta tabla:
- **CAC de equilibrio ≈ $18** (sin soporte, hosting ni reembolsos). Es un techo, no una meta.
- **CAC objetivo ≤ $9** *(hipótesis: ~50% de margen de contribución)*. Reserva 5–8% para reembolsos y contracargos *(supuesto)*.
- **Order bump / upsell** (por ejemplo $20 → $29–$39 con un paquete) mueve más el resultado que bajar el CPC.
- **Precios regionales** en LatAm, Sur de Asia y África. $20 es un ticket alto en esos mercados y un precio único recortaría la conversión.

## 3. Matemática del embudo para 1M de ventas

| Conversión visita → compra | Visitas necesarias |
|---|---|
| 1% | 100,000,000 |
| 2% | 50,000,000 |
| 3% | 33,300,000 |
| 5% | 20,000,000 |

Con CPC y conversión *ilustrativos* (supuestos, no datos): CPC $0.20 y 3% de conversión dan CAC ≈ $6.7. CPC $0.40 y 2% dan CAC = $20, o sea pérdida. **Conclusión:** el tráfico pagado solo no sostiene el millón. Hay que combinar SEO programático (una página por micro-nicho), afiliados con comisión, bucles virales dentro del propio producto y marketplaces. Eso se diseña en [[06 - Fase 4 - Trafico y Adquisicion]]. Para la Fase 0 importa porque **la mina de datos también debe medir "qué tan barato es llegar a este nicho"**, no solo "qué tan grande es".

## 4. Stack de herramientas a desbloquear

### A. Minería de demanda (Fase 1)

| Herramienta | Para qué | Costo | Notas |
|---|---|---|---|
| Google Trends (web) | Tendencia por país/idioma | Gratis | Sin API oficial abierta |
| [Google Trends API (alpha)](https://developers.google.com/search/apis/trends) | Tendencias consistentes, ventana de 5 años, comparación regional | Sin precio público | Acceso **por solicitud**. **Aplicar hoy**: no hay certeza de aprobación |
| [DataForSEO](https://docs.dataforseo.com/v3/dataforseo_trends/overview/) | Tendencias y volúmenes en masa, pago por uso | ~$0.001/tarea (serie propia) a ~$0.009/tarea (serie Google) **(verificar)** | Límite 2,000 req/min. 10,000 keywords ≈ $2–$18. **Recomendado sobre suscripciones**: la minería es por lotes, no por asiento |
| Semrush Pro / Ahrefs Lite | Contraste manual y análisis de competidores | Semrush ~$139/mes (7 días de prueba). Ahrefs Lite $99–$129/mes **(verificar)** | Solo 1 mes puntual para contrastar. No como base del motor |
| [Apify](https://use-apify.com/docs/best-apify-actors/best-reddit-scrapers) (scrapers de Reddit, foros, reseñas) | Dolores textuales: "cómo hago…", "odio que…" | ~$3.40 por 1,000 resultados; 20k posts ≈ $68 **(verificar)** | Revisar términos de cada sitio antes de extraer |
| Reddit API oficial | Alternativa a scrapers | Gratis sin uso comercial. Uso comercial por negociación **(verificar)**. Fuentes citan ~$0.24 por 1,000 llamadas | Sus términos por defecto prohíben usar los datos para ML. **Revisión legal antes de usarlo** |
| APIs gratuitas: Hacker News, Stack Exchange, YouTube Data, Product Hunt | Dolor profesional y técnico | Gratis (verificar cuotas) | Rápidas de conectar |
| API de LLM (Claude) | Clasificar, agrupar y puntuar millones de textos | Por tokens (revisar tarifa vigente) | Aquí vive el "escuadrón de agentes" |

### B. Cobro y cumplimiento fiscal

| Herramienta | Para qué | Costo |
|---|---|---|
| **Lemon Squeezy** o **Paddle** (MoR) | Cobro global, IVA/sales tax, moneda local, PayPal | 5% + $0.50 (ver sección 2) |
| Stripe directo | Más barato por venta, pero **tú** resuelves impuestos por país | ~2.9% + $0.30 (EE.UU., conocimiento general, verificar) |

Recomendación: **MoR al arrancar**. A escala mundial el cumplimiento fiscal por país es un trabajo en sí mismo. Se revisa pasar a Stripe directo cuando el volumen justifique el equipo. Ambos requieren **verificación de tu negocio y una cuenta de pago**.

### C. Construcción y publicación (Fases 2–3)
Claude Code / API de Claude para generar código, GitHub para versionar, hosting estático o edge (Vercel / Cloudflare Pages, con capas gratuitas), Supabase o similar para backend ligero, PWA o Capacitor para empaquetar. Se detalla en [[05 - Fase 3 - Motor de Creacion]]. **No hay compra urgente aquí.**

### D. Medición y adquisición (Fase 4)
Analítica de producto (PostHog o Plausible), email transaccional (Resend o similar), cuentas publicitarias (Meta, Google, TikTok, Reddit Ads) con **presupuesto de prueba**. Se activa solo después de que un nicho pase la validación de la Fase 1.

## 5. Presupuesto de arranque (primer mes, solo Fase 1)

| Concepto | Estimado |
|---|---|
| DataForSEO (saldo prepago) | ~$100 |
| Semrush Pro, 1 mes (opcional) | ~$139 |
| Apify, scrapers de dolor | ~$70 |
| Créditos de API de LLM | ~$100 |
| Dominio | ~$15 |
| **Total estimado** | **≈ $400–$450** |

Es una estimación mía, no una cotización. El MoR no cuesta nada hasta la primera venta. Los anuncios de validación son un presupuesto aparte, a definir en la Fase 1.

## 6. Puertas de salida de la Fase 0 (Go / No-Go)

- [ ] Solicitud a la Google Trends API alpha enviada
- [ ] Cuenta DataForSEO con saldo y una consulta de prueba exitosa
- [ ] Credenciales de Apify y de al menos 3 fuentes gratuitas (HN, Stack Exchange, YouTube)
- [ ] Revisión legal rápida de términos de extracción (Reddit y las demás fuentes)
- [ ] Cuenta MoR (Lemon Squeezy o Paddle) iniciada, con la verificación del negocio en proceso
- [ ] Presupuesto del primer mes aprobado

## 7. Lo que necesito de ti
1. **Aprobar el presupuesto** de la sección 5 (o ajustarlo).
2. **Crear las cuentas y compartirme las claves de API.** Yo no puedo comprar licencias ni abrir cuentas a tu nombre. Las claves van en variables de entorno o un gestor de secretos, nunca en este repo.
3. **Elegir el MoR** (Lemon Squeezy o Paddle) y la entidad legal que recibirá los pagos.
4. **Confirmar el orden de mercados** para la Fase 1 (EE.UU., Europa, Asia, LatAm) o dejar que los datos lo decidan.

## 8. Fuentes
- [Google Trends API alpha](https://developers.google.com/search/apis/trends)
- [DataForSEO — Trends API](https://docs.dataforseo.com/v3/dataforseo_trends/overview/) · [comparativa de precios 2026](https://www.socialcrawl.dev/blog/best-google-trends-apis-2026)
- [Semrush vs Ahrefs — precios 2026](https://konabayev.com/blog/seo-tool-pricing-2026/)
- [Lemon Squeezy — comisiones](https://docs.lemonsqueezy.com/help/getting-started/fees) · [Paddle vs Lemon Squeezy](https://resources.rework.com/tools/billing-revenue/paddle-vs-lemon-squeezy)
- [Reddit API — precios 2026](https://www.redditapis.com/blogs/reddit-api-pricing-2026) · [Apify — scrapers de Reddit](https://use-apify.com/docs/best-apify-actors/best-reddit-scrapers)
