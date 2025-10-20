import os
import streamlit as st
import google.generativeai as genai 

# --- A. Leer la clave del candado ---
# Le dice a Python que busque la clave que pusiste en el panel Secrets.
API_KEY = os.environ.get('GEMINI_API_KEY')

# --- B. Configurar el servicio de Gemini ---
if API_KEY:
    # Si  la clave se encuentra, configura el servicio de Google
    genai.configure(api_key=API_KEY)
else:
    # Si la clave NO se encuentra, muestra un mensaje y detiene la aplicación
    st.error("¡Ups! Necesitas configurar tu Clave API de Gemini.")
    st.info("Ve al panel de Secrets (candado 🔒) y asegúrate de que la clave 'GEMINI_API_KEY' esté guardada correctamente.")
    st.stop()
import pandas as pd
import json
from datetime import datetime
import os
from components.selectors import render_selectors
from services.gemini_service import GeminiService
from services.pdf_generator import generate_pdf
from utils.data_loader import load_ciclos_data

# Configuración de la página
st.set_page_config(
    page_title="Asistente IA - Situaciones de Aprendizaje FP Sanitaria Aragón",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🏥 Crea tus Situaciones de Aprendizaje con IA")
st.subheader("Tu asistente personal para FP Sanitaria en Aragón")

# Inicializar servicios
@st.cache_resource
def init_services():
    return GeminiService()

gemini_service = init_services()

# Cargar datos
@st.cache_data
def load_data():
    return load_ciclos_data()

ciclos_data = load_data()

# Sidebar con información institucional
with st.sidebar:
    st.markdown("### 👋 ¡Hola!")
    st.info("""
    Te ayudo a crear situaciones de aprendizaje para FP Sanitaria en Aragón, siguiendo la normativa LOMLOE y las órdenes de 2024.
    
    Todo lo que generes estará alineado con los currículos oficiales.
    """)
    
    st.markdown("### 🎯 ¿Cómo funciona?")
    st.success("""
    1️⃣ Elige tu ciclo y módulo
    2️⃣ Selecciona metodologías que te gusten
    3️⃣ Define lo que quieres que aprendan
    4️⃣ ¡Dale al botón y la IA lo genera!
    5️⃣ Descarga tu situación y rúbrica en PDF
    
    Simple, rápido y listo para usar en clase 😊
    """)

# Contenedor principal
main_container = st.container()

with main_container:
    # Renderizar selectores
    selection_data = render_selectors(ciclos_data)
    
    if selection_data:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📝 Parámetros Adicionales")
            
            # Duración
            duracion = st.selectbox(
                "Duración estimada",
                ["1-2 sesiones (2-4 horas)", "3-5 sesiones (6-10 horas)", 
                 "1-2 semanas (12-20 horas)", "3-4 semanas (25-40 horas)", 
                 "Más de 1 mes (40+ horas)"]
            )
            
            # Recursos necesarios
            recursos = st.multiselect(
                "Recursos necesarios",
                ["Laboratorio de prácticas", "Simuladores clínicos", "Material sanitario", 
                 "Aula informática", "Biblioteca", "Centro sanitario", "Casos clínicos reales",
                 "Software especializado", "Material audiovisual", "Modelos anatómicos"]
            )
            
            # Contexto profesional
            contexto = st.text_area(
                "Contexto profesional específico",
                placeholder="Describe el contexto profesional donde se aplicará el aprendizaje...",
            )
            
        with col2:
            st.markdown("### 🎯 Tipo de Producto Final")
            producto_final = st.selectbox(
                "Selecciona el producto final",
                ["Proyecto de investigación", "Memoria técnica", "Presentación oral",
                 "Prototipo/Modelo", "Caso práctico resuelto", "Informe de prácticas",
                 "Plan de cuidados", "Protocolo de actuación", "Estudio de caso",
                 "Portfolio de evidencias"]
            )
            
            st.markdown("### ⚙️ Configuración IA")
            creatividad = st.slider(
                "Nivel de creatividad",
                min_value=0.1,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Mayor valor = más creativo y variado"
            )

    # Botón de generación
    if st.button("✨ Generar mi Situación de Aprendizaje", type="primary", use_container_width=True):
        if not selection_data:
            st.error("⚠️ ¡Espera! Antes necesito que elijas al menos un ciclo y un módulo.")
        else:
            with st.spinner("⏳ Generando tu situación de aprendizaje personalizada... Esto puede tardar unos segundos."):
                try:
                    # Preparar prompt para Gemini
                    prompt_data = {
                        **selection_data,
                        "duracion": duracion,
                        "recursos": recursos,
                        "contexto": contexto,
                        "producto_final": producto_final,
                        "creatividad": creatividad
                    }
                    
                    # Generar situación de aprendizaje
                    situacion = gemini_service.generar_situacion_aprendizaje(prompt_data)
                    
                    # Generar rúbrica
                    rubrica = gemini_service.generar_rubrica(prompt_data, situacion)
                    
                    # Mostrar resultados
                    st.success("🎉 ¡Listo! Aquí tienes tu situación de aprendizaje personalizada.")
                    
                    # Tabs para organizar el contenido
                    tab1, tab2, tab3 = st.tabs(["📋 Situación de Aprendizaje", "📊 Rúbrica de Evaluación", "📥 Descargar"])
                    
                    with tab1:
                        st.markdown(situacion)
                        
                    with tab2:
                        st.markdown(rubrica)
                    
                    with tab3:
                        st.markdown("### 📥 Opciones de descarga")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if st.button("📄 Descargar PDF", use_container_width=True):
                                pdf_content = generate_pdf(situacion, rubrica, prompt_data)
                                st.download_button(
                                    label="⬇️ Descargar PDF",
                                    data=pdf_content,
                                    file_name=f"situacion_aprendizaje_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                    mime="application/pdf"
                                )
                        
                        with col2:
                            if st.button("📝 Descargar Word", use_container_width=True):
                                # Para implementar descarga Word más adelante
                                st.info("Funcionalidad de descarga Word próximamente disponible")
                    
                    # Guardar en session state para mantener los resultados
                    st.session_state['ultima_situacion'] = situacion
                    st.session_state['ultima_rubrica'] = rubrica
                    st.session_state['ultimos_parametros'] = prompt_data
                    
                except Exception as e:
                    error_message = str(e)
                    if "INVALID_ARGUMENT" in error_message or "Invalid API key" in error_message or "API_KEY_INVALID" in error_message:
                        st.error("🔑 **¡Ups! Necesitas configurar tu clave de Gemini**")
                        st.warning("""
                        No te preocupes, es súper fácil y **gratis**:
                        
                        **Paso 1:** Consigue tu clave gratuita
                        - Entra en https://aistudio.google.com/apikey
                        - Usa tu cuenta de Google
                        - Dale a "Create API Key" (o "Get API Key")
                        - Copia la clave que te dan
                        
                        **Paso 2:** Ponla en la app
                        - En Replit, ve a "Secrets" (candadito en el lateral)
                        - Crea una nueva con nombre: `GEMINI_API_KEY`
                        - Pega tu clave como valor
                        
                        **Paso 3:** Recarga la página
                        ¡Y listo! Ya puedes generar tus situaciones 🎉
                        """)
                    else:
                        st.error(f"❌ Vaya, algo fue mal: {error_message}")
                        st.info("Revisa que hayas seleccionado todo correctamente. Si sigue fallando, prueba a recargar la página.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p style='color: #7f8c8d; font-size: 0.9em;'>
            Hecho con ❤️ para profes de FP Sanitaria en Aragón<br>
            Alineado con LOMLOE y las órdenes 842/843/2024
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
