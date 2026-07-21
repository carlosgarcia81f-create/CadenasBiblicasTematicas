# generador_html.py
import pandas as pd
from utilidades import limpiar_texto_biblico

def crear_html_estudio(df_estudio, titulo_tema):
    """
    Genera un archivo HTML responsivo que se adapta automáticamente 
    a la pantalla de cualquier celular o tablet.
    """
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Estudio: {titulo_tema}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #0F172A;
            color: #F8FAFC;
            margin: 0;
            padding: 15px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
        }}
        .titulo-estudio {{
            color: #60A5FA;
            font-size: 22px;
            font-weight: bold;
            text-align: center;
            border-bottom: 2px solid #3B82F6;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .subtema-titulo {{
            color: #2DD4BF;
            font-size: 18px;
            font-weight: bold;
            margin-top: 25px;
            margin-bottom: 10px;
            border-bottom: 1px solid #0D9488;
            padding-bottom: 4px;
        }}
        .idea-titulo {{
            color: #FBBF24;
            font-size: 15px;
            font-weight: bold;
            margin-top: 15px;
            margin-bottom: 8px;
        }}
        .verso-contenedor {{
            background-color: rgba(148, 163, 184, 0.1);
            padding: 12px 15px;
            border-radius: 8px;
            border-left: 4px solid #94A3B8;
            margin-bottom: 12px;
            font-size: 15px;
        }}
        .verso-contenedor-idea {{
            background-color: rgba(245, 158, 11, 0.12);
            padding: 12px 15px;
            border-radius: 8px;
            border-left: 4px solid #F59E0B;
            margin-bottom: 12px;
            font-size: 15px;
        }}
        .cita {{
            font-weight: bold;
            color: #93C5FD;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="titulo-estudio">📖 ESTUDIO: {titulo_tema.upper()}</div>
"""

    # Recorremos la estructura de Subtemas, Ideas y Versículos
    for subtema, grupo_subtema in df_estudio.groupby('Subtema', sort=False):
        subtema_str = str(subtema).strip() if pd.notna(subtema) and str(subtema).strip() not in ["", "nan", "None"] else "ESTUDIO GENERAL"
        html_content += f'<div class="subtema-titulo">🔹 {subtema_str.upper()}</div>\n'
        
        idea_actual = None
        
        for _, fila in grupo_subtema.iterrows():
            idea_fila = str(fila['Ideas']).strip() if pd.notna(fila['Ideas']) else ""
            tiene_idea = idea_fila not in ["", "nan", "None"]
            
            cita = f"{fila['Libro']} {fila['Capítulo']}:{fila['Versículo']}"
            texto_verso = limpiar_texto_biblico(fila['Texto_Verso'])
            
            if tiene_idea:
                if idea_fila != idea_actual:
                    idea_actual = idea_fila
                    html_content += f'<div class="idea-titulo">🔸 {idea_actual}</div>\n'
                
                html_content += f"""
                <div class="verso-contenedor-idea">
                    <span class="cita">📖 {cita}</span> — {texto_verso}
                </div>
                """
            else:
                idea_actual = None
                html_content += f"""
                <div class="verso-contenedor">
                    <span class="cita">📖 {cita}</span> — {texto_verso}
                </div>
                """

    html_content += """
    </div>
</body>
</html>
"""
    return html_content.encode('utf-8')
