import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Autoevaluación Estudiantil", page_icon="⭐", layout="centered")

st.markdown("""
<style>
    .main { max-width: 680px; margin: 0 auto; }
    .stSlider > div > div > div { background: #EF9F27; }
    div[data-testid="stForm"] { border: none; padding: 0; }
</style>
""", unsafe_allow_html=True)

CRITERIOS = [
    ("participacion",   "Participación activa",          "Contribución en clases, debates y actividades grupales."),
    ("puntualidad",     "Puntualidad y asistencia",      "Cumplimiento de horarios y presencia en las sesiones."),
    ("tareas",          "Entrega de tareas y trabajos",  "Cumplimiento oportuno con las actividades asignadas."),
    ("calidad",         "Calidad del trabajo entregado", "Profundidad, claridad y rigor en los productos académicos."),
    ("autonomia",       "Autonomía y responsabilidad",   "Capacidad de gestionar el aprendizaje de forma independiente."),
    ("colaboracion",    "Trabajo colaborativo",          "Aporte y disposición para trabajar en equipo."),
]

ETIQUETAS = {
    1.0: "1.0 – Insuficiente",
    1.5: "1.5",
    2.0: "2.0 – Bajo",
    2.5: "2.5",
    3.0: "3.0 – Básico",
    3.5: "3.5",
    4.0: "4.0 – Alto",
    4.5: "4.5",
    5.0: "5.0 – Superior",
}

CSV_FILE = "respuestas_autoevaluacion.csv"

def guardar_respuesta(datos: dict):
    df_nuevo = pd.DataFrame([datos])
    if os.path.exists(CSV_FILE):
        df_nuevo.to_csv(CSV_FILE, mode="a", header=False, index=False)
    else:
        df_nuevo.to_csv(CSV_FILE, index=False)

st.title("Autoevaluación estudiantil")
st.caption("Valora tu desempeño en cada criterio de forma honesta. La calificación va de 1.0 a 5.0.")

st.divider()

nombre = st.text_input("Nombre completo", placeholder="Escribe tu nombre completo")

st.divider()
st.markdown("#### Criterios de autoevaluación")

calificaciones = {}
for key, nombre_criterio, descripcion in CRITERIOS:
    st.markdown(f"**{nombre_criterio}**")
    st.caption(descripcion)
    val = st.slider(
        label=nombre_criterio,
        min_value=1.0, max_value=5.0, value=3.0, step=0.5,
        key=key,
        label_visibility="collapsed"
    )
    st.markdown(f"<small style='color:gray'>→ {ETIQUETAS.get(val, str(val))}</small>", unsafe_allow_html=True)
    calificaciones[nombre_criterio] = val
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

listo = nombre.strip() != "" and juramento
boton = st.button("Enviar autoevaluación", type="primary", disabled=not listo, use_container_width=True)

if boton and listo:
    promedio = round(sum(calificaciones.values()) / len(calificaciones), 2)
    datos = {
        "Fecha y hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Nombre": nombre.strip(),
        **calificaciones,
        "Promedio": promedio,
        "Comentarios": comentarios.strip(),
    }
    guardar_respuesta(datos)

    st.success(f"¡Autoevaluación enviada correctamente, {nombre.split()[0]}!")
    st.balloons()

    st.markdown("#### Resumen de tu calificación")
    col1, col2 = st.columns([3, 1])
    with col1:
        for criterio, nota in calificaciones.items():
            st.markdown(f"- **{criterio}:** {nota}")
    with col2:
        st.metric("Promedio", f"{promedio}")

    st.divider()
    st.caption("Tus respuestas han sido guardadas. Puedes cerrar esta ventana.")
