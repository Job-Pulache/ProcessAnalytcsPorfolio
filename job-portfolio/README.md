# Portfolio v2.0 — Job Pulache Carreño

Dashboard ejecutivo interactivo (Streamlit + Plotly) para compartir con empresas agroindustriales.
Posicionamiento: Analista de Operaciones y Procesos con formación en Sistemas.

## Probarlo en tu compu

```bash
pip install -r requirements.txt
streamlit run app.py
```
Si `streamlit` no se reconoce como comando, usa:
```bash
python -m streamlit run app.py
```

Se abre en `http://localhost:8501`.

## Publicarlo gratis (para tener un link que enviar a empresas)

1. Sube esta carpeta a un repositorio en GitHub.
2. Entra a **share.streamlit.io** con tu cuenta de GitHub.
3. "New app" → elige el repo, la rama y `app.py` como archivo principal → Deploy.
4. En un par de minutos tienes un link tipo `https://job-pulache-portfolio.streamlit.app`.

## Qué cambió en la v2.0

- **Hero ejecutivo**: mensaje de valor + panel de mini-dashboard (status, ubicación, foco, proyecto actual).
- **Narrative rail**: hilo conductor de 5 pasos (Comprender → Analizar → Optimizar → Automatizar → Construir AgroBrain) que conecta toda la página.
- **Perfil Ejecutivo** reemplaza los KPIs numéricos: 4 capacidades transversales, no cantidades.
- **Trayectoria** reescrita como habilidades adquiridas (Comprendiendo la operación, Calidad del dato, Optimización de procesos, Transformación digital), sin lenguaje de "digitador".
- **Casos de éxito** con estructura de 5 etapas: Problema → Análisis → Solución → Resultado → Impacto para el negocio.
- **AgroBrain IA** reposicionado como visión de negocio primero; el detalle técnico (arquitectura, stack) vive en un expander opcional.
- **Módulo en vivo**: el simulador ahora usa `st.status` (pipeline paso a paso), `st.progress` y `st.metric` — se siente como un módulo empresarial, no un demo de juguete.
- **Capacidades**: matriz de competencias con badges cualitativos (NÚCLEO / SÓLIDO / EN CRECIMIENTO) en vez de porcentajes o gráficos de radar inventados.
- **Microinteracciones**: fade-in al hacer scroll (`.reveal`), mejores hovers, badges de estado.
- **Código**: componentes reutilizables (`section_header`, `panel_card`, `capability_card`, `case_card`) en vez de HTML repetido.

Paleta, tipografía (Space Mono + Public Sans), nav fijo/dock móvil y modo claro/oscuro se mantienen exactamente iguales a la v1.

## Estructura

```
app.py              -> toda la app (una sola página)
assets/
  profile_natural.jpg
  profile_duotone.jpg
.streamlit/config.toml
requirements.txt
```

## Personalizar

- Textos: listas `TIMELINE`, `EXEC_PROFILE`, `CAPABILITIES`, `RAIL_STEPS` en `app.py`.
- Colores: diccionario `C` (uno para modo oscuro, uno para claro), al inicio del archivo.
- Datos del simulador: diccionario `MOCK_PRODUCERS` — son datos de ejemplo, no reales.
