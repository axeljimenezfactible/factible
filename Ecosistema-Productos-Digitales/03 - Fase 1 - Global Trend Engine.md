---
tags: [proyecto, productos-digitales, fase-1]
creado: 2026-10-08
estado: pasada-3-completa
---

# Fase 1 — Minería de Datos Exhaustiva (Global Trend Engine)

Volver al [[00 - Indice]] · Anterior: [[02 - Fase 0 - Diagnostico y Herramientas]] · Siguiente: [[04 - Fase 2 - Fabrica de Micro-Apps]]

## Objetivo (del brief)
- Búsqueda exhaustiva en EE.UU., Europa, Asia y LatAm de los puntos de dolor más buscados hoy.
- Modelos estadísticos para filtrar necesidades que la gente pagaría por resolver a $20 USD. Sirven 10, 100 o 1,000 nichos.

> [!warning] Lo que esta pasada es y no es
> Es una **pasada cualitativa y sin costo**: 112 hipótesis de nicho con evidencia citada. **No es la minería estadística final.** No hay volúmenes de búsqueda ni tendencias medidas, y los puntajes **no son comparables entre regiones** (ver "Límites que condicionan todo").

## Límites que condicionan todo

1. **Ningún agente de las dos pasadas pudo abrir una página.** Todo sale de resúmenes de búsqueda web. `WebFetch` falló con error de DNS y `curl` recibió 403 de la política de red. Algunas URLs son inferidas del título del resultado y los agentes lo marcaron donde lo notaron.
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

### Propuesta de finalistas de la pasada 1 (superada por la pasada 2)

Se conserva como registro: la pasada 2 la desmontó en buena parte (ver más abajo). Propuesta original:

1. `local-audio-file-transcriber`: la mejor evidencia de pago. Probar $19 contra $29.
2. `home-inventory-insurance-local`: anclas $9.99–$19.99 y petición explícita de pago único.
3. **Paquete freelancer que cobra en USD** (`ar-`, `br-`, `mx-freelancer-…`): tres variantes del mismo motor. *Hipótesis:* quien cobra en dólares sí puede pagar $20. Un titular citado dice que el 93% de los freelancers argentinos cobra en USD, **sin verificar**.
4. `br-motorista-app-lucro-real`: audiencia enorme; probar precio regional y Pix.
5. `dac7-ledger-vendedores-segunda-mano`: la suscripción de los competidores hace fácil el argumento del pago único.
6. `nebenkosten-check-mieter`: hay precio de referencia por revisión; cuidar el encuadre regulatorio.
7. `in-gst-billing-offline-onetime`: ancla a $19 contra suscripciones anuales; probar precio regional.

Dejo fuera `offline-pdf-toolkit` y `offline-invoice-generator-freelancers`, salvo que tengan un diferenciador que la calibración no contradiga.

## Pasada 2: verificación (2026-10-08)

Cinco agentes: cuatro verificaron 24 candidatos (EE.UU. 7, Europa 5, Asia 6, LatAm 6) y uno reunió referencias de costo por clic. Cada uno hizo entre 34 y 39 búsquedas, sin rechazos. Como en la pasada 1, nadie pudo abrir páginas: **"confirmado" significa que una fuente independiente lo respalda en su resumen de búsqueda**, no que alguien leyó la página. Los veredictos completos, con la razón de cada agente, están en `global-trend-engine/data/verificacion_pasada2.csv`.

### Lo que cambió

- **La pasada 1 subestimó la competencia gratuita.** Registró en promedio **0.8** alternativas gratuitas por candidato (11 de los 24 sin ninguna). La verificación encontró **5.0** en promedio (mínimo 3, máximo 8).
- **Veredicto de los agentes sobre los 24:** 14 descartar, 9 rehacer, 1 mantener. 23 quedan con confianza baja y 1 con media.
- **Los finalistas de la pasada 1 (9 candidatos en 7 propuestas):** ninguno se mantiene; 5 pasan a rehacer y 4 a descartar.

