import pandas as pd

def generar_markmap(df_tema, nombre_tema):
    md = []
    
    # Encabezado Frontmatter para editores compatibles (Obsidian, VS Code, etc.)
    md.append("---")
    md.append("markmap:")
    md.append("  initialExpandLevel: 3")
    md.append("---\n")
    
    # Nivel 1: Tema Principal
    md.append(f"# 📖 {nombre_tema.upper()}\n")
    
    col_subtema = 'Subtema' if 'Subtema' in df_tema.columns else 'SubTema'
    col_idea = 'Ideas' if 'Ideas' in df_tema.columns else 'Idea'
    
    # Nivel 2: Subtemas
    for subtema, df_subtema in df_tema.groupby(col_subtema, sort=False):
        md.append(f"## {subtema}\n")
        
        # Agrupamos por Idea permitiendo valores nulos
        for idea, df_idea in df_subtema.groupby(col_idea, sort=False, dropna=False):
            
            # CASO A: La fila SÍ tiene una Idea
            if pd.notna(idea) and str(idea).strip() != "" and str(idea).strip().lower() != "nan":
                md.append(f"### {idea}\n")
                indent_pasaje = "####" # Pasaje en Nivel 4
                indent_nota = "#####"  # Nota en Nivel 5
            
            # CASO B: La fila NO tiene Idea (celda vacía)
            else:
                indent_pasaje = "###"  # Pasaje en Nivel 3 directo
                indent_nota = "####"   # Nota en Nivel 4
            
            # Renderizamos los pasajes
            for _, fila in df_idea.iterrows():
                cita = f"{fila['Libro']} {fila['Capítulo']}:{fila['Versículo']}"
                texto_verso = str(fila['Texto_Verso']).strip()
                
                md.append(f"{indent_pasaje} **{cita}** - {texto_verso}")
                
                # Renderizamos Notas Explicativas (si existen)
                if 'Notas' in fila and pd.notna(fila['Notas']):
                    nota_texto = str(fila['Notas']).strip()
                    if nota_texto and nota_texto.lower() not in ["nan", "none", ""]:
                        md.append(f"{indent_nota} 💡 *Nota:* {nota_texto}")
                        
                md.append("")
                
    return "\n".join(md)


def crear_html_markmap(texto_markmap, nombre_tema):
    """
    Genera una página HTML completa, multicolor e interactiva que abre en el Nivel 3.
    """
    html_plantilla = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mapa Mental - {nombre_tema}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        html, body {{
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            font-family: sans-serif;
            background-color: #ffffff;
        }}
        .markmap {{
            width: 100vw;
            height: 100vh;
        }}
    </style>
    <!-- Configuración previa para forzar el nivel de expansión a Nivel 3 -->
    <script>
        window.markmap = {{
            autoFit: true,
            duration: 300,
            initialExpandLevel: 3
        }};
    </script>
    <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@0.15.4"></script>
</head>
<body>
    <div class="markmap">
        <script type="text/template">
{texto_markmap}
        </script>
    </div>
</body>
</html>"""
    return html_plantilla
