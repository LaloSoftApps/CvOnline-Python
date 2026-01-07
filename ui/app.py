import streamlit as st
import json
import base64
import requests

# ----------------------------------
# Configuración general
# ----------------------------------
st.set_page_config(page_title="Curriculum Vitae", layout="wide")


# ----------------------------------
# Configuración API
# ----------------------------------
API_URL = "http://localhost:8000/cv" # Reemplazar por la URL real
API_TIMEOUT = 10

# ----------------------------------
# Utilidades
# ----------------------------------
def load_cv_from_api(url: str) -> dict:
    response = requests.get(url, timeout=API_TIMEOUT)
    response.raise_for_status()
    return response.json()


def image_to_base64(path: str) -> str:
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

# ----------------------------------
# Cargar datos desde API
# ----------------------------------
try:
    cv = load_cv_from_api(API_URL)
except Exception as e:
    st.error(f"No se pudo obtener la información del CV desde la API: {e}")
    st.stop()


# ----------------------------------
# Estilos CSS
# ----------------------------------
st.markdown(
    """
    <style>
/* Header principal */
.hero {
    background-color: #e5e7eb;
    padding: 50px 40px;
    border-radius: 18px;
    margin-bottom: 40px;
}
.hero-grid {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 40px;
    align-items: center;
}
.hero-photo {
    text-align: center;
}
.hero-text {
    text-align: left;
}
.profile-img {
    width: 170px;
    height: 170px;
    border-radius: 50%;
    object-fit: cover;
    border: 4px solid #6b7280;
}
.name {
    font-size: 38px;
    font-weight: 700;
}
.role {
    font-size: 20px;
    color: #374151;
    margin-top: 10px;
}

/* Secciones */
.section-title {
    background-color: #e5e7eb;
    font-size: 26px;
    font-weight: 700;
    border-bottom: 3px solid #374151;
    padding-bottom: 6px;
    margin: 40px 0 22px 0;
}
.card {
    background-color: #f9fafb;
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 18px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}
.muted {
    color: #6b7280;
    font-size: 14px;
}
</style>
    """,
    unsafe_allow_html=True
)

# ----------------------------------
# Sección principal (fondo gris)
# ----------------------------------
photo_b64 = image_to_base64(cv["header"]["photo"])

st.markdown(
    f"""
    <div class="hero">
  <div class="hero-grid">
    <div class="hero-photo">
      <img src="data:image/png;base64,{photo_b64}" class="profile-img" />
    </div>
    <div class="hero-text">
      <div class="name">{cv['header']['name']} {cv['header']['surname']}</div>
      <div class="role">{cv['header']['description']}</div>
    </div>
  </div>
</div>
    """,
    unsafe_allow_html=True
)

# ----------------------------------
# Información Personal
# ----------------------------------
st.markdown('<div class="section-title">Información</div>', unsafe_allow_html=True)

c = cv["contact"]
st.markdown(
    f"""
    <div class="card">
        <b>Fecha de nacimiento:</b> {c['birthdate']}<br>
        <b>Email:</b> {c['email']}<br>
        <b>Teléfono:</b> {c['phone']}<br>
        <b>Dirección:</b> {c['address']}<br>
        <b>LinkedIn:</b> {c['linkedin']}<br>
        <b>GitHub:</b> {c['github']}
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------------
# Experiencia Laboral
# ----------------------------------
st.markdown('<div class="section-title">Experiencia Laboral</div>', unsafe_allow_html=True)

for exp in cv.get("experience", []):
    st.markdown(
        f"""
        <div class="card">
            <b>{exp['position']}</b> – {exp['company']}<br>
            <span class="muted">{exp['from']} - {exp['to']}</span><br>
            <b>Tecnologías:</b> {', '.join(exp['technologies'])}
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------------
# Formación
# ----------------------------------
st.markdown('<div class="section-title">Formación</div>', unsafe_allow_html=True)

for edu in cv.get("education", []):
    st.markdown(
        f"""
        <div class="card">
            <b>{edu['title']}</b><br>
            {edu['institution']} – {edu['degree']}<br>
            <span class="muted">{edu['date']}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------------
# Cursos y Capacitaciones
# ----------------------------------
st.markdown('<div class="section-title">Cursos y Capacitaciones</div>', unsafe_allow_html=True)

for course in cv.get("courses", []):
    st.markdown(
        f"""
        <div class="card">
            <b>{course['name']}</b><br>
            {course['institution']}<br>
            <span class="muted">{course['date']}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------------
# Idiomas
# ----------------------------------
if "languages" in cv:
    st.markdown('<div class="section-title">Idiomas</div>', unsafe_allow_html=True)
    st.markdown(
        f"<div class='card'>{' • '.join(cv['languages'])}</div>",
        unsafe_allow_html=True
    )

# ----------------------------------
# Skills
# ----------------------------------
if "skills" in cv:
    st.markdown('<div class="section-title">Skills</div>', unsafe_allow_html=True)
    st.markdown(
        f"<div class='card'>{' • '.join(cv['skills'])}</div>",
        unsafe_allow_html=True
    )

# ----------------------------------
# Intereses
# ----------------------------------
if "interests" in cv:
    st.markdown('<div class="section-title">Intereses</div>', unsafe_allow_html=True)
    st.markdown(
        f"<div class='card'>{' • '.join(cv['interests'])}</div>",
        unsafe_allow_html=True
    )
