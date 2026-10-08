---
tags: [proyecto, productos-digitales, guia]
creado: 2026-10-08
estado: vigente
---

# Guía: qué debes hacer tú

Volver al [[00 - Indice]] · Contexto: [[03 - Fase 1 - Global Trend Engine]] · [[04 - Fase 2 - Fabrica de Micro-Apps]]

> [!warning] Regla de oro
> **Nunca pegues claves ni contraseñas en el chat ni en archivos del repo.** Se guardan en la configuración del entorno, y una sesión nueva las toma.

## Resumen

| # | Qué | Tiempo | Costo | Para qué |
|---|---|---|---|---|
| 1 | Abrir la red del entorno | 5 min | $0 | Que yo pueda consultar Hacker News, Stack Exchange, Google Trends y DataForSEO |
| 2 | Crear la cuenta de DataForSEO y cargar saldo | 15 min | mínimo $50 | Volúmenes de búsqueda y costo por clic reales |
| 3 | Guardar las credenciales en el entorno | 5 min | $0 | Que yo las lea sin que pasen por el chat |
| 4 | Abrir una sesión nueva sobre la misma rama | 2 min | $0 | Una sesión nueva es la que toma los cambios de red y credenciales |
| 5 | Opcional: pedir acceso a la API de Google Trends | 10 min | $0 | Series de tendencia oficiales; no bloquea nada |

Los pasos 1 a 4 son lo único necesario para medir la demanda real de los candidatos.

## Paso 1: abrir la red

**Qué es.** Cada sesión en la nube corre en un "entorno" con un cortafuegos de lista blanca. Por defecto el nivel de acceso es **Limited**: solo deja pasar dominios de una lista (servicios de Anthropic, GitHub, GitLab, registros de contenedores y gestores de paquetes). Los cuatro dominios que necesito están fuera de esa lista; por eso recibí un error 403 al intentar usarlos. Lo que hay que hacer es **añadirlos a la lista de dominios permitidos** del entorno.

**Dónde está.** Hay dos caminos y llevan al mismo cuadro de diálogo:
- **Camino A (desde esta sesión):** en la barra del título de la sesión, pulsa el nombre del **entorno en la nube** y elige **Edit**.
- **Camino B (desde la web):** entra a claude.ai/code, abre el selector de entornos, pasa el ratón sobre tu entorno y pulsa el **icono de ajustes** que aparece a la derecha.

**Qué verás.** Un cuadro con el nombre del entorno, el **nivel de acceso a la red**, las variables de entorno y un script de configuración. Las etiquetas pueden variar un poco según la versión de la app.

**Qué hacer, paso a paso.**
1. En **Network access** deja el nivel en **Limited**. En las versiones de la app sin actualizar, esa misma opción aparece como **Custom**.
2. Busca el campo **Allowed domains** (dominios permitidos).
3. Añade estos cuatro dominios, solo el nombre y sin `https://`. Si el campo muestra un ejemplo de formato, sigue ese (normalmente uno por línea):
   - `hn.algolia.com` (Hacker News)
   - `api.stackexchange.com` (Stack Exchange)
   - `trends.google.com` (Google Trends)
   - `api.dataforseo.com` (DataForSEO; confirma este nombre en la documentación de DataForSEO)
4. Deja **marcada** la casilla que incluye la lista predeterminada de gestores de paquetes (**Allow package managers**), para que no se rompan las instalaciones.
5. Guarda.

**Cómo comprobar que quedó.** Los cambios los toma una **sesión nueva** (paso 4). En ella te pediré que pruebe cada dominio; si responde, está bien.

**Por qué no abrir todo.** Existe la opción de un nivel de acceso más amplio que la lista blanca. Mi recomendación, que es una buena práctica y no algo que diga la documentación: no la uses. Una sesión con acceso libre a internet, que además tendrá tus credenciales de DataForSEO, tiene más superficie si alguien logra colar instrucciones en una página que se lea. La lista de cuatro dominios es suficiente.

**Casos especiales.**
- **No añadas Reddit.** Sus términos restringen este uso de los datos.
- **Si no ves la opción o está bloqueada,** la política la fija el administrador de tu organización. Envíale este mensaje: *"Por favor permitan estos dominios en el entorno en la nube de Claude Code para el proyecto: hn.algolia.com, api.stackexchange.com, trends.google.com y api.dataforseo.com. Son APIs públicas de consulta."*
- **`WebFetch`** (la herramienta que abre páginas) falla por DNS desde el principio. No sé si este cambio lo arregla.
- **Si algo no coincide con lo que ves,** dime qué opciones aparecen en el cuadro y te guío con tu pantalla.

La guía oficial está en https://code.claude.com/docs/en/cloud-environments#network-access.

## Paso 2: crear la cuenta de DataForSEO

1. Regístrate en dataforseo.com con el correo que quieras usar como **API login**.
2. Verifica el correo y entra al **Dashboard**.
3. Carga saldo con **Add Funds**. Según su centro de ayuda y comparativas de terceros, el mínimo es **$50**, los pagos pasan por FastSpring y el saldo no caduca. Hay un crédito de prueba pequeño (~$1; las fuentes discrepan). **Confirma estas cifras en su sitio antes de pagar.**
4. En el menú de la izquierda abre **API Access**. Ahí están:
   - tu **API login**: el correo con el que te registraste;
   - tu **API password**: **no es la contraseña del Dashboard**. Se muestra completa solo las primeras 24 horas; después puedes pedir **Send by e-mail** para recibirla.

