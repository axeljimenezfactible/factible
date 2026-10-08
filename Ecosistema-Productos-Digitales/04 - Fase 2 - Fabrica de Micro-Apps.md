---
tags: [proyecto, productos-digitales, fase-2]
creado: 2026-10-08
estado: en-curso
---

# Fase 2 — Arquitectura del producto (Fábrica de Micro-Apps)

Volver al [[00 - Indice]] · Anterior: [[03 - Fase 1 - Global Trend Engine]] · Siguiente: [[05 - Fase 3 - Motor de Creacion]] · Qué te toca a ti: [[07 - Guia - Que debes hacer tu]]

## Objetivo (del brief)
- Con los datos de la Fase 1, diseñar la estructura lógica de los productos: herramientas de alta utilidad que automaticen tareas diarias, resuelvan cuellos de botella profesionales o simplifiquen procesos complejos.
- Diseño **modular**, para que la producción se automatice casi por completo.

> [!warning] Estado y límites
> Es un **diseño y un esqueleto ejecutable**, no apps construidas. Los costos y licencias salen de tres rondas de agentes con **búsqueda web únicamente**: nadie abrió páginas oficiales ni archivos LICENSE. La confianza máxima es media. Lo que decide el país o el tipo de entidad del vendedor está marcado como **abierto**.

## Qué cambia en el diseño por lo que enseñó la Fase 1

1. **Portafolio, no producto estrella.** El mejor caso de tracción visto vende unas 57.5K unidades (MacWhisper, autodeclarado, 2023, sin verificar). Si el camino es un portafolio, el costo marginal de cada app es la variable decisiva.
2. **Todo local es el argumento de venta.** Las cuatro candidatas de confianza media procesan archivos del usuario sin subirlos. El diseño lo impone, no lo promete.
3. **Resultados parciales exigen revisión humana.** OCR, detección de nombres y transcripción fallan en parte. Una app que los use debe mostrar el resultado al usuario antes de guardar, y no prometer anonimato ni exactitud.
4. **Windows y macOS, de $19 a $49, licencia perpetua con 12 meses de actualizaciones.** Es el patrón que cobran las herramientas que más ingresan.
5. **El pago único cuesta mantenimiento.** MacUpdater cerró en enero de 2026 por no sostenerlo. Cada dependencia y cada formato soportado es un costo futuro.

## Arquitectura en cuatro capas

```
Receta de la app        ← especificación JSON: lo único que cambia por producto
Módulos de capacidad    ← compartidos entre apps (regla de dos)
Núcleo (core.*)         ← cascarón, licencias, actualizaciones, guardia de privacidad
Plataforma de publicador← firma, cuentas, comerciante de registro, hospedaje, sitio (una vez)
```

- **Receta.** Declara módulos, plataformas, precio, flujo, pruebas de oro, riesgos y la prueba de puerta falsa. El validador (`micro-app-factory/spec.py`) rechaza recetas que incumplen las reglas.
- **Módulos.** Un módulo nuevo solo se promueve a compartido cuando lo usan **dos o más apps**; antes, es código de una sola app.
- **Núcleo.** Implícito en toda app. `core.privacy_guard` limita la red a licencia, actualización y telemetría opcional, y se prueba en modo avión.
- **Plataforma de publicador.** La firma, las cuentas y el comerciante de registro son **por publicador, no por app**: su costo se reparte entre todo el portafolio.

### Reglas que aplica el validador
Núcleo implícito · módulos del catálogo que cubran las plataformas · procesar todo en local · módulos de resultado parcial implican `review_required` y `review.ui` · al menos 3 pasos de flujo, 3 pruebas de oro y un riesgo · prueba de puerta falsa con precios · precio hasta $200.

## Catálogo de módulos y uso en las 6 recetas de ejemplo

18 módulos de capacidad más 4 del núcleo. Las 6 recetas (4 de confianza media, 2 de baja) las escogí yo: el conteo orienta el orden de construcción, **no es un resultado de mercado**.

