import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Autoevaluación Estudiantil", page_icon="⭐", layout="centered")

st.markdown("""
<style>
    .stApp {
        background-color: #F0EAF8;
    }
    section.main > div {
        background-color: #F0EAF8;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2D1B69 !important;
        font-weight: 700;
    }
    p, label, div, span {
        color: #3B2A6E;
    }
    input[type="text"], textarea {
        background-color: #FFFFFF !important;
        color: #2D1B69 !important;
        border: 1.5px solid #C3A9E8 !important;
        border-radius: 10px !important;
    }
    input::placeholder, textarea::placeholder {
        color: #A08BBF !important;
    }
    .stButton > button[kind="primary"] {
        background-color: #7C4DCC !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #6A3DB8 !important;
    }
    .stButton > button:disabled {
        background-color: #C9B8E8 !important;
        color: #FFFFFF !important;
    }
    .criterio-card {
        background-color: #FFFFFF;
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.5rem;
        border: 1px solid #D8C6F0;
    }
    .criterio-titulo {
        font-size: 16px;
        font-weight: 700;
        color: #2D1B69;
        margin: 0 0 2px 0;
    }
    .criterio-desc {
        font-size: 13px;
        color: #6B5A90;
        margin: 0 0 10px 0;
    }
    .nota-label {
        font-size: 12px;
        color: #7C4DCC;
        font-weight: 600;
        margin-top: 4px;
    }
    [data-testid="stAlert"] {
        background-color: #EDE4FA !important;
        border: 1px solid #C3A9E8 !important;
        border-radius: 12px !important;
        color: #2D1B69 !important;
    }
    [data-testid="stCheckbox"] label {
        color: #2D1B69 !important;
        font-size: 14px;
    }
    [data-testid="stMetric"] {
        background-color: #EDE4FA;
        border-radius: 12px;
        padding: 10px;
    }
    [data-testid="stMetricValue"] {
        color: #2D1B69 !important;
    }
    hr { border-color: #D8C6F0; }
    .stCaption { color: #6B5A90 !important; }
    /* Botones de estrella: ocultar texto, mostrar solo icono */
    .star-btn-row button {
        background: none !important;
        border: none !important;
        font-size: 28px !important;
        padding: 0 !important;
        min-height: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

CRITERIOS = [
    ("participacion", "Participación activa",          "Contribución en clases, debates y actividades grupales."),
    ("puntualidad",   "Puntualidad y asistencia",      "Cumplimiento de horarios y presencia en las sesiones."),
    ("tareas",        "Entrega de tareas y trabajos",  "Cumplimiento oportuno con las actividades asignadas."),
    ("calidad",       "Calidad del trabajo entregado", "Profundidad, claridad y rigor en los productos académicos."),
    ("autonomia",     "Autonomía y responsabilidad",   "Capacidad de gestionar el aprendizaje de forma independiente."),
    ("colaboracion",  "Trabajo colaborativo",          "Aporte y disposición para trabajar en equipo."),
]

ETIQUETAS = {
    1: "1.0 – Insuficiente",
    2: "2.0 – Bajo",
    3: "3.0 – Básico",
    4: "4.0 – Alto",
    5: "5.0 – Superior",
}

CSV_FILE = "respuestas_autoevaluacion.csv"

def guardar_respuesta(datos: dict):
    df_nuevo = pd.DataFrame([datos])
    if os.path.exists(CSV_FILE):
        df_nuevo.to_csv(CSV_FILE, mode="a", header=False, index=False)
    else:
        df_nuevo.to_csv(CSV_FILE, index=False)

if "calificaciones" not in st.session_state:
    st.session_state.calificaciones = {key: 0 for key, _, _ in CRITERIOS}

st.title("⭐ Autoevaluación estudiantil")
st.caption("Valora tu desempeño en cada criterio de forma honesta. Selecciona las estrellas para calificar del 1.0 al 5.0.")

st.divider()

nombre = st.text_input("Nombre completo", placeholder="Escribe tu nombre completo")

st.divider()
st.markdown("#### Criterios de autoevaluación")

for key, nombre_criterio, descripcion in CRITERIOS:
    actual = st.session_state.calificaciones[key]

    estrellas_html = "".join(
        f'<span style="font-size:34px;color:{"#EF9F27" if i <= actual else "#D8C6F0"};">{"★" if i <= actual else "☆"}</span>'
        for i in range(1, 6)
    )
    etiqueta = ETIQUETAS.get(actual, "") if actual > 0 else "⚠ Sin calificar"

    st.markdown(f"""
    <div class="criterio-card">
        <p class="criterio-titulo">{nombre_criterio}</p>
        <p class="criterio-desc">{descripcion}</p>
        <div style="margin-bottom:4px;">{estrellas_html}</div>
        <p class="nota-label">{"→ " + etiqueta if actual > 0 else etiqueta}</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(5)
    for i, col in enumerate(cols, start=1):
        with col:
            if st.button(f"{'★' if i <= actual else '☆'} {i}", key=f"btn_{key}_{i}", use_container_width=True):
                st.session_state.calificaciones[key] = i
                st.rerun()

    st.write("")

st.divider()

comentarios = st.text_area(
    "Comentarios adicionales (opcional)",
    placeholder="Si deseas, comparte alguna reflexión sobre tu proceso de aprendizaje...",
    height=100
)

st.divider()

st.markdown("#### Declaración de compromiso y veracidad")
st.info(
    "Declaro, bajo mi palabra de honor, que la calificación consignada en este formulario "
    "refleja de manera fiel y honesta mi propio desempeño académico. Así mismo, confirmo que "
    "soy quien suscribe esta autoevaluación y que no estoy suplantando la identidad de ningún "
    "otro estudiante. Entiendo que esta calificación será tenida en cuenta por el docente en "
    "la evaluación final del curso."
)
juramento = st.checkbox("Acepto la declaración anterior")

st.write("")

todos_calificados = all(v > 0 for v in st.session_state.calificaciones.values())
listo = nombre.strip() != "" and juramento and todos_calificados

st.button("Enviar autoevaluación", type="primary", disabled=not listo, use_container_width=True, key="enviar")

if st.session_state.get("enviar") and listo:
    calificaciones = {
        nombre_criterio: float(st.session_state.calificaciones[key])
        for key, nombre_criterio, _ in CRITERIOS
    }
    promedio = round(sum(calificaciones.values()) / len(calificaciones), 2)
    datos = {
        "Fecha y hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Nombre": nombre.strip(),
        **calificaciones,
        "Promedio": promedio,
        "Comentarios": comentarios.strip(),
    }
    guardar_respuesta(datos)
    st.session_state.calificaciones = {key: 0 for key, _, _ in CRITERIOS}

    st.success(f"¡Autoevaluación enviada correctamente, {nombre.split()[0]}!")
    st.balloons()

    st.markdown("#### Resumen de tu calificación")
    col1, col2 = st.columns([3, 1])
    with col1:
        for criterio, nota in calificaciones.items():
            st.markdown(f"- **{criterio}:** {nota:.1f}")
    with col2:
        st.metric("Promedio", f"{promedio:.1f}")

    st.divider()
    st.caption("Tus respuestas han sido guardadas. Puedes cerrar esta ventana.")
