# generador_pdf.py
import pandas as pd
from fpdf import FPDF

class PDFEstudio(FPDF):
    def __init__(self, titulo_estudio):
        super().__init__()
        self.titulo_estudio = titulo_estudio

    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(30, 58, 138)  # Azul
        self.cell(0, 10, f'ESTUDIO BÍBLICO: {self.titulo_estudio.upper()}', border=0, ln=True, align='C')
        self.set_draw_color(200, 200, 200)
        self.line(10, 20, 200, 20)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

def crear_pdf_estudio(df_estudio, titulo_tema):
    """
    Función principal del módulo:
    Recibe un DataFrame de Pandas y el título del tema,
    y devuelve los bytes del archivo PDF generado.
    """
    pdf = PDFEstudio(titulo_tema)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Recorremos la estructura de Subtemas, Ideas y Versículos
    for subtema, grupo_subtema in df_estudio.groupby('Subtema', sort=False):
        subtema_str = str(subtema).strip() if pd.notna(subtema) and str(subtema).strip() not in ["", "nan", "None"] else "ESTUDIO GENERAL"
        
        # Formato de Subtema
        pdf.ln(3)
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(13, 148, 136)  # Teal / Verde agua
        pdf.cell(0, 8, f'{subtema_str.upper()}', ln=True)
        pdf.set_draw_color(13, 148, 136)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        
        idea_actual = None
        
        for _, fila in grupo_subtema.iterrows():
            idea_fila = str(fila['Ideas']).strip() if pd.notna(fila['Ideas']) else ""
            tiene_idea = idea_fila not in ["", "nan", "None"]
            
            cita = f"{fila['Libro']} {fila['Capítulo']}:{fila['Versículo']}"
            texto_verso = str(fila['Texto_Verso']).replace('_x000D_', '').strip()
            
            # Imprimir Idea si cambió
            if tiene_idea and idea_fila != idea_actual:
                idea_actual = idea_fila
                pdf.ln(2)
                pdf.set_font('Helvetica', 'B', 10)
                pdf.set_text_color(217, 119, 6)  # Ámbar / Naranja
                pdf.cell(0, 6, f'* {idea_actual}', ln=True)
            elif not tiene_idea:
                idea_actual = None
                
            # Cita en azul y texto del pasaje
            pdf.set_font('Helvetica', 'B', 9)
            pdf.set_text_color(37, 99, 235)
            pdf.write(5, f"[{cita}] ")
            
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(50, 50, 50)
            pdf.write(5, f"{texto_verso}\n\n")
            
    return bytes(pdf.output())
