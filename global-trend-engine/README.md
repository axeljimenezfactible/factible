# Global Trend Engine (Fase 1)

Herramientas de la Fase 1 del proyecto de micro-apps a $20 USD. Solo biblioteca estándar de Python 3; sin dependencias.

| Archivo | Para qué |
|---|---|
| `score.py` | Puntúa y ordena candidatos de nicho (JSON) con una media geométrica ponderada, penaliza las alternativas gratuitas (hasta 25%) y marca huecos de datos |
| `data/` | Evidencia cruda de los agentes (`fase1_*.json`), rankings (`ranking_v0.csv` antes de la penalización, `ranking.csv` actual) y la pasada 2 (`fase1b_*.json`, `verificacion_pasada2.csv`) |
| `faketest.py` | Decide GO / DESCARTAR / CONTINUAR en una prueba de puerta falsa (Beta-Binomial) |
| `tests/` | Pruebas unitarias. Sus candidatos son fixtures sintéticos, no datos de mercado |

```bash
python3 -I -m unittest discover -s tests          # pruebas
python3 score.py candidatos_us.json candidatos_eu.json --csv ranking.csv --top 20
python3 faketest.py --visits 1000 --intents 150 --cpc 0.30
```

## Qué falta (y por qué)
- **Colectores de datos en masa** (DataForSEO, Google Trends API, Hacker News, Stack Exchange): no se escribieron porque no se pueden probar aquí. Los hosts están bloqueados por la política de red del entorno y faltan claves. Se añaden cuando se desbloqueen.
- El componente de **demanda** es un proxy débil hasta tener volúmenes reales.
- Los **pesos** del puntaje y los supuestos de `faketest.py` (*haircut*, prior) son iniciales y deben recalibrarse con las primeras pruebas.
