import json
import streamlit.components.v1 as components

def mostrar_mapa_interactivo(texto_markmap, height=550):
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                width: 100vw;
                height: 100vh;
                overflow: hidden;
                background-color: #ffffff;
            }}
            #mindmap {{
                width: 100vw;
                height: 100vh;
                display: block;
            }}
        </style>
        <!-- Carga de scripts de Markmap y D3 -->
        <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-lib@0.15.4"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-view@0.15.4"></script>
    </head>
    <body>
        <svg id="mindmap"></svg>
        <script>
            document.addEventListener("DOMContentLoaded", () => {{
                try {{
                    const {{ Transformer, Markmap }} = window.markmap;
                    const markdownText = {json.dumps(texto_markmap)};
                    
                    const transformer = new Transformer();
                    const {{ root }} = transformer.transform(markdownText);
                    
                    // Configuración de visualización e inicialización
                    const mm = Markmap.create('#mindmap', {{
                        initialExpandLevel: 3,
                        duration: 300
                    }}, root);
                    
                    // Reajustar encuadre y zoom automáticamente tras renderizar
                    setTimeout(() => {{
                        mm.fit();
                    }}, 200);
                    
                    // Escuchar redimensionamiento de ventana
                    window.addEventListener('resize', () => {{
                        mm.fit();
                    }});
                }} catch (e) {{
                    console.error("Error al cargar Markmap:", e);
                }}
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=height)