| Uso | Módulos |
|---|---|
| 6 de 6 | `export.formats`, `io.files` |
| 5 de 6 | `batch.queue` |
| 4 de 6 | `review.ui` |
| 3 de 6 | `doc.pdf` |
| 2 de 6 | `meta.docs`, `rules.engine`, `vision.ocr` |
| 1 de 6 (específicos) | `ai.ner_local`, `ai.transcribe_local`, `audio.io`, `capture.input_win`, `data.tables`, `io.watch_folder`, `mail.parse`, `vision.contours`, `vision.redact` |
| 0 de 6 | `ai.llm_byok` |

## Decisiones tomadas y abiertas

### 1. Cascarón y motor
- **Por defecto:** Tauri 2 con el motor de procesamiento en Python como proceso auxiliar, empaquetado con PyInstaller en modo carpeta y firmado. La documentación oficial de Tauri cita PyInstaller para ese patrón. Los blogs reportan instaladores de 8–18 MB frente a 200–290 MB de Electron (no son pruebas de rendimiento controladas).
- **Alternativas:** Electron si solo se domina JavaScript (instaladores mucho mayores); PySide6 si todo es Python (LGPL: enlace dinámico y aviso). Flutter y Avalonia/.NET quedaron sin datos suficientes.
- **Abierto:** qué marco genera y mantiene mejor una IA no está verificado con ninguna fuente; es juicio mío.

### 2. Licencias de componentes (para vender software cerrado)

| Área | Usar | Evitar |
|---|---|---|
| PDF | pypdf (BSD-3), pdfplumber (MIT), pypdfium2 | **PyMuPDF**: AGPL o licencia comercial de pago sin precio público |
| OCR | Tesseract (Apache 2.0), RapidOCR/PaddleOCR (Apache-2.0) | — (verificar licencia de los datos de idioma) |
| Audio | FFmpeg LGPL con enlace dinámico; faster-whisper (MIT) | Compilaciones de FFmpeg con `--enable-gpl` o `--enable-nonfree` |
| Nombres | GLiNER con pesos Apache-2.0 (`gliner_multi-v2.1`) | `gliner_multi` (CC BY-NC 4.0); modelos `es_core_news_*` de spaCy (GPL-3.0) |
| Modelo de lenguaje | Phi-3.5 mini (MIT), Qwen3-4B y Qwen2.5-1.5B (Apache-2.0) | Qwen2.5-3B (Qwen Research License); Llama y Gemma tienen términos propios |
| Correo | biblioteca estándar para `.eml` | **extract-msg** (GPL v3) para `.msg` |
| Visión | OpenCV 4.5 o posterior (Apache 2) | **Ultralytics YOLO** (AGPL o comercial) |
| Metadatos | ExifTool como proceso aparte; Pillow, python-docx, openpyxl | — |
| Empaquetado | PyInstaller (GPL con excepción del bootloader, permite distribución cerrada) | — |

Casi ninguna licencia viene del archivo LICENSE ni de la ficha oficial, sino de PyPI, agregadores y blogs. **Hay que revisarlas antes de distribuir.** Las notas por módulo están en `micro-app-factory/catalog.json`.

### 3. Firma y distribución (costos por publicador)

