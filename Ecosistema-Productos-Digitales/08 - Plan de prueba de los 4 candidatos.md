---
tags: [proyecto, productos-digitales, plan-de-prueba]
creado: 2026-10-08
estado: plan
---

# Plan de prueba de los 4 candidatos de confianza media

Volver al [[00 - Indice]] · Origen: [[03 - Fase 1 - Global Trend Engine]] (pasada 3) · Recetas: [[04 - Fase 2 - Fabrica de Micro-Apps]] · Qué te toca: [[07 - Guia - Que debes hacer tu]]

> [!warning] Es un plan, no un resultado
> Los umbrales de abajo son **aritmética mía sobre supuestos**: que solo el 30% de la intención medida termina en compra (*haircut*), que el CAC objetivo es el 50% del neto por venta, y costos por clic tomados de blogs de agencias. Se recalibran con los primeros datos reales.

## Los cuatro candidatos

`steps-recorder-successor-local` · `audio-anonimizador-entrevistas` · `extractos-bancarios-local-csv` · `scanned-photo-splitter-robust`

## Orden de trabajo

1. **Etapa A: demanda, sin anuncios.** Medir volumen y costo por clic de las palabras clave de cada candidato con DataForSEO, y buscar señales en Hacker News y Stack Exchange. Requiere los pasos 1 a 4 de la guía [[07 - Guia - Que debes hacer tu]].
2. **Etapa B: puerta falsa.** Una página con el precio visible y un botón de "Quiero esto" que lleva a una lista de espera. **No se cobra y se dice abiertamente que el producto aún no está disponible** (por ejemplo: "Lanzamiento próximo: deja tu correo y recibe un descuento"). Requiere cuenta publicitaria, presupuesto, dominio y página.
3. **Etapa C: decisión** con `global-trend-engine/faketest.py`: GO si la probabilidad de superar la tasa mínima es de al menos 0.90 con 300 visitas o más; DESCARTAR si es de 0.10 o menos; CONTINUAR en otro caso.

## Cuánta intención hace falta, según precio y costo por clic

Tasa mínima de intención = CPC ÷ (CAC objetivo × 0.30). CAC objetivo = 50% del neto por venta con comisión de 5% + $0.50.

| Precio | Neto | CAC objetivo | Meta EE.UU. $1.11 | Meta EE.UU. $2.69 | Meta México $0.35 | Meta México $0.80 |
|---|---|---|---|---|---|---|
| $19 | $17.55 | $8.78 | 42.2% | 102.2% | 13.3% | 30.4% |
| $29 | $27.05 | $13.52 | 27.4% | 66.3% | 8.6% | 19.7% |
| $39 | $36.55 | $18.27 | 20.2% | 49.1% | 6.4% | 14.6% |
| $49 | $46.05 | $23.02 | 16.1% | 38.9% | 5.1% | 11.6% |

Cómo leerla:
- Con anuncios en EE.UU., un precio de $19–$29 exige tasas de intención de 27% a más de 100%: **no es alcanzable**. A $39–$49 baja a 16–49%, que sigue siendo muy exigente.
- Con costos de México la exigencia baja a 5–30%, pero que el clic sea barato **no significa que la audiencia pague** esos precios.
- Un precio más alto relaja la exigencia: por eso las pruebas incluyen $39 y $49 en las herramientas profesionales.

## Presupuesto orientativo de anuncios

Para decidir con el mínimo de 300 visitas por precio probado:

| Mercado (costo por clic de blogs) | 300 visitas | 4 candidatos, un precio cada uno |
|---|---|---|
| Meta EE.UU. ($1.11–$2.69) | $333–$807 | $1,332–$3,228 |
| Meta México ($0.35–$0.80) | $105–$240 | $420–$960 |

Probar tres precios por separado triplica esas cifras; repartir el tráfico entre precios abarata la prueba pero le quita potencia estadística. **El presupuesto es decisión tuya.** Hay rutas sin pago (comunidades de cada oficio, SEO de cola larga, afiliados con el 30–50% de comisión), sin garantía de resultados.

