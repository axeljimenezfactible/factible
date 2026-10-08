---
tags: [proyecto, productos-digitales, fase-1]
creado: 2026-10-08
estado: pasada-1-completa
---

# Fase 1 — Minería de Datos Exhaustiva (Global Trend Engine)

Volver al [[00 - Indice]] · Anterior: [[02 - Fase 0 - Diagnostico y Herramientas]] · Siguiente: [[04 - Fase 2 - Fabrica de Micro-Apps]]

## Objetivo (del brief)
- Búsqueda exhaustiva en EE.UU., Europa, Asia y LatAm de los puntos de dolor más buscados hoy.
- Modelos estadísticos para filtrar necesidades que la gente pagaría por resolver a $20 USD. Sirven 10, 100 o 1,000 nichos.

> [!warning] Lo que esta pasada es y no es
> Es una **pasada cualitativa y sin costo**: 112 hipótesis de nicho con evidencia citada. **No es la minería estadística final.** No hay volúmenes de búsqueda ni tendencias medidas, y los puntajes **no son comparables entre regiones** (ver "Límites que condicionan todo").

## Límites que condicionan todo

1. **Ningún agente pudo abrir una página.** Todo sale de resúmenes de búsqueda web. `WebFetch` falló con error de DNS y `curl` recibió 403 de la política de red. Algunas URLs son inferidas del título del resultado y los agentes lo marcaron donde lo notaron.
2. **Presupuesto de búsqueda agotado.** Cada agente alcanzó el tope compartido tras ~35–48 búsquedas, antes de verificar precios o cubrir todos los países que quería.
3. **Sin volúmenes de búsqueda** en ninguno de los 112 candidatos. El componente de demanda es un proxy débil.
4. **Precios de referencia vistos** (candidatos con al menos una alternativa de pago con precio en rango): EE.UU. 11 de 25, Europa 1 de 27, Asia 2 de 29, LatAm 0 de 31. Parte de Europa es un artefacto: el agente vio precios en EUR y SEK pero no los convirtió a USD, así que el motor los ignora. En LatAm sí faltan: casi todos los precios quedaron en `null`.
5. **Ningún candidato con confianza alta.** Máximo "media" (40 de 112); el resto, "baja".
6. **Hosts bloqueados por la política de red** (probado el 2026-10-08): `hn.algolia.com`, `api.stackexchange.com` y `trends.google.com` (el proxy responde 403 a la conexión). `reddit.com` no respondió y un agente lo reporta bloqueado. No se rodearon. Para desbloquearlos: menú del entorno → Edit → *Allowed domains*.

## Método

1. **Cinco agentes en paralelo**: uno por región (EE.UU./angloparlante, Europa, Asia, LatAm), buscando en idiomas locales, y uno que calibra qué categorías ya se venden a ~$10–$40 en pago único. Regla: nada de datos inventados; lo no observado va como `null`.
2. **Puntaje v0.1** (`global-trend-engine/score.py`): media geométrica ponderada, 0–100.

| Componente | Peso | Cómo se mide |
|---|---|---|
| Evidencia | 0.15 | Dominios independientes que citan el dolor (tope 4) |
| Pago | 0.30 | Alternativas de pago con precio en rango creíble (único $8–$50, mensual $2–$12, anual $15–$100; tope 3) + evidencia de que $20 es plausible |
| Urgencia | 0.20 | Escala 1–5 del agente |
| Construibilidad | 0.20 | Escala 1–5 del agente |
| Demanda | 0.15 | **Proxy**: frases de búsqueda reales (tope 5) + volumen con fuente |

Se multiplica por la confianza del agente (baja 0.6, media 0.8, alta 1.0). **Cambio v0 → v0.1:** tras ver que el ranking contradecía la calibración de pago, añadí una penalización de hasta 25% cuando el candidato cita 3 o más alternativas gratuitas o freemium. Solo mira los datos estructurados, así que no capta las gratuitas mencionadas en el texto libre de riesgos. Los pesos son un punto de partida mío.

3. **Validación estadística antes de construir** (`faketest.py`): landing con precio visible + anuncio. Modelo Beta-Binomial: probabilidad de que la tasa de intención supere la mínima que paga el CAC objetivo (CPC ÷ CAC objetivo ÷ *haircut*; con CPC $0.30, CAC $9 y *haircut* 0.3 sale ≈ 11%). Regla: GO si P ≥ 0.90 con al menos 300 visitas; DESCARTAR si P ≤ 0.10. El *haircut* y el prior son supuestos a calibrar.

## Resultados

112 candidatos: 25 EE.UU., 27 Europa, 29 Asia, 31 LatAm. Ranking completo en `global-trend-engine/data/ranking.csv`; la evidencia cruda, en los JSON de la misma carpeta.