| Concepto | Costo | Requisitos y notas |
|---|---|---|
| Apple Developer Program | $99/año | Persona física: sin D-U-N-S, y su nombre legal queda como publicador. Organización: entidad legal (no unipersonal) con D-U-N-S y dominio propio; 2–4 semanas según un foro y más de 2 meses reportado en 2026. La notarización no tiene cargo aparte (no confirmado explícitamente) |
| Actualizador macOS (Sparkle 2) | $0 | Licencia no verificada |
| Windows: Microsoft Artifact Signing, plan Basic | $9.99/mes (≈ $120/año) | **Desde México no es viable** (ni persona física ni moral). Organizaciones en 12 regiones listadas (EE.UU., Canadá, UE, Reino Unido, Australia, Nueva Zelanda, Japón, Corea del Sur, Singapur, Suiza, Noruega, Israel). Individuos solo en EE.UU. y Canadá. **México y Colombia no aparecen.** Un resultado sin fuente dice que el alta de individuos estaba pausada en marzo de 2026; hay reportes de validaciones atascadas más de un mes, y un autónomo no constituido de Irlanda no calificó (Microsoft Q&A). Las versiones anteriores de la documentación listaban menos regiones. Si no eres elegible, la ruta que queda es la Microsoft Store con MSIX (la firma Microsoft) |
| Windows: alternativa de certificado OV | ~$116/año a 3 años (Certum vía revendedor, blog); Sectigo OV $220–450/año | EV $290–650/año, y ya no da reputación SmartScreen inmediata. Llaves en hardware o nube desde junio de 2023; validez máxima ~460 días. No se confirmó si validan individuos fuera de EE.UU. y la UE |
| Microsoft Store | Cuenta individual gratis; MSIX lo firma Microsoft | Comisión 0% con comercio propio (apps que no son juegos) o 15%. Cuenta de empresa: $0 según un blog de mayo de 2026 y $99 según Learn (conflicto) |
| Hospedaje de instaladores | $0–5/año | Cloudflare R2: $0.015/GB-mes y descargas gratis. GitHub Releases: gratis con repo público |
| **Total mínimo** | **≈ $220/año** | Apple individual + Artifact Signing Basic (o certificado Certum). Suma del agente; no incluye comisiones de tienda ni de pagos |

**El vendedor está en México** (persona física al principio, persona moral después; ya hay una persona moral disponible): ver la sección 6. **Abierto:** si empezar como persona física o directamente con la persona moral.

### 4. Cobro y licencias

| Plataforma | Tarifa | Claves de licencia | Precios por país | Notas |
|---|---|---|---|---|
| Polar | 5% + $0.50 (plan gratis, desde el 27-may-2026; cuentas anteriores 4% + $0.40) | Nativas, con límite de activaciones; activar y validar sin clave de API del vendedor | No nativo | Cobra vía Stripe Connect; lista de países de pago no verificada completa |
| Lemon Squeezy | 5% + $0.50 (según blogs) | Sí, con API | No nativo | Pagos bancarios confirmados a Argentina, Chile y Colombia; México y España no confirmados. Es de Stripe; sin cierre anunciado oficialmente, pero blogs reportan ritmo lento |
| Creem | 3.9% + $0.40 (oficial) | Complemento "License Keys" | No nativo | Lista pagos a México y Colombia. Validación sin conexión no documentada |
| Paddle | 5% + $0.50 (publicado) | No trae licencias propias | **Sí, nativo** (precios por país) | Su política de uso aceptable restringe VPN y limpiadores de sistema |
| Gumroad | 10% + $0.50 | Sí | Sí, nativo | La tarifa más alta |
| Stripe Managed Payments | Tarifas estándar + 3.5% (ayuda oficial) | No | — | En vista previa; las fuentes discrepan sobre su estado |

- **Neto por venta de $20** (aritmética mía, sin recargos internacionales ni de PayPal): $18.50 con 5% + $0.50 y $18.82 con 3.9% + $0.40.
- **Ninguna plataforma confirma** que acepte grabación de pantalla, anonimización, conversión de extractos bancarios ni herramientas fiscales: ninguna lista recuperada las menciona. **Hay que escribir a su soporte antes de construir cada producto.**
- **La capa de licencias va detrás de un adaptador.** Dado el riesgo de plataforma (Lemon Squeezy dentro de Stripe, tarifas que cambian), `core.license` debe poder cambiar de comerciante sin tocar las apps.
- **Abierto:** cuál elegir depende del país del vendedor y de la respuesta de cada soporte.

### 5. Licencia "perpetua con 12 meses de actualizaciones"

