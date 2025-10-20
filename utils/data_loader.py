import json
import os
import streamlit as st

@st.cache_data()
def load_ciclos_data():
    """Carga los datos de ciclos formativos desde el archivo JSON"""

    try:
        # RUTA CORREGIDA: Esto soluciona los errores de ruta y existencia
        data_path = "data/ciclos_sanitarios.json"

        with open(data_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception as e:
        # Si falla, muestra el error y usa datos por defecto
        st.error(f"Error al cargar los datos: {str(e)}")
        return get_default_data()

def _get_default_data():
    """Retorna datos básicos por defecto en caso de error"""
    return {
        "grado_medio": {
            "Cuidados Auxiliares de Enfermería": {
                "codigo": "SAN01",
                "duracion": "2000 horas",
                "modulos": {
                    "Técnicas básicas de enfermería": {
                        "codigo": "0021",
                        "horas": 230,
                        "resultados_aprendizaje": [
                            "Aplica técnicas de aseo e higiene corporal",
                            "Aplica técnicas de movilización y traslado",
                            "Realiza técnicas de alimentación enteral"
                        ],
                        "criterios_evaluacion": [
                            "Se han aplicado las medidas de protección individual",
                            "Se han identificado las necesidades de aseo e higiene",
                            "Se han aplicado técnicas de movilización"
                        ]
                    }
                }
            }
        },
        "grado_superior": {
            "Imagen para el Diagnóstico y Medicina Nuclear": {
                "codigo": "SAN11",
                "duracion": "2000 horas",
                "modulos": {
                    "Anatomía por la imagen": {
                        "codigo": "0041",
                        "horas": 165,
                        "resultados_aprendizaje": [
                            "Identifica la anatomía humana interpretando las estructuras"
                        ],
                        "criterios_evaluacion": [
                            "Se han identificado las estructuras anatómicas básicas"
                        ]
                    }
                }
            }
        },
        "metodologias_activas": [
            "Aprendizaje Basado en Problemas (ABP)",
            "Aprendizaje Colaborativo",
            "Gamificación"
        ],
        "competencias": {
            "profesionales": [
                "Aplicar técnicas y protocolos de trabajo según normativa"
            ],
            "personales": [
                "Desarrollar la responsabilidad profesional"
            ],
            "sociales": [
                "Comunicarse de forma efectiva con pacientes"
            ]
        }
    }

def validate_selection_data(selection_data, ciclos_data):
    """Valida que los datos seleccionados sean consistentes"""
    
    if not selection_data:
        return False, "No hay datos seleccionados"
    
    required_fields = ["nivel", "ciclo", "modulo"]
    
    for field in required_fields:
        if field not in selection_data:
            return False, f"Falta el campo requerido: {field}"
    
    # Validar que el ciclo existe
    nivel_key = "grado_medio" if selection_data["nivel"] == "Grado Medio" else "grado_superior"
    
    if selection_data["ciclo"] not in ciclos_data.get(nivel_key, {}):
        return False, "El ciclo seleccionado no es válido"
    
    # Validar que el módulo existe
    ciclo_data = ciclos_data[nivel_key][selection_data["ciclo"]]
    if selection_data["modulo"] not in ciclo_data.get("modulos", {}):
        return False, "El módulo seleccionado no es válido"
    
    return True, "Datos válidos"

def get_modulo_info(selection_data, ciclos_data):
    """Obtiene información detallada del módulo seleccionado"""
    
    if not selection_data or "nivel" not in selection_data:
        return None
    
    try:
        nivel_key = "grado_medio" if selection_data["nivel"] == "Grado Medio" else "grado_superior"
        ciclo_data = ciclos_data[nivel_key][selection_data["ciclo"]]
        modulo_data = ciclo_data["modulos"][selection_data["modulo"]]
        
        return {
            "ciclo_info": ciclo_data,
            "modulo_info": modulo_data,
            "nivel_formativo": selection_data["nivel"]
        }
        
    except KeyError as e:
        st.error(f"Error al obtener información del módulo: {str(e)}")
        return None
