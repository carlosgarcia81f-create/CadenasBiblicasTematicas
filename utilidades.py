#Limpiar texto de los versículos
#Quitar llamadas a notas al pie: Eliminar cualquier (A), (B), [a], [b], etc.
#Quitar títulos/subtítulos iniciales: Detectar si el texto comienza con palabras antes del primer número y descartar solo ese encabezado.
#Limpiar los números de versículos (al inicio e intermedios): Borrar los números aislados que van pegados al texto o entre pasajes sin cortar la frase.

import re

def limpiar_texto_biblico(texto):
    if not texto or str(texto).strip() in ["", "nan", "None"]:
        return ""
    
    texto_limpio = str(texto).replace('_x000D_', '').strip()
    
    # 1. Eliminar referencias a notas como (A), (B), [a], [b], (1), [2], etc.
    texto_limpio = re.sub(r'\([A-Za-z0-9]+\)|\[[A-Za-z0-9]+\]', '', texto_limpio)
    
    # 2. Si el texto inicia con un subtítulo antes del primer número (ej: "Doxología final 25 Y a aquel..."),
    # eliminamos lo que esté antes de ese primer número.
    if re.search(r'^\D+\d+', texto_limpio):
        texto_limpio = re.sub(r'^[^\d]+(?=\d+)', '', texto_limpio)
    
    # 3. Eliminar los números de versículos aislados (tanto el inicial como los intermedios del rango)
    # \b\d+\b busca números independientes para no borrar palabras que contengan números.
    texto_limpio = re.sub(r'\b\d+\b', '', texto_limpio)
    
    # 4. Limpiar espacios dobles o residuales que queden al inicio, medio o final
    texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
    
    return texto_limpio

def sanitizar_para_pdf(texto):
    if not texto:
        return ""
    
    # Reemplazamos los caracteres tipográficos más comunes por versiones estándar
    reemplazos = {
        '—': '-',    # Raya / Guion largo
        '–': '-',    # Guion medio
        '“': '"',    # Comilla doble apertura
        '”': '"',    # Comilla doble cierre
        '‘': "'",    # Comilla simple apertura
        '’': "'",    # Comilla simple cierre
        '…': '...',  # Puntos suspensivos
        'É': 'É',    # Por si hay temas de acentos en fuentes básicas
    }
    
    texto_limpio = str(texto)
    for origen, destino in reemplazos.items():
        texto_limpio = texto_limpio.replace(origen, destino)
        
    # Forzamos la conversión a Latin-1 ignorando cualquier otro carácter extraño que se colara
    return texto_limpio.encode('latin-1', 'replace').decode('latin-1')

def generar_markdown_notion(df_tema, nombre_tema):
    md = []
    # Título Principal del Estudio (Heading 1 en Notion)
    md.append(f"# ESTUDIO: {nombre_tema.upper()}\n")
    md.append(f"**Total de pasajes:** {len(df_tema)}\n")
    
    # Agrupamos por Subtema
    for subtema, df_subtema in df_tema.groupby('Subtema', sort=False):
        md.append(f"## ◆ {subtema}\n")
        
        # Agrupamos por Idea (si la hay)
        for idea, df_idea in df_subtema.groupby('Ideas', sort=False):
            if pd.notna(idea) and str(idea).strip() != "":
                md.append(f"### ◆ {idea}\n")
            
            for _, fila in df_idea.iterrows():
                cita = f"{fila['Libro']} {fila['Capítulo']}:{fila['Versículo']}"
                texto_verso = fila['Texto_Verso']
                
                # Formato estilo cita de Notion (Quote Block)
                md.append(f"> 📖 **{cita}** — {texto_verso}\n")
                
                # Si hay notas personales, se agregan como sub-bloque indented o cursiva
                if 'Notas' in fila and pd.notna(fila['Notas']) and str(fila['Notas']).strip() != "":
                    md.append(f"> *💡 Nota: {fila['Notas']}*\n")
                    
                md.append("") # Línea en blanco
                
    return "\n".join(md)