### Ranking global (top 15, v0.1)

Por lo dicho arriba, el ranking premia a EE.UU. porque ahí se vieron precios. **Léelo como lista de hipótesis, no como veredicto.** La columna "Lectura" contrasta cada candidato con la calibración de pago.

| # | Región | Candidato | Puntaje | Lectura |
|---|---|---|---|---|
| 1 | US | `home-inventory-insurance-local` | 54.9 | Anclas de pago único $9.99–$19.99. Un usuario pidió alternativa de pago único frente a ~$40/año. Hay apps gratuitas. $20 queda en el techo de la banda |
| 2 | US | `offline-pdf-toolkit` | 52.9 | ⚠ **Contradice la calibración**: el PDF básico no sostiene $20 (PDFgear gratis, Vista Previa de macOS). Rivales de pago único a $19.99–$39.99 |
| 3 | US | `local-audio-file-transcriber` | 52.8 | ✅ Categoría mejor evidenciada: rivales de pago único a $14–$69. MacWhisper declara ~57.5K descargas y ~$100K (newsletter, 2023). Competida |
| 4 | US | `offline-invoice-generator-freelancers` | 52.8 | ⚠ **Contradice la calibración**: la facturación básica es gratis (Wave, Invoice Ninja). Rivales a $10–$59 |
| 5 | ASIA | `in-gst-billing-offline-onetime` | 43.4 | Ancla a $19 pago único (sin ventas verificadas). Los líderes cobran ₹3,399/año o ₹199/mes. Probable precio regional |
| 6 | LATAM | `br-motorista-app-lucro-real` | 42.0 | Sin precios vistos. Segmento de ingresos ajustados: precio regional y Pix |
| 7 | LATAM | `ar-courier-impuestos-compras-exterior` | 40.4 | ⚠ Consumidor masivo con baja disposición a pagar. Reglas volátiles y cifras contradictorias |
| 8 | US | `subscription-audit-from-bank-csv` | 39.9 | Sin ancla de precio |
| 9 | EU | `dac7-ledger-vendedores-segunda-mano` | 39.9 | Competidores cobran €5,99–8,99/mes (sin convertir). Un pago único cubre pocos meses de eso |
| 10 | US | `resume-builder-no-billing-trap` | 38.8 | ⚠ Saturado. Los rivales cobran ~$23–$30 por ciclo, con trampa de renovación |
| 11 | EU | `nebenkosten-check-mieter` | 38.2 | Servicios de revisión cobran €14,90–99,90 (Finanztip). Zona regulada (RDG) |
| 12 | ASIA | `in-exam-photo-signature-resizer` | 37.9 | Alternativa gratuita citada. Sin ancla de precio |
| 13 | LATAM | `latam-reposteria-costeo-es` | 37.1 | Sin ancla de precio |
| 14 | US | `mileage-log-manual-export` | 36.8 | MileIQ ~$140/año; vitalicio más barato ~$100–$120. Zona fiscal |
| 15 | ASIA | `id-sscasn-document-prep` | 36.6 | ⚠ El propio agente: $20 no es plausible; alternativas gratis abundantes |

### Top 5 por región (la comparación válida)

- **EE.UU.:** `home-inventory-insurance-local`, `offline-pdf-toolkit`, `local-audio-file-transcriber`, `offline-invoice-generator-freelancers`, `subscription-audit-from-bank-csv`
- **Europa:** `dac7-ledger-vendedores-segunda-mano`, `nebenkosten-check-mieter`, `rechtstexte-generator-datenschutz-impressum`, `sepa-xml-desde-excel`, `e-rechnung-reader-offline`
- **Asia:** `in-gst-billing-offline-onetime`, `in-exam-photo-signature-resizer`, `id-sscasn-document-prep`, `id-coretax-xml-validator`, `vn-marketplace-fee-profit-tax`
- **LatAm:** `br-motorista-app-lucro-real`, `ar-courier-impuestos-compras-exterior`, `latam-reposteria-costeo-es`, `mx-freelancer-usd-cfdi-resico`, `br-freelancer-dolar-nfse-carneleao`

### Calibración de pago: qué se vende hoy a ~$20

Del agente de calibración (todo según resúmenes de búsqueda, muestra sesgada a apps indie de Mac):