| Candidato | Pos. en pasada 1 | Pasada 2 | Por qué |
|---|---|---|---|
| `local-audio-file-transcriber` | 3 | Rehacer | Buzz y Vibe, gratuitos, hacen lo mismo. Precios: Whisper Notes entre $6.99 y $14 (las fuentes se contradicen), MacWhisper €59 (no €64). Solo defendible como app sin configuración para usuarios no técnicos en Windows |
| `home-inventory-insurance-local` | 1 | Descartar | Apps gratuitas (NAIC, Know Your Stuff, Encircle) y rivales de pago único a $5–$10. Under My Roof cuesta ~$25/año, no $40 |
| `ar-freelancer-factura-e-cobro-exterior` | 33 | Rehacer | El simulador de ARCA y las guías gratuitas cubren cada pieza. Solo vale como flujo único con vigencia fechada, o fusionado con otro país |
| `br-freelancer-dolar-nfse-carneleao` | 25 | Descartar | Calculadora gratuita casi idéntica (Contabilidade Zen) y Carnê-Leão Web gratuito |
| `mx-freelancer-usd-cfdi-resico` | 16 | Rehacer | Hueco estrecho rodeado de guías gratuitas. Hay que validar la disposición a pagar con compradores reales |
| `br-motorista-app-lucro-real` | 6 | Descartar | Drivvo Premium cuesta R$2/mes o R$12/año, FinDriver es gratuita y 99 tiene calculadora oficial |
| `dac7-ledger-vendedores-segunda-mano` | 9 | Rehacer | Margeo ya tiene contador DAC7, plan gratuito (tope de 30 artículos), Pro a €7,99/mes o €69/año y plantilla Excel gratuita. Hueco: libro local multipaís, sin tope ni suscripción |
| `nebenkosten-check-mieter` | 11 | Rehacer | Nebenkostenpro cobra €14,90 con carta, Mineko €39–69 y el Mieterbund ofrece checks gratuitos. Solo como checklist offline reutilizable. El plazo legal para objetar es de 12 meses (§556 BGB), no 4 semanas |
| `in-gst-billing-offline-onetime` | 5 | Descartar | Opciones gratuitas offline y planes de ₹399/año. El ancla de $19 viene solo del post de su propio vendedor |
| `resume-builder-no-billing-trap` | 10 | **Mantener** (media) | La única. Quejas recientes (Trustpilot, mar–abr 2026), Zety renueva cada 4 semanas, y no se encontró herramienta que combine constructor local y comparación de palabras clave contra la oferta (Jobscan $49.95/mes; Kickresume en la nube). Sigue saturado y dominado por SEO |

**Otros veredictos.** Descartar: `subscription-audit-from-bank-csv`, `offline-pdf-toolkit`, `offline-invoice-generator-freelancers`, `rechtstexte-generator-datenschutz-impressum`, `e-rechnung-reader-offline`, `in-exam-photo-signature-resizer`, `id-sscasn-document-prep`, `jp-pdf-tools-lifetime`, `ar-courier-impuestos-compras-exterior`, `latam-reposteria-costeo-es`. Rehacer: `mileage-log-manual-export` (solo un giro sin validar: reconstruir kilometraje pasado), `sepa-xml-desde-excel` (ventana corta: los formatos viejos valen hasta nov-2026), `id-coretax-xml-validator` (solo como pre-validador por filas para contadores con varios clientes), `vn-marketplace-fee-profit-tax` (calculadora con tarifas editables; el 28-may-2026 el regulador pidió a Shopee no aplicar cargos nuevos y esta difirió el de visibilidad, pero no el aumento del cargo COD de 4,91% a 6%).

### El dato del "93%"

Viene de Deel y cubre solo a sus contratistas argentinos, medido como retiros en dólares (mayo 2025–abril 2026). **No es una encuesta del segmento.** Infobae cita 90% de otro estudio privado. No hay cifras comparables de Brasil ni México; para Colombia hay 34%. La hipótesis de que "quien cobra en dólares puede pagar $20" queda sin respaldo general.