## Por candidato

### 1. `steps-recorder-successor-local` (Windows)
- **Público:** soporte técnico, formadores y quien documenta procesos internos en Windows.
- **Precios a probar:** $19, $29, $39.
- **Palabras clave semilla (a medir, no son datos):** *steps recorder windows 11 alternative*, *psr.exe removed windows 11*, *record steps screenshots windows*, *document process screenshots tool*, *how to create step by step guide windows*, *grabador de pasos windows 11*, *alternativa grabadora de acciones windows*, *crear manual paso a paso capturas*.
- **Mensaje honesto:** "Graba tus clics y obtén una guía paso a paso con capturas. Todo ocurre en tu PC: sin nube y sin suscripción."
- **No prometer:** compatibilidad con todos los antivirus.
- **Riesgo:** los ganchos de teclado y ratón pueden activar alertas, y exige firma de código. Hay que revisar si las plataformas de anuncios restringen "software de grabación de pantalla" (no verificado).

### 2. `audio-anonimizador-entrevistas` (Windows y Mac)
- **Público:** investigadores cualitativos, tesistas, periodistas, recursos humanos.
- **Precios a probar:** $29, $39, $49.
- **Palabras clave semilla:** *anonymize interview audio*, *redact names from audio recording*, *bleep names in audio*, *audio redaction software*, *anonymise interview recordings research*, *anonimizar entrevistas audio*, *tapar nombres en audio*, *anonimizar grabaciones investigación cualitativa*.
- **Mensaje honesto:** "Propone qué tramos tapar y tú apruebas cada uno. El audio no sale de tu equipo."
- **No prometer:** anonimato total. La voz sigue siendo identificable y la detección de nombres es parcial (F1 de 0.77 en un prototipo).
- **Riesgo:** no existe comparable a precio de consumidor.

### 3. `extractos-bancarios-local-csv` (Windows y Mac)
- **Público:** contadores y tenedores de libros con varios clientes, autónomos.
- **Precios a probar:** $29, $49, $79.
- **Palabras clave semilla:** *bank statement pdf to csv*, *convert bank statement to excel*, *scanned bank statement to excel*, *bank statement converter offline*, *extractos bancarios pdf a excel*, *convertir estado de cuenta pdf a excel*, *estado de cuenta bancario a csv*, *convertir estado de cuenta escaneado*.
- **Mensaje honesto:** "Convierte tus extractos a Excel y comprueba que los importes cuadran con el saldo. Todo local."
- **No prometer:** compatibilidad con un banco concreto hasta tener su perfil, ni exactitud perfecta.
- **Riesgo:** un perfil por banco; un error en un importe es crítico; mercado saturado.

### 4. `scanned-photo-splitter-robust` (Windows y Mac)
- **Público:** familias que digitalizan álbumes, aficionados a la genealogía, fotógrafos aficionados.
- **Precios a probar:** $19, $29, $39.
- **Palabras clave semilla:** *split scanned photos*, *scan multiple photos at once separate*, *crop multiple photos from scan*, *auto crop scanned photos*, *photo scanning batch crop software*, *separar fotos escaneadas*, *recortar varias fotos escaneadas*, *dividir fotos escaneadas automáticamente*.
- **Mensaje honesto:** "Escanea varias fotos de una vez y sepáralas, aunque estén casi pegadas. Se procesan en tu equipo."
- **No prometer:** acierto en cualquier escaneo; hay que medir la precisión con escaneos reales antes de construir.
- **Riesgo:** ScanSpeeder ya existe con prueba gratuita.

## Qué falta antes del primer anuncio

- Cuenta publicitaria, presupuesto, dominio, página y analítica.
- Aviso de privacidad y términos de la página, revisados por un abogado.
- Las políticas de cada plataforma de anuncios para estas categorías (no verificadas).
- Para la lista de espera **no hace falta** comerciante de registro: basta un formulario de correo.