- **Sí venden:** utilidades de un solo propósito a $10–$20 (DaisyDisk $9.99 con 2,676 valoraciones; PDF Squeezer 4 $19.99 con ~1.8K), captura de pantalla a $29 con 1 año de actualizaciones, utilidades de desarrollo e IA local a $29–$69, automatización para usuarios avanzados a $24–$42.
- **No sostienen $20:** PDF básico, gestores de ventanas y de portapapeles, facturación y control de tiempo básicos, plantillas de presupuesto ($3.99–$15), extensiones de navegador como negocio (57% gana $0; conversión ~0.8%).
- **Precio:** $20 es el **techo** de las utilidades de un solo propósito y queda **por debajo** de lo que cobran las herramientas que más ingresan ($29–$69). La mediana de producto de pago en Gumroad es $7. **No se encontró evidencia directa de que $19, $20 o $29 conviertan mejor que $9 o $49**: el precio hay que probarlo.
- **Reembolsos:** los motivos repetidos son cobro distinto al anunciado, no poder probar antes de comprar, y "vitalicio" que deja de funcionar. Quien cobra $29+ ofrece garantía de 30 días.

### Temas que se repiten entre regiones

Clasificación mía por palabras clave del id y el dolor, aproximada. 78 de los 112 candidatos caen en uno de seis temas:

| Tema | Candidatos | Regiones | Por qué importa |
|---|---|---|---|
| Impuestos y régimen de autónomos y freelancers (simuladores y trackers por país) | 20 | LatAm 9, Asia 6, Europa 5 | Mismo motor con "paquete de reglas" por país: encaja con la fábrica modular de la Fase 2. Riesgos: zona regulada, reglas que cambian, calculadoras oficiales gratuitas |
| Facturación electrónica y cumplimiento (leer, validar, convertir formatos oficiales) | 17 | Asia 9, Europa 5, LatAm 3 | Obligaciones con fecha límite crean urgencia. Mucha competencia gratuita |
| Reemplazo offline de pago único para herramientas con suscripción o límites | 22 | EE.UU. 18, Asia 2, Europa 2 | Es donde hay precios visibles; es también donde la calibración advierte saturación |
| Ganancia real de vendedores de marketplace y revendedores | 8 | Asia 4, Europa 3, EE.UU. 1 | Cambios de comisión e impuestos en 2026 crean la urgencia |
| Ganancia real de trabajo por plataforma y microneg. (costeo, cobranza) | 7 | Solo LatAm | Audiencia grande, baja disposición a pagar |
| Preparar fotos y documentos para portales oficiales | 4 | Asia 3, EE.UU. 1 | Alternativas gratuitas abundantes |

Los dos temas de impuestos y facturación tienen puntaje promedio bajo (20.7 y 22.8) frente a 28.8 del tema de reemplazo offline, que es casi todo de EE.UU. Es por la falta de precios vistos en esas regiones, no porque haya menos demanda.

### Propuesta de finalistas para prueba de puerta falsa

Mi propuesta, no una decisión; pendiente de que apruebes presupuesto de anuncios:

1. `local-audio-file-transcriber`: la mejor evidencia de pago. Probar $19 contra $29.
2. `home-inventory-insurance-local`: anclas $9.99–$19.99 y petición explícita de pago único.
3. **Paquete freelancer que cobra en USD** (`ar-`, `br-`, `mx-freelancer-…`): tres variantes del mismo motor. *Hipótesis:* quien cobra en dólares sí puede pagar $20. Un titular citado dice que el 93% de los freelancers argentinos cobra en USD, **sin verificar**.
4. `br-motorista-app-lucro-real`: audiencia enorme; probar precio regional y Pix.
5. `dac7-ledger-vendedores-segunda-mano`: la suscripción de los competidores hace fácil el argumento del pago único.
6. `nebenkosten-check-mieter`: hay precio de referencia por revisión; cuidar el encuadre regulatorio.
7. `in-gst-billing-offline-onetime`: ancla a $19 contra suscripciones anuales; probar precio regional.

Dejo fuera `offline-pdf-toolkit` y `offline-invoice-generator-freelancers`, salvo que tengan un diferenciador que la calibración no contradiga.

## Para pasar de hipótesis a datos

1. **Desbloquear los hosts** (HN, Stack Exchange, Google Trends, Reddit) y **aprobar las claves de la Fase 0** (DataForSEO) para tener volúmenes y CPC reales.
2. **Segunda pasada de agentes** con presupuesto de búsqueda nuevo: verificar las evidencias del top 15, y registrar precios en moneda local más una tabla de cambio fija (campos `price_local` y `currency`), para que Europa deje de quedar subvalorada.
3. **Puertas falsas** de los finalistas, con la calculadora `faketest.py`. Requieren cuenta publicitaria y presupuesto, que son decisiones tuyas.

## Archivos
- `global-trend-engine/score.py`, `faketest.py`, `tests/` (14 pruebas)
- `global-trend-engine/data/`: `fase1_us.json`, `fase1_eu.json`, `fase1_asia.json`, `fase1_latam.json`, `fase1_wtp.json`, `ranking_v0.csv` (antes de la penalización), `ranking.csv` (v0.1)
