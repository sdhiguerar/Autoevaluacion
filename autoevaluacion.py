import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Autoevaluación Estudiantil", page_icon="⭐", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #F0EAF8; }
    section.main > div { background-color: #F0EAF8; }
    h1, h2, h3, h4, h5, h6 { color: #2D1B69 !important; font-weight: 700; }
    p, label, div, span { color: #3B2A6E; }
    input[type="text"], input[type="password"], textarea {
        background-color: #FFFFFF !important;
        color: #2D1B69 !important;
        border: 1.5px solid #C3A9E8 !important;
        border-radius: 10px !important;
    }
    input::placeholder, textarea::placeholder { color: #A08BBF !important; }
    .stButton > button[kind="primary"] {
        background-color: #7C4DCC !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
    }
    .stButton > button[kind="primary"]:hover { background-color: #6A3DB8 !important; }
    .stButton > button:disabled { background-color: #C9B8E8 !important; color: #FFFFFF !important; }
    .criterio-card {
        background-color: #FFFFFF;
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.5rem;
        border: 1px solid #D8C6F0;
    }
    .criterio-titulo { font-size: 16px; font-weight: 700; color: #2D1B69; margin: 0 0 2px 0; }
    .criterio-desc { font-size: 13px; color: #6B5A90; margin: 0 0 10px 0; }
    .nota-label { font-size: 12px; color: #7C4DCC; font-weight: 600; margin-top: 4px; }
    [data-testid="stAlert"] {
        background-color: #EDE4FA !important;
        border: 1px solid #C3A9E8 !important;
        border-radius: 12px !important;
        color: #2D1B69 !important;
    }
    [data-testid="stCheckbox"] label { color: #2D1B69 !important; font-size: 14px; }
    [data-testid="stMetric"] { background-color: #EDE4FA; border-radius: 12px; padding: 10px; }
    [data-testid="stMetricValue"] { color: #2D1B69 !important; }
    hr { border-color: #D8C6F0; }
    .stCaption { color: #6B5A90 !important; }
    .login-card {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 2rem 2rem 1.5rem;
        border: 1px solid #D8C6F0;
        max-width: 400px;
        margin: 3rem auto 0;
    }
    .panel-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        border: 1px solid #D8C6F0;
        margin-bottom: 1rem;
    }
    .danger-btn > button {
        background-color: #F5E4E4 !important;
        color: #A32D2D !important;
        border: 1px solid #F0A0A0 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    .danger-btn > button:hover { background-color: #F0C0C0 !important; }
    [data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Configuración ──────────────────────────────────────────────
DOCENTE_USER = "docente"
DOCENTE_PASS = "curso2025"
CSV_FILE     = "respuestas_autoevaluacion.csv"

CRITERIOS = [
    ("participacion", "Participación activa",          "Contribución en clases, debates y actividades grupales."),
    ("puntualidad",   "Puntualidad y asistencia",      "Cumplimiento de horarios y presencia en las sesiones."),
    ("tareas",        "Entrega de tareas y trabajos",  "Cumplimiento oportuno con las actividades asignadas."),
    ("calidad",       "Calidad del trabajo entregado", "Profundidad, claridad y rigor en los productos académicos."),
    ("autonomia",     "Autonomía y responsabilidad",   "Capacidad de gestionar el aprendizaje de forma independiente."),
    ("colaboracion",  "Trabajo colaborativo",          "Aporte y disposición para trabajar en equipo."),
]

ETIQUETAS = {1: "1.0 – Insuficiente", 2: "2.0 – Bajo", 3: "3.0 – Básico", 4: "4.0 – Alto", 5: "5.0 – Superior"}

def guardar_respuesta(datos: dict):
    df_nuevo = pd.DataFrame([datos])
    if os.path.exists(CSV_FILE):
        df_nuevo.to_csv(CSV_FILE, mode="a", header=False, index=False)
    else:
        df_nuevo.to_csv(CSV_FILE, index=False)

def cargar_registros():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame()

# ── Estado de sesión ───────────────────────────────────────────
if "calificaciones" not in st.session_state:
    st.session_state.calificaciones = {key: 0 for key, _, _ in CRITERIOS}
if "docente_auth" not in st.session_state:
    st.session_state.docente_auth = False
if "vista" not in st.session_state:
    st.session_state.vista = "estudiante"
if "confirmar_eliminar" not in st.session_state:
    st.session_state.confirmar_eliminar = False

# ══════════════════════════════════════════════════════════════
#  BARRA LATERAL — navegación
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### Navegación")
    if st.button("📝  Formulario estudiante", use_container_width=True):
        st.session_state.vista = "estudiante"
        st.rerun()
    if st.button("🔒  Panel docente", use_container_width=True):
        st.session_state.vista = "login" if not st.session_state.docente_auth else "panel"
        st.rerun()
    if st.session_state.docente_auth:
        st.divider()
        if st.button("Cerrar sesión", use_container_width=True):
            st.session_state.docente_auth = False
            st.session_state.vista = "estudiante"
            st.rerun()

# ══════════════════════════════════════════════════════════════
#  VISTA: FORMULARIO ESTUDIANTE
# ══════════════════════════════════════════════════════════════
if st.session_state.vista == "estudiante":
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

    if st.button("Enviar autoevaluación", type="primary", disabled=not listo, use_container_width=True):
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
            "Declaración aceptada": "Sí",
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

# ══════════════════════════════════════════════════════════════
#  VISTA: LOGIN DOCENTE
# ══════════════════════════════════════════════════════════════
elif st.session_state.vista == "login":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("### 🔒 Acceso docente")
    st.caption("Ingresa tus credenciales para ver los registros de autoevaluación.")
    st.write("")
    usuario = st.text_input("Usuario", placeholder="Usuario")
    contrasena = st.text_input("Contraseña", type="password", placeholder="Contraseña")
    st.write("")
    if st.button("Ingresar", type="primary", use_container_width=True):
        if usuario == DOCENTE_USER and contrasena == DOCENTE_PASS:
            st.session_state.docente_auth = True
            st.session_state.vista = "panel"
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  VISTA: PANEL DOCENTE
# ══════════════════════════════════════════════════════════════
elif st.session_state.vista == "panel" and st.session_state.docente_auth:

    st.title("📊 Panel docente")
    st.caption("Consulta, descarga y administra los registros de autoevaluación.")
    st.divider()

    df = cargar_registros()

    if df.empty:
        st.info("Aún no hay registros de autoevaluación.")
    else:
        # ── Métricas rápidas ──────────────────────────────────
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de estudiantes", len(df))
        with col2:
            st.metric("Promedio del grupo", f"{df['Promedio'].mean():.2f}")
        with col3:
            st.metric("Nota más alta", f"{df['Promedio'].max():.1f}")

        st.write("")

        # ── Tabla de registros ────────────────────────────────
        st.markdown("#### Registros de autoevaluación")
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.write("")

        # ── Descarga ──────────────────────────────────────────
        st.markdown("#### Descargar registros")
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️  Descargar como Excel (.csv)",
            data=csv_bytes,
            file_name=f"autoevaluacion_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True,
        )

        st.write("")

        # ── Eliminar registros ────────────────────────────────
        st.markdown("#### Eliminar registros")
        st.warning("⚠️ Esta acción eliminará **todos** los registros de forma permanente. Asegúrate de haber descargado el archivo antes de continuar.")

        if not st.session_state.confirmar_eliminar:
            with st.container():
                st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
                if st.button("🗑️  Eliminar todos los registros", use_container_width=True):
                    st.session_state.confirmar_eliminar = True
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("¿Estás seguro? Esta acción no se puede deshacer.")
            col_si, col_no = st.columns(2)
            with col_si:
                if st.button("Sí, eliminar", type="primary", use_container_width=True):
                    if os.path.exists(CSV_FILE):
                        os.remove(CSV_FILE)
                    st.session_state.confirmar_eliminar = False
                    st.success("Registros eliminados correctamente.")
                    st.rerun()
            with col_no:
                if st.button("Cancelar", use_container_width=True):
                    st.session_state.confirmar_eliminar = False
                    st.rerun()
