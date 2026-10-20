import pandas as pd

def generar_markdown(df_tema, nombre_tema):
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
                # Condicional de Notas: solo si la celda tiene contenido real
                if 'Notas' in fila and pd.notna(fila['Notas']):
                    nota_texto = str(fila['Notas']).strip()
                    if nota_texto and nota_texto.lower() not in ["nan", "none", ""]:
                        md.append(f"> [!NOTE]")
                        md.append(f"> > 💡 **Nota:** *{nota_texto}*")
                    
                md.append("") # Línea en blanco
                
    return "\n".join(md)
