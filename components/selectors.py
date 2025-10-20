import streamlit as st
import json

def render_selectors(ciclos_data):
    """Renderiza todos los selectores de la interfaz y retorna los datos seleccionados"""
    
    selection_data = {}
    
    # Selector de nivel formativo
    st.markdown("### 🎓 Selección del Ciclo Formativo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nivel = st.selectbox(
            "Nivel formativo",
            ["Seleccionar...", "Grado Medio", "Grado Superior"]
        )
        
        if nivel != "Seleccionar...":
            selection_data["nivel"] = nivel
            nivel_key = "grado_medio" if nivel == "Grado Medio" else "grado_superior"
            
            # Selector de ciclo formativo
            ciclos_disponibles = ["Seleccionar..."] + list(ciclos_data[nivel_key].keys())
            ciclo_seleccionado = st.selectbox(
                "Ciclo Formativo",
                ciclos_disponibles
            )
            
            if ciclo_seleccionado != "Seleccionar...":
                selection_data["ciclo"] = ciclo_seleccionado
                ciclo_data = ciclos_data[nivel_key][ciclo_seleccionado]
                
                # Mostrar información del ciclo
                st.info(f"**Código:** {ciclo_data['codigo']} | **Duración:** {ciclo_data['duracion']}")
    
    with col2:
        if "ciclo" in selection_data:
            # Selector de módulo
            modulos_disponibles = ["Seleccionar..."] + list(ciclo_data["modulos"].keys())
            modulo_seleccionado = st.selectbox(
                "Módulo Profesional",
                modulos_disponibles
            )
            
            if modulo_seleccionado != "Seleccionar...":
                selection_data["modulo"] = modulo_seleccionado
                modulo_data = ciclo_data["modulos"][modulo_seleccionado]
                
                # Mostrar información del módulo
                st.info(f"**Código:** {modulo_data['codigo']} | **Horas:** {modulo_data['horas']}")

    # Si hay módulo seleccionado, mostrar más opciones
    if "modulo" in selection_data:
        st.markdown("### 📚 Resultados de Aprendizaje y Criterios")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Selector de resultados de aprendizaje
            resultados_disponibles = modulo_data.get("resultados_aprendizaje", [])
            if resultados_disponibles:
                resultados_seleccionados = st.multiselect(
                    "Resultados de Aprendizaje (RA)",
                    resultados_disponibles,
                    help="Selecciona uno o más resultados de aprendizaje del módulo"
                )
                if resultados_seleccionados:
                    selection_data["resultados_aprendizaje"] = resultados_seleccionados
        
        with col2:
            # Selector de criterios de evaluación
            criterios_disponibles = modulo_data.get("criterios_evaluacion", [])
            if criterios_disponibles:
                criterios_seleccionados = st.multiselect(
                    "Criterios de Evaluación (CE)",
                    criterios_disponibles,
                    help="Selecciona uno o más criterios de evaluación"
                )
                if criterios_seleccionados:
                    selection_data["criterios_evaluacion"] = criterios_seleccionados

        # Metodologías activas
        st.markdown("### 🎯 Metodología y Competencias")
        
        col1, col2 = st.columns(2)
        
        with col1:
            metodologia_seleccionada = st.selectbox(
                "Metodología Activa Principal",
                ["Seleccionar..."] + ciclos_data["metodologias_activas"]
            )
            
            if metodologia_seleccionada != "Seleccionar...":
                selection_data["metodologia"] = metodologia_seleccionada
                
            # Metodologías secundarias
            metodologias_secundarias = st.multiselect(
                "Metodologías Complementarias (opcional)",
                [m for m in ciclos_data["metodologias_activas"] if m != metodologia_seleccionada],
                help="Selecciona metodologías adicionales que se integrarán"
            )
            if metodologias_secundarias:
                selection_data["metodologias_secundarias"] = metodologias_secundarias
        
        with col2:
            # Competencias profesionales
            competencias_prof = st.multiselect(
                "Competencias Profesionales",
                ciclos_data["competencias"]["profesionales"],
                help="Selecciona las competencias profesionales a desarrollar"
            )
            if competencias_prof:
                selection_data["competencias_profesionales"] = competencias_prof
            
            # Competencias personales y sociales
            competencias_pers = st.multiselect(
                "Competencias Personales",
                ciclos_data["competencias"]["personales"][:4],  # Limitar para no saturar
                help="Selecciona las competencias personales a desarrollar"
            )
            if competencias_pers:
                selection_data["competencias_personales"] = competencias_pers
            
            competencias_soc = st.multiselect(
                "Competencias Sociales", 
                ciclos_data["competencias"]["sociales"][:4],  # Limitar para no saturar
                help="Selecciona las competencias sociales a desarrollar"
            )
            if competencias_soc:
                selection_data["competencias_sociales"] = competencias_soc

    return selection_data if len(selection_data) >= 2 else None