**Qué es, en sencillo.** La persona paga una vez (por ejemplo $29). La app es suya para siempre: nunca se apaga ni deja de funcionar. Durante los primeros 12 meses recibe todas las versiones nuevas. Pasado ese año sigue usando la versión que tiene, pero para recibir versiones nuevas renueva por un precio menor (el patrón visto es ~60% del precio, unos $17) o compra la versión siguiente.

**Por qué este modelo y no otro.**
- *Pago único puro:* es lo más simple y encaja con el "ticket de $20", pero no financia el mantenimiento. Los formatos de bancos, de Office y de los sistemas operativos cambian, y MacUpdater cerró en enero de 2026 por no sostener el pago único.
- *Suscripción:* financia el mantenimiento, pero "sin suscripción" es el argumento de venta de estas herramientas y la queja más repetida contra las alternativas.
- *Perpetua con 12 meses:* es el patrón que cobran las herramientas que más ingresan (CleanShot X $29 con un año de actualizaciones, renovación a $19; Xnapper y DevUtils $29 con renovación al 60%).

**Lo que no sabemos.** Cuántos clientes renuevan: no hay ninguna tasa de renovación en la investigación. Por eso no se debe contar con ese ingreso en los números.

**Cómo funciona por dentro.** La clave de licencia no caduca. Guarda una "fecha de actualizaciones hasta". Cada versión de la app tiene su fecha de compilación. La app instala una versión nueva solo si su fecha de compilación es anterior a la fecha de actualizaciones del cliente; la versión que ya tiene sigue corriendo siempre. Renovar mueve esa fecha un año.

**Cómo se ofrece, para evitar reembolsos.** El patrón de reembolso más repetido es el "cobro distinto al anunciado". La oferta debe decir en la página de compra, en una frase, qué incluye ("pago único, 12 meses de actualizaciones incluidos, sin suscripción") y ofrecer una garantía de 30 días.

**Propuesta.** Anunciar así en las pruebas de puerta falsa y decidir el precio de la renovación con datos reales, no antes.

**Ninguna plataforma lo documenta de forma nativa.** Se construye con lógica propia en `core.license`: la clave es perpetua, y un token firmado guarda la fecha hasta la que la persona recibe versiones nuevas; la app compara esa fecha con la de su compilación. La renovación (a ~60% del precio, según el patrón visto) es un producto aparte. La validación sin conexión tampoco está documentada: se usa un token firmado y guardado en el equipo, con un periodo de gracia.

### 6. Vendedor en México: persona física primero, persona moral después

Tres rondas más de agentes, con búsqueda web únicamente. Detalle en `micro-app-factory/data/fase2_mx_firma.json`, `fase2_mx_cobro.json` y `fase2_mx_apple.json`.

**Apple (macOS)**

| Vía | Qué exige | Plazo reportado | Notas |
|---|---|---|---|
| Persona física (individuo) | $99/año con renovación automática (el monto en MXN y el IVA no salen en ninguna fuente). Verificación con foto del documento desde la app Apple Developer. La licencia de conducir no se acepta en México; el pasaporte es lo seguro (del INE no hay fuente) | De unos días a 2–7 semanas o más, según foros de 2026 | Su nombre legal queda como vendedor |
| Persona moral (organización) | Entidad legal, número D-U-N-S (gratis), dominio con sitio activo y correo del dominio, y autoridad de firma | El D-U-N-S tarda hasta 5 días hábiles más 2 según Apple y hasta 30 días hábiles según D&B. Los foros reportan 2 meses o más de 100 días, y rechazos sin motivo | Sin confirmación de que acepte S.A.S. o S. de R.L. |
| Pasar de individuo a organización | Proceso oficial para actualizar el mismo equipo, sin abrir otra cuenta. Hay que ser fundador, tener D-U-N-S y documentos | Relatos de 2026 de 17 días a 3 meses, con beneficios deshabilitados y actualizaciones bloqueadas mientras tanto | El Team ID no cambia. Las apps ya firmadas siguen funcionando. No hay transferencia soportada de apps que solo usan Developer ID. La rotación de claves de Sparkle se liga a una firma Apple coincidente: su independencia no está confirmada |