### Costo de adquisición

Todas las cifras salen de blogs y agencias, no de datos de plataforma, y las fuentes discrepan entre sí. Detalle en `data/fase1b_cpc.json`.

| Referencia | Valor |
|---|---|
| Google Search EE.UU., CPC medio | $5.26–$5.42 (WordStream 2025–26, vía resúmenes) |
| "transcribe audio to text", EE.UU. | $5.99 con ~22.2k búsquedas/mes (seodata.dev); otra herramienta reporta $9.89–$11.88 para variantes |
| "home inventory", EE.UU. | $2.01, ~1.3k búsquedas/mes |
| Meta, CPC | EE.UU. $1.11–$2.69; México $0.35–$0.80; Argentina $0.15–$0.90 |
| Google Alemania, por categoría | Software €2–8, finanzas €3–15, seguros €10–50 |
| Conversión | Landing promedio 2.35%; Meta e-commerce, mediana clic→compra 1.57%. **Ninguna cifra específica de producto digital de $20** |
| Afiliados | 30–50% en productos digitales de pago único (= $6–$10 por venta de $20); 15–30% en SaaS |
| Gumroad | 10% + $0.50 en ventas directas; 30% en Discover |

Aritmética del agente (CAC = CPC ÷ conversión). Para un CAC de $9, el CPC máximo es **$0.14, $0.27 o $0.45** con conversión de 1.57%, 3% o 5%. **El 3% es un supuesto: no se midió en ningún nicho.** Con 3%: transcripción en EE.UU. ≈ $130–$400 por venta en Google y $37–$90 en Meta; inventario del hogar ≈ $67; software en Alemania ≈ €67–267. **Ningún nicho tiene respaldo público para un CAC ≤ $9 con anuncios.** EE.UU. y Alemania no son plausibles por esa vía. México, Argentina, Brasil e India quedan sin concluir: los CPC son bajos, pero faltan datos por término y de conversión, y es donde la disposición a pagar $20 es menor.

### Lectura mía

1. **La señal más fuerte no es un nicho, es el criterio.** Un dolor solo es oportunidad si no tiene equivalente gratuito. "Hueco frente a lo gratuito" debe ser el filtro principal, antes que urgencia o volumen.
2. **Con anuncios, un producto de consumo a $20 no cuadra en EE.UU. ni Alemania** según estos benchmarks. Quedan estas palancas: afiliados (el costo es la comisión, $6–$10), contenido y SEO de cola larga, marketplaces, precios más altos en herramientas profesionales ($29–$69 según la calibración), y nichos profesionales donde el comprador paga por tiempo ahorrado (contadores con varios clientes, conversión SEPA con fecha límite). Son hipótesis a probar, no resultados.
3. **Los 88 candidatos sin verificar probablemente siguen el patrón** de la pasada 1: omitieron competencia gratuita. Es una inferencia mía, no verificada. No los doy por buenos.

## Pasada 3: enfoque invertido (2026-10-08)

Cinco agentes partieron de categorías que ya venden (utilidades de propósito único, captura e imagen, IA local y desarrollo, automatización, nichos profesionales) y buscaron el hueco que dejan los gratuitos. Método obligatorio: buscar primero 3 o más alternativas gratuitas, rechazar la idea si una la cubre, y solo entonces buscar evidencia de necesidad (2 fuentes independientes) y de precio. El tope de búsquedas compartido (200 por turno) se agotó en cada agente tras ~36–49 búsquedas, así que solo el de IA local llegó a la meta de 6 sobrevivientes; los demás dejaron 4. De nuevo nadie pudo abrir páginas.

### Resultado

- **22 sobrevivientes y 53 rechazados.** De las 75 ideas registradas, cayó el 71%. Tablas completas: `data/candidatos_pasada3.csv` y `data/rechazados_pasada3.csv`.
- **Confianza:** 4 media, 18 baja, ninguna alta.
- **Precio objetivo propuesto:** mediana de $29; 16 de los 20 que tienen precio quedan entre $19 y $49.
- **Plataforma:** 15 multiplataforma, 3 solo Mac, 3 solo Windows, 1 web.

