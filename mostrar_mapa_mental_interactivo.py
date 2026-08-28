import json
import streamlit.components.v1 as components

def mostrar_mapa_interactivo(texto_markmap, height=550):
    # Convierte el string de Python a una cadena JSON válida y segura para JS
    markdown_json = json.dumps(texto_markmap)
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                background-color: #ffffff;
            }}
            .markmap {{
                width: 100%;
                height: 100%;
            }}
        </style>
        <!-- Configuración de Markmap para ajustar vista automáticamente -->
        <script>
            window.markmap = {{
                autoFit: true,
                duration: 300
            }};
        </script>
        <!-- Carga de scripts oficiales auto-contenidos -->
        <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@0.15.4"></script>
    </head>
    <body>
        <div class="markmap">
            <script type="text/template">
                {texto_markmap}
            </script>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=height)