Ninguna fuente aconseja explícitamente empezar como organización. Una guía de terceros lo sugiere si la empresa se constituirá pronto; un ingeniero de Apple confirma en el foro que empezar como individuo y actualizar después es una vía soportada.

**Windows**

| Vía | Persona física | Persona moral |
|---|---|---|
| Artifact Signing (Microsoft) | No viable | No viable. Solo con una entidad en una región elegible (≈ $120/año) |
| Certificado de una autoridad certificadora | SSL.com IV $249 más eSigner $180/año (≈ $429; la duración del precio no se confirmó), Certum Standard Cloud €109–189/año, o Sectigo IV por revendedor ≈ $220/año con token físico | OV desde ≈ $129 hasta ≈ $440/año según autoridad y revendedor; Microsoft cita $150–300 |
| Microsoft Store con MSIX | Microsoft firma el paquete: sin certificado propio y sin SmartScreen. Registro $0 (individuos desde septiembre de 2025). Solo cubre distribución dentro de la Store | Igual, registro $0 desde mayo de 2026 |

- **Comisión de la Store:** con comercio propio no hay comisión en apps que no son juegos; con la plataforma de Microsoft es 15%. No se verificó si la Store permite vender licencias propias.
- **Cambio de física a moral:** probablemente reinicia la reputación de SmartScreen (la documentación oficial solo habla de reputación por archivo). El nombre mostrado pasa del nombre propio a la razón social. Mover apps entre cuentas de la Store solo se logra con un ticket de soporte.
- **Sin verificar:** qué documentos aceptan las autoridades a mexicanos, si envían tokens a México y la retención del W-8BEN en la Store (el 10% con tratado viene solo de fuentes no oficiales).

**Cobro**

| Plataforma | ¿Paga a México? | Notas |
|---|---|---|
| Creem | **Sí**: México aparece en su lista oficial de pagos bancarios locales | Falta confirmar si acepta persona física, en qué moneda llega y la tarifa real del pago (las fuentes dicen "USD 7 o 1%" frente a "sin cargo adicional"). Prohíbe software de vigilancia y servicios regulados de banca o finanzas |
| Polar | Sin confirmar | Paga vía Stripe Connect Express, con KYC por INE o pasaporte y revisión previa al primer pago de hasta 14 días |
| Paddle | Sin confirmar | Acepta individuos sin verificación de negocio. Pago por transferencia, probablemente en USD, mínimo $100; comisión SWIFT de $15 por confirmar |
| Lemon Squeezy | Banco sin confirmar | PayPal en más de 200 países (3% con tope de $30 por pago). Prohíbe software de vigilancia y servicios regulados de banca o finanzas. Fuentes de terceros reportan cuentas congeladas o rechazadas |
| Gumroad | Sin confirmar | México probablemente con depósito bancario (según Wise, no oficial); mínimo de $100 reportado |
| Stripe México directo (no es comerciante de registro) | **Sí**, persona física con actividad empresarial y persona moral | RFC y una CLABE en pesos. El vendedor asume los impuestos y el cumplimiento internacional |
| Stripe Managed Payments | **No**: México no está entre las ubicaciones soportadas | |

- Ninguna plataforma documenta el cambio de persona física a moral.
- **Para tu contador:** qué documento fiscal (factura, CFDI o formulario W-8BEN) pide cada comerciante, si cuenta como cliente extranjero y cómo se trata el cambio de persona física a moral. Las fuentes no dicen nada de esto.