### Los cuatro de confianza media

| Candidato | Objetivo | Pagos observados | Hueco | Riesgo principal |
|---|---|---|---|---|
| `steps-recorder-successor-local` (Windows) | $29 | Pago único: Screenpresso Pro $29.99, ScreenSnap Pro $39, StepGrab $44.99 (Mac). Suscripción: Scribe $25–35/mes, Guidde $19–29/mes | Microsoft retiró Steps Recorder. Lo que genera los pasos solo es en la nube y por suscripción; los gratuitos locales son jóvenes o inactivos | Capturar por clic exige hooks de bajo nivel y firma de código; los antivirus pueden marcarlo; aparecen competidores gratuitos nuevos |
| `audio-anonimizador-entrevistas` | $39 | Solo referencia forense: CaseGuard ~$299/usuario/mes. MacWhisper Pro €59 como ancla de transcripción local | Hoy se silencian nombres y teléfonos a mano en Audacity; la detección automática existe solo como código de investigación | Sin comparable a precio de consumidor. La detección de nombres tuvo F1 de 0.77 en un prototipo: exige revisión humana y no se puede prometer anonimato |
| `extractos-bancarios-local-csv` | $49 | LedgerSprout $129 pago único; varios SaaS con ingresos pequeños ($0.6k–2.3k MRR en los listados claros) | Tabula y pdfplumber fallan con filas de varias líneas y con escaneos | Mercado saturado; cada banco tiene su formato; un error en un importe es crítico |
| `scanned-photo-splitter-robust` (Mac y Windows) | $29 | ScanSpeeder desde $29.95; AutoSplitter ~$20–40 | Un usuario reporta que AutoSplitter no reconoce nada con huecos pequeños y acierta solo 30–50% con huecos grandes | Los incumbentes tienen prueba gratuita; hay que validar la precisión con escaneos reales antes de construir |

### Otros con señal de precio

- `culling-ia-local-pago-unico` (fotógrafos de bodas, $79): Aftershoot ~$120/año, FilterPixel ~$180/año, Narrative Select $10–15/mes; Photo Mechanic es de pago único pero sin IA. Construcción difícil (visión por computadora y formatos RAW de muchas cámaras). Sin ventas verificadas.
- `conciliador-payouts-etsy-csv` ($39): Link My Books $17–21/mes y A2X $29/mes. No hay pago único equivalente, lo que puede ser un hueco o falta de demanda.
- `limpiador-metadatos-oficina` ($19): BatchPurifier cuesta $19 en Windows; en Mac solo hay un título antiguo y una herramienta de línea de comandos.
- `takeout-photo-date-fixer-gui` ($19.99): ya hay un vendedor de pago único a ~$24–30, y la herramienta gratuita GPTH Neo está activa.
- `cotizador-ponderado-traductores` ($39): TO3000 cuesta €75–260 y AnyCount €49+.
- El resto, todos de confianza baja: `ia-por-lotes-tabla`, `emails-a-pdf-por-lotes`, `autoguardado-adjuntos-correo`, `dividir-excel-por-columna`, `cross-platform-filename-preflight`, `apple-photos-export-onetime`, `screen-recording-secret-redactor`, `face-plate-anonymizer-offline`, `libro-a-audio-local`, `etiquetado-fotos-ia-local`, `traductor-pdf-local-formato`, `takeoff-pdf-oficios-mac-pago-unico`, `publisher-pub-converter` (su ventana cierra: el soporte perpetuo de Publisher termina el 13-oct-2026).

### Qué enseña

