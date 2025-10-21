import os
import json
from google import genai
from google.genai import types

class GeminiService:
    def __init__(self):
        """Inicializa el servicio de Gemini con la API key"""
        api_key = os.getenv("GEMINI_API_KEY", "default_key")
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"
    
    def generar_situacion_aprendizaje(self, datos_seleccion):
        """Genera una situación de aprendizaje completa usando Gemini AI"""
        
        prompt = self._construir_prompt_situacion(datos_seleccion)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=datos_seleccion.get("creatividad", 0.7),
                    max_output_tokens=4000
                )
            )
            
            return response.text or "Error: No se pudo generar la situación de aprendizaje"
            
        except Exception as e:
            raise Exception(f"Error al generar situación de aprendizaje: {str(e)}")
    
    def generar_rubrica(self, datos_seleccion, situacion_aprendizaje):
        """Genera una rúbrica de evaluación basada en la situación de aprendizaje"""
        
        prompt = self._construir_prompt_rubrica(datos_seleccion, situacion_aprendizaje)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.5,  # Menos creatividad para rúbricas más estructuradas
                    max_output_tokens=3000
                )
            )
            
            return response.text or "Error: No se pudo generar la rúbrica"
            
        except Exception as e:
            raise Exception(f"Error al generar rúbrica: {str(e)}")
    
    def _construir_prompt_situacion(self, datos):
        """Construye el prompt para generar la situación de aprendizaje"""
        
        prompt = f"""
        Actúa como un experto en pedagogía y formación profesional sanitaria en España. Necesito que generes una SITUACIÓN DE APRENDIZAJE completa y detallada para Formación Profesional Sanitaria en Aragón, totalmente alineada con:

        - LOMLOE (Ley Orgánica 3/2020)
        - ORDEN ECD/842/2024 (Grado Medio) y ORDEN ECD/843/2024 (Grado Superior)
        - Decreto 91/2024 del Gobierno de Aragón
        - Real Decreto de enseñanzas mínimas correspondiente

        ## DATOS DE LA SITUACIÓN:
        
        **Ciclo Formativo:** {datos.get('nivel', '')} - {datos.get('ciclo', '')}
        **Módulo Profesional:** {datos.get('modulo', '')}
        **Metodología Principal:** {datos.get('metodologia', '')}
        **Metodologías Complementarias:** {', '.join(datos.get('metodologias_secundarias', []))}
        **Duración:** {datos.get('duracion', '')}
        **Recursos Necesarios:** {', '.join(datos.get('recursos', []))}
        **Contexto Profesional:** {datos.get('contexto', '')}
        **Producto Final:** {datos.get('producto_final', '')}

        **Resultados de Aprendizaje seleccionados:**
        {chr(10).join(f"- {ra}" for ra in datos.get('resultados_aprendizaje', []))}

        **Criterios de Evaluación seleccionados:**
        {chr(10).join(f"- {ce}" for ce in datos.get('criterios_evaluacion', []))}

        **Competencias Profesionales:**
        {chr(10).join(f"- {cp}" for cp in datos.get('competencias_profesionales', []))}

        **Competencias Personales:**
        {chr(10).join(f"- {cp}" for cp in datos.get('competencias_personales', []))}

        **Competencias Sociales:**
        {chr(10).join(f"- {cs}" for cs in datos.get('competencias_sociales', []))}

        ## ESTRUCTURA REQUERIDA DE LA SITUACIÓN DE APRENDIZAJE:

        Genera una situación de aprendizaje completa con la siguiente estructura en formato Markdown:

        # SITUACIÓN DE APRENDIZAJE: [Título atractivo y específico]

        ## 1. IDENTIFICACIÓN
        - **Título:** 
        - **Ciclo Formativo:** 
        - **Módulo Profesional:** 
        - **Nivel:** 
        - **Duración:** 
        - **Temporalización:** 

        ## 2. CONTEXTUALIZACIÓN Y JUSTIFICACIÓN
        [Descripción del contexto profesional real donde se desarrolla, justificación pedagógica alineada con LOMLOE y normativa aragonesa]

        ## 3. OBJETIVOS Y COMPETENCIAS
        ### Objetivos Didácticos:
        [3-5 objetivos específicos y medibles]

        ### Competencias a Desarrollar:
        - **Competencia general del ciclo:** 
        - **Competencias profesionales:** 
        - **Competencias personales y sociales:** 

        ## 4. RESULTADOS DE APRENDIZAJE Y CRITERIOS DE EVALUACIÓN
        [Especificar exactamente los RA y CE seleccionados y cómo se trabajan]

        ## 5. SABERES BÁSICOS/CONTENIDOS
        ### Contenidos Conceptuales:
        ### Contenidos Procedimentales:
        ### Contenidos Actitudinales:

        ## 6. METODOLOGÍA
        ### Metodología Principal: {datos.get('metodologia', '')}
        [Descripción detallada de cómo se aplicará]

        ### Metodologías Complementarias:
        [Si existen metodologías secundarias, explicar su integración]

        ### Estrategias Inclusivas:
        [Medidas de atención a la diversidad y accesibilidad universal]

        ## 7. SECUENCIA DIDÁCTICA
        ### Fase 1: [Nombre de la fase]
        - **Duración:** 
        - **Actividades:** 
        - **Recursos:** 
        - **Evaluación:** 

        ### Fase 2: [Nombre de la fase]
        - **Duración:** 
        - **Actividades:** 
        - **Recursos:** 
        - **Evaluación:** 

        [Continuar con las fases necesarias según la duración]

        ## 8. RECURSOS Y MATERIALES
        ### Recursos Humanos:
        ### Recursos Materiales:
        ### Recursos Tecnológicos:
        ### Espacios:

        ## 9. EVALUACIÓN
        ### Instrumentos de Evaluación:
        ### Criterios de Calificación:
        ### Procedimientos de Evaluación:
        ### Evaluación Inclusiva:

        ## 10. PRODUCTO FINAL
        **Producto:** {datos.get('producto_final', '')}
        [Descripción detallada del producto final esperado, criterios de calidad, presentación]

        ## 11. BIBLIOGRAFÍA Y REFERENCIAS
        [Referencias normativas y bibliográficas actualizadas]

        ## 12. ANEXOS
        ### Anexo I: Fichas de trabajo
        ### Anexo II: Lista de verificación
        ### Anexo III: Recursos complementarios

        IMPORTANTE:
        - La situación debe ser REALISTA y APLICABLE en un centro de FP sanitaria
        - Debe integrar perfectamente la metodología seleccionada
        - Debe estar completamente alineada con la normativa LOMLOE y aragonesa
        - Debe ser específica del ámbito sanitario y profesionalizante
        - Incluir aspectos de digitalización y sostenibilidad cuando sea pertinente
        - Considerar la perspectiva de género y diversidad
        - Ser innovadora pero factible con los recursos indicados
        - Genera el documento completo con sus 8 puntos. si es necesaerio puedes abreviar en los puntos 2,3,4 y 5 pero los puntos 6,7 y 8 tienen que estár completos 
        """
        
    
    def _construir_prompt_rubrica(self, datos, situacion):
        """Construye el prompt para generar la rúbrica de evaluación"""
        
        prompt = f"""
        Basándote en la siguiente SITUACIÓN DE APRENDIZAJE que has generado, crea una RÚBRICA DE EVALUACIÓN completa y detallada:

        {situacion[:2000]}...

        ## DATOS PARA LA RÚBRICA:
        **Resultados de Aprendizaje:**
        {chr(10).join(f"- {ra}" for ra in datos.get('resultados_aprendizaje', []))}

        **Criterios de Evaluación:**
        {chr(10).join(f"- {ce}" for ce in datos.get('criterios_evaluacion', []))}

        **Producto Final:** {datos.get('producto_final', '')}

        ## ESTRUCTURA REQUERIDA PARA LA RÚBRICA:

        # RÚBRICA DE EVALUACIÓN

        ## Información General
        - **Situación de Aprendizaje:** [Título]
        - **Módulo:** {datos.get('modulo', '')}
        - **Producto Final:** {datos.get('producto_final', '')}
        - **Instrumento:** Rúbrica analítica
        - **en la calificación final:** [Especificar porcentaje]

        ## Criterios de Evaluación y Niveles de Desempeño

        ### Criterio 1: [Nombre del criterio basado en los CE seleccionados]
        **:** [% sobre nota final]

        | NIVEL | EXCELENTE (4) | SATISFACTORIO (3) | EN DESARROLLO (2) | INSUFICIENTE (1) |
        |-------|---------------|-------------------|-------------------|------------------|
        | **Descripción** | [Descripción detallada del nivel excelente] | [Descripción nivel satisfactorio] | [Descripción nivel en desarrollo] | [Descripción nivel insuficiente] |
        | **Indicadores** | • [Indicador específico] <br> • [Indicador específico] | • [Indicador específico] <br> • [Indicador específico] | • [Indicador específico] <br> • [Indicador específico] | • [Indicador específico] <br> • [Indicador específico] |

        [Repetir para cada criterio identificado - mínimo 4-6 criterios]

        ## Competencias Transversales

        ### Competencias Profesionales
        [Evaluar las competencias profesionales seleccionadas]

        ### Competencias Personales y Sociales  
        [Evaluar las competencias personales y sociales seleccionadas]

        ## Evaluación del Proceso

        ### Participación y Actitud (10%)
        | EXCELENTE | SATISFACTORIO | EN DESARROLLO | INSUFICIENTE |
        |-----------|---------------|---------------|--------------|
        | [Descripción] | [Descripción] | [Descripción] | [Descripción] |

        ### Trabajo en Equipo (10%)
        | EXCELENTE | SATISFACTORIO | EN DESARROLLO | INSUFICIENTE |
        |-----------|---------------|---------------|--------------|
        | [Descripción] | [Descripción] | [Descripción] | [Descripción] |

        ## Cálculo de la Calificación Final

        **Fórmula de cálculo:**
        - Criterio 1: ___ × % = ___
        - Criterio 2: ___ × % = ___
        - [...]
        - **NOTA FINAL = Σ (Puntuación)**

        ## Escala de Calificación
        - **EXCELENTE (9-10):** Supera ampliamente los objetivos
        - **SATISFACTORIO (7-8):** Alcanza completamente los objetivos  
        - **EN DESARROLLO (5-6):** Alcanza parcialmente los objetivos
        - **INSUFICIENTE (0-4):** No alcanza los objetivos mínimos

        ## Observaciones y Feedback
        **Espacio para comentarios del evaluador:**
        - Fortalezas observadas:
        - Áreas de mejora:
        - Recomendaciones para el desarrollo profesional:

        ## Autoevaluación del Estudiante
        [Incluir apartado para que el estudiante reflexione sobre su propio aprendizaje]

        IMPORTANTE:
        - La rúbrica debe estar perfectamente alineada con los resultados de aprendizaje y criterios de evaluación seleccionados
        - Debe ser específica y observable (evitar términos vagos)
        - Debe incluir indicadores cuantitativos y cualitativos
        - Debe permitir evaluación formativa y sumativa
        - Debe ser comprensible para estudiantes y profesores
        - Incluir aspectos del ámbito sanitario específico
        """
        
        return prompt