**Lo que esto sugiere** (inferencias mías, sin verificar con un contador):
1. **Nada de esto bloquea** la prueba de demanda ni la lista de espera.
2. **Los plazos largos** están en Apple: la organización tarda 2 meses o más y la conversión de individuo a organización, hasta 3 meses con actualizaciones bloqueadas. Si se va a usar la persona moral que ya existe, empezar directamente como organización evita la conversión, y su espera puede correr en paralelo a las pruebas de demanda. Si no, el individuo con pasaporte es la vía más rápida y se actualiza después.
3. **Windows:** los rangos de costo de persona física y moral se traslapan, así que ser persona moral no es claramente más barato. Lo que sí evita es el reinicio de la reputación y el cambio del nombre del publicador. **No comprar certificado hasta que un candidato pase la prueba de puerta falsa:** las compilaciones de prueba pueden ir sin firmar.
4. **Cobro:** solo Creem tiene México en una lista oficial. Hay que preguntar por escrito a varias plataformas (ver [[09 - Preguntas para los comerciantes de registro]]), sobre todo por la categoría: "software de vigilancia" podría afectar a la grabadora de pasos, y "servicios regulados de banca o finanzas" podría rozar a la conversión de extractos bancarios.

## Economía por app

- **Neto por venta:** $18.50–$18.82 (sección 4), menos reembolsos (5–8%, supuesto mío) y costo variable.
- **Costo fijo del publicador:** ≥ $220/año, repartido entre las N apps.
- **Ventas necesarias para recuperar una app** = (costo de construirla + mantenimiento anual + su parte del costo del publicador) ÷ [neto × (1 − reembolsos) − costo variable].
- Los costos de construir y mantener dependen del motor de la Fase 3; no los invento. Meta de diseño: que una receta nueva cueste casi nada de construir una vez que existan el núcleo y los módulos compartidos.

## Orden de construcción propuesto

1. **Núcleo y plataforma de publicador:** `core.shell`, `core.license` con adaptador, `core.update`, `core.privacy_guard`, y el proceso de firma y empaquetado. No depende del producto, pero conviene empezarlo cuando ya haya cuenta de publicador y comerciante elegido.
2. **Compartidos por 4 o más recetas:** `io.files`, `export.formats`, `batch.queue`, `review.ui`.
3. **Por demanda:** `doc.pdf`, `vision.ocr`, `rules.engine`, `meta.docs`.
4. **Específicos** del primer producto que pase la puerta falsa.

**No construir las etapas 2 a 4 antes de que un candidato pase la prueba de puerta falsa.** Se generaliza un módulo cuando lo pide la segunda app.

## Riesgos y lo que falta verificar

- **Identidad y país:** firma de Windows y ruta de Apple dependen de ellos.
- **Categorías de producto:** ninguna plataforma de cobro confirma aceptar las categorías sensibles.
- **Antivirus:** los ganchos de bajo nivel de `capture.input_win` pueden activar alertas, y no se verificó cómo puntúan los EDR a UI Automation ni a Windows Graphics Capture.
- **Licencias de componentes:** nada leído del archivo LICENSE; hay riesgos AGPL, GPL y de pesos no comerciales (sección 2).
- **Mantenimiento perpetuo:** el pago único no financia las actualizaciones por formato; el límite de 12 meses es parte de la mitigación.
- **Calidad de la evidencia:** resúmenes de búsqueda. Sin verificar: plazos de validación de identidad, precios oficiales de las autoridades certificadoras, validación sin conexión de licencias, tamaños y rendimiento en laptop sin GPU, y si el 15% de la Mac App Store sigue vigente en 2026.

## Archivos
- `micro-app-factory/`: `README.md`, `catalog.json`, `spec.py`, `specs/` (6 recetas), `tests/` (18 pruebas)
- Investigación: `micro-app-factory/data/fase2_firma.json`, `fase2_cobro.json`, `fase2_pila.json`

## Siguiente
- Decidir si se empieza como persona física o directamente con la persona moral (sección 6), con tu contador.
- Enviar las preguntas de [[09 - Preguntas para los comerciantes de registro]] a las plataformas de cobro.
- Fase 3: el motor que convierte una receta en una app (generación de código, pruebas de oro, compilación firmada).
