import pandas as pd

def generar_markmap(df_tema, nombre_tema):
    md = []
    # Nivel 1: Tema Principal
    md.append(f"# 📖 {nombre_tema.upper()}\n")
    
    col_subtema = 'Subtema' if 'Subtema' in df_tema.columns else 'SubTema'
    col_idea = 'Ideas' if 'Ideas' in df_tema.columns else 'Idea'
    
    # Nivel 2: Subtemas
    for subtema, df_subtema in df_tema.groupby(col_subtema, sort=False):
        md.append(f"## {subtema}\n")
        
        # Nivel 3: Ideas
        for idea, df_idea in df_subtema.groupby(col_idea, sort=False):
            if pd.notna(idea) and str(idea).strip() != "":
                md.append(f"### {idea}\n")
                indent = "####"
            else:
                indent = "###"
            
            # Nivel 4: Citas Bíblicas y Pasajes
            for _, fila in df_idea.iterrows():
                cita = f"{fila['Libro']} {fila['Capítulo']}:{fila['Versículo']}"
                texto_verso = str(fila['Texto_Verso']).strip()
                
                # Para que el mapa mental no cree nodos gigantescos, acortamos el texto en el nodo principal
                # si es muy largo, pero mantenemos la cita clara.
                md.append(f"{indent} **{cita}** - {texto_verso}")
                
                # Nivel 5: Notas explicativas (Condicional)
                if 'Notas' in fila and pd.notna(fila['Notas']):
                    nota_texto = str(fila['Notas']).strip()
                    if nota_texto and nota_texto.lower() not in ["nan", "none", ""]:
                        md.append(f"{indent}# 💡 *Nota:* {nota_texto}")
                        
                md.append("") # Línea en blanco entre ramas
                
    return "\n".join(md)