Cuánto vamos a gastar: la consulta de volúmenes de Google Ads acepta hasta 1,000 palabras por petición. La página de DataForSEO cita $60 por millón de palabras en cola estándar. Para ~31 candidatos con ~20 palabras cada uno son ~620 palabras, es decir **centavos**. El mínimo de $50 alcanza para meses. El precio exacto de la consulta "en vivo" no lo pude confirmar: la cuenta muestra el gasto, y DataForSEO tiene un sandbox gratuito para probar.

## Paso 3: guardar las credenciales

1. Vuelve al **menú del entorno → Edit**.
2. Si ves la sección **Network secrets** (en apps sin actualizar se llama **API credentials**), añade ahí las dos. Si no existe, usa **variables de entorno**.
3. Usa estos nombres exactos:
   - `DATAFORSEO_LOGIN` = tu API login (el correo)
   - `DATAFORSEO_PASSWORD` = tu API password
4. Si alguna vez se filtra, regenera la contraseña de API en el Dashboard.

## Paso 4: sesión nueva

Esta sesión no verá los cambios. Abre una **sesión nueva** con ese entorno sobre:
- repositorio: `axeljimenezfactible/factible`
- rama: `claude/digital-products-ecosystem-1fhahn` (es el PR #1)

Primer mensaje sugerido, para copiar y pegar:

> Continúa el proyecto desde `Ecosistema-Productos-Digitales/00 - Indice.md` y las notas 03 y 04. Ya configuré la red y las variables `DATAFORSEO_LOGIN` y `DATAFORSEO_PASSWORD`. Comprueba que llegas a `api.dataforseo.com` y empieza a medir volúmenes y costo por clic de los candidatos de la pasada 3.

Todo el trabajo está en el repo y en Drive, así que no se pierde nada al cambiar de sesión.

## Paso 5 (opcional): API de Google Trends

Se pide en https://developers.google.com/search/apis/trends. Es por solicitud y sin garantía de aprobación. No bloquea nada.

## Qué haré yo cuando lo tengas

1. Probar la conexión en el sandbox gratuito de DataForSEO.
2. Escribir y probar contra la API real los colectores que aún no existen (DataForSEO, Hacker News, Stack Exchange).
3. Medir volúmenes y costo por clic de los 22 sobrevivientes de la pasada 3 y los 9 "rehacer" de la pasada 2, y volver a puntuar con demanda real.
4. Calcular con `faketest.py` el costo por clic máximo que soporta cada candidato para mantener el CAC en $9 o menos.

## Lo que NO necesitas hacer todavía

- Cuenta publicitaria, presupuesto de anuncios, dominio y cuenta de cobro: se necesitan para las pruebas de puerta falsa y los pido **después** de medir volúmenes, para no gastar en nichos sin demanda.
- Apify, Semrush y créditos de API de LLM de la Fase 0: no hacen falta ahora.

## Cuentas que prepararás más adelante

No son para ahora, salvo lo que tiene plazos largos (ver abajo). Detalle y fuentes en [[04 - Fase 2 - Fabrica de Micro-Apps]]; todas las cifras salen de búsqueda web y hay que confirmarlas en las páginas oficiales.

| Cuenta | Costo | Qué exige | Plazo |
|---|---|---|---|
| Apple Developer Program (firmar apps de Mac) | $99/año | Persona física: sin D-U-N-S, y su nombre legal queda como publicador. Organización: entidad legal (no unipersonal), D-U-N-S y dominio propio | Organización: 2–4 semanas según un foro; más de 2 meses reportado en 2026 |
| Firma de apps de Windows | ≈ $120/año (Microsoft Artifact Signing, plan Basic) o ≈ $116–450/año (certificado OV) | Artifact Signing: organizaciones en 12 regiones listadas; individuos solo en EE.UU. y Canadá; **México y Colombia no aparecen** | No verificado |
| Comerciante de registro (cobro, impuestos, claves de licencia) | Entre 3.9% + $0.40 y 10% + $0.50 por venta | Depende del país del vendedor; **ninguna confirma aceptar** grabación de pantalla, anonimización, extractos bancarios ni herramientas fiscales | No verificado |
| Hospedaje de instaladores | $0–5/año | Cuenta en Cloudflare (R2) o GitHub | Inmediato |
| Dominio | Variable | Lo exige Apple para cuentas de organización; también sirve para la página de venta | Inmediato |

**Lo que sí conviene adelantar si vas a vender como empresa:** el número D-U-N-S y la inscripción de organización en Apple tardan semanas o meses. Antes necesito saber tu país y si cobrarás como persona o como empresa (ver abajo).

**Antes de construir cada producto,** hay que preguntar por escrito al soporte de 2 o 3 comerciantes de registro si aceptan su categoría. Eso lo preparo yo; tú solo necesitarás enviarlo desde tu cuenta.

## Decisiones

1. ✅ **País y tipo de vendedor:** México. Persona física al principio y persona moral después; ya hay una persona moral disponible. Se está verificando qué implica para la firma de Windows, el cobro y Apple (ver [[04 - Fase 2 - Fabrica de Micro-Apps]]).
2. ⏳ **Modelo de licencia** "perpetua con 12 meses de actualizaciones y renovación opcional": explicado en la sección 5 de la nota 04. Falta tu decisión.
3. ✅ **Qué probar primero:** los 4 candidatos de confianza media de la pasada 3. El plan está en [[08 - Plan de prueba de los 4 candidatos]].
4. ⏳ **Presupuesto de anuncios** para las pruebas de puerta falsa: cuando llegue el momento. El plan de prueba trae cifras orientativas.
