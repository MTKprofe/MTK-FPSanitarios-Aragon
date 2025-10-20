from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import io
from datetime import datetime
import re

def generate_pdf(situacion_content, rubrica_content, parametros):
    """Genera un PDF con la situación de aprendizaje y rúbrica"""
    
    # Crear buffer en memoria
    buffer = io.BytesIO()
    
    # Crear documento PDF
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Obtener estilos
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1f77b4')
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#2c3e50')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    # Lista de elementos del documento
    story = []
    
    # Título principal
    story.append(Paragraph("SITUACIÓN DE APRENDIZAJE", title_style))
    story.append(Paragraph("Formación Profesional Sanitaria - Aragón", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Información del ciclo
    info_data = [
        ['Ciclo Formativo:', f"{parametros.get('nivel', '')} - {parametros.get('ciclo', '')}"],
        ['Módulo:', parametros.get('modulo', '')],
        ['Metodología:', parametros.get('metodologia', '')],
        ['Duración:', parametros.get('duracion', '')],
        ['Fecha de generación:', datetime.now().strftime('%d/%m/%Y %H:%M')]
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4fd')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 20))
    
    # Convertir el contenido markdown a párrafos para PDF
    story.extend(_markdown_to_paragraphs(situacion_content, styles, normal_style, subtitle_style))
    
    # Nueva página para la rúbrica
    from reportlab.platypus import PageBreak
    story.append(PageBreak())
    
    # Título de la rúbrica
    story.append(Paragraph("RÚBRICA DE EVALUACIÓN", title_style))
    story.append(Spacer(1, 20))
    
    # Convertir rúbrica
    story.extend(_markdown_to_paragraphs(rubrica_content, styles, normal_style, subtitle_style))
    
    # Footer
    story.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#7f8c8d')
    )
    
    story.append(Paragraph(
        "Gobierno de Aragón - Departamento de Educación, Cultura y Deporte<br/>Generado con Asistente IA para FP Sanitaria",
        footer_style
    ))
    
    # Construir PDF
    doc.build(story)
    
    # Obtener el contenido del buffer
    pdf_content = buffer.getvalue()
    buffer.close()
    
    return pdf_content

def _markdown_to_paragraphs(markdown_content, styles, normal_style, subtitle_style):
    """Convierte contenido markdown básico a párrafos de ReportLab"""
    
    paragraphs = []
    lines = markdown_content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            paragraphs.append(Spacer(1, 6))
            continue
            
        # Títulos con #
        if line.startswith('# '):
            title_text = line[2:].strip()
            paragraphs.append(Paragraph(title_text, subtitle_style))
            paragraphs.append(Spacer(1, 12))
            
        elif line.startswith('## '):
            subtitle_text = line[3:].strip()
            h3_style = ParagraphStyle(
                'H3Style',
                parent=subtitle_style,
                fontSize=12,
                spaceAfter=8
            )
            paragraphs.append(Paragraph(subtitle_text, h3_style))
            
        elif line.startswith('### '):
            h4_text = line[4:].strip()
            h4_style = ParagraphStyle(
                'H4Style',
                parent=normal_style,
                fontSize=11,
                fontName='Helvetica-Bold',
                spaceAfter=6
            )
            paragraphs.append(Paragraph(h4_text, h4_style))
            
        elif line.startswith('- '):
            # Lista con viñetas
            bullet_text = line[2:].strip()
            paragraphs.append(Paragraph(f"• {bullet_text}", normal_style))
            
        elif line.startswith('**') and line.endswith('**'):
            # Texto en negrita
            bold_text = line[2:-2]
            bold_style = ParagraphStyle(
                'BoldStyle',
                parent=normal_style,
                fontName='Helvetica-Bold'
            )
            paragraphs.append(Paragraph(bold_text, bold_style))
            
        else:
            # Texto normal
            if len(line) > 0:
                paragraphs.append(Paragraph(line, normal_style))
    
    return paragraphs