1. **Lo que ya está cubierto.** Los rechazos incluyen clones de CleanShot, Xnapper y Snagit para Windows y Linux, DaisyDisk y Permute para Windows y Linux, Hazel y Keyboard Maestro para Windows, expansión de texto, chat con documentos y quitafondos: hay gratuitos o pagos baratos que los cubren.
2. **El techo de $20.** Según el agente de utilidades, las utilidades de una sola función se venden a $3–$10, y MacUpdater cerró en enero de 2026 por no sostener el pago único. Los $20 se aguantan solo en flujos de varios pasos.
3. **Nichos profesionales.** "Pagan más": respaldado, con precios de $40–$300 en pago único y $17–$120 al mes. "Se alcanzan más barato": solo indicios y ninguna cifra de costo (descuento para miembros de ProZ, beneficios de ASMP, tienda de apps de Xero, Setapp). La saturación sigue alta: 10 de las 14 ideas de ese agente cayeron, y en 2026 aparecieron herramientas gratuitas nuevas.
4. **Matemática de portafolio (inferencia mía).** El mejor caso de tracción visto es MacWhisper, con ~57.5K descargas y ~$100K (newsletter de 2023, autodeclarado, sin verificar). Un millón de ventas equivale a unos 17 productos de ese nivel, o a 100–200 productos si cada uno vendiera 5–10 mil unidades (supuesto ilustrativo mío, sin datos). Si el portafolio es el camino, el costo de producir cada micro-app pasa a ser la variable decisiva, y eso le da sentido al diseño modular y a la automatización de las Fases 2 y 3.

### Límites de esta pasada

Mismos que antes: solo resúmenes de búsqueda, sin hilos de usuarios con fecha (Reddit y HN no son accesibles), precios tomados de agregadores y no de las webs de los vendedores, y casi todas las fechas en `null`. Ningún candidato llega a confianza alta.

## Para pasar de hipótesis a datos

1. **Abrir la red y las credenciales.** En el menú del entorno → *Edit* → *Network access*, añadir `hn.algolia.com`, `api.stackexchange.com`, `trends.google.com` y `api.dataforseo.com` (confirmar este último en la documentación de DataForSEO). Crear la cuenta de DataForSEO con saldo y guardar sus credenciales de API como `DATAFORSEO_LOGIN` y `DATAFORSEO_PASSWORD` en *Network secrets* (o *API credentials*), o como variables de entorno. Una sesión nueva las toma. Nunca pegar claves en el chat.
2. **Medir volúmenes y CPC por término** de los 22 sobrevivientes y los 9 "rehacer". Requiere el paso 1; es lo que falta para pasar de hipótesis a datos.
3. **Puertas falsas**, empezando por los 4 de confianza media, con precios de prueba de $19, $29 y $39. Requieren cuenta publicitaria y presupuesto, decisiones del usuario.
4. **Fase 2 en paralelo.** Por la matemática de portafolio, los componentes compartidos (licencias, cobro vía comerciante de registro, actualizaciones, empaquetado para Windows y Mac, telemetría con consentimiento) son lo que decide si el modelo escala. Propuesto, no iniciado.
5. **Tabla de cambio fija** (`price_local` y `currency`): no se aplicó, porque la verificación reordenó la lista de todos modos. Queda para cuando se vuelva a puntuar.

## Archivos
- `global-trend-engine/score.py`, `faketest.py`, `tests/` (14 pruebas)
- `global-trend-engine/data/`: `fase1_us.json`, `fase1_eu.json`, `fase1_asia.json`, `fase1_latam.json`, `fase1_wtp.json`, `ranking_v0.csv` (antes de la penalización), `ranking.csv` (v0.1)
- Pasada 2: `fase1b_us.json`, `fase1b_eu.json`, `fase1b_asia.json`, `fase1b_latam.json`, `fase1b_cpc.json`, `verificacion_pasada2.csv`
- Pasada 3: `fase1c_utilidades.json`, `fase1c_captura.json`, `fase1c_ia_dev.json`, `fase1c_automatizacion.json`, `fase1c_profesional.json`, `candidatos_pasada3.csv`, `rechazados_pasada3.csv`
