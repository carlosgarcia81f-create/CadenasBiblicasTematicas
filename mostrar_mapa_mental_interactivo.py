import json
import streamlit.components.v1 as components

def mostrar_mapa_interactivo(texto_markmap, height=550):
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
                width: 100vw;
                height: 100vh;
                overflow: hidden;
                background-color: #ffffff;
            }}
            #mindmap {{
                width: 100%;
                height: 100%;
                display: block;
            }}
            /* Asegura visibilidad y tipografía limpia en los nodos SVG */
            .markmap-node text {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
                font-size: 14px !important;
                fill: #1f2937 !important;
            }}
        </style>
        <!-- Librerías con soporte completo para transform y estilos -->
        <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-lib@0.15.4/dist/browser/index.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-view@0.15.4/dist/index.js"></script>
    </head>
    <body>
        <svg id="mindmap"></svg>
        <script>
            document.addEventListener("DOMContentLoaded", async () => {{
                try {{
                    const {{ Transformer, Markmap, loadCSS, loadJS }} = window.markmap;
                    const markdownText = {markdown_json};
                    
                    const transformer = new Transformer();
                    const {{ root, features }} = transformer.transform(markdownText);
                    
                    // Cargar estilos y scripts requeridos por el contenido transformado
                    const {{ styles, scripts }} = transformer.getUsedAssets(features);
                    if (styles) loadCSS(styles);
                    if (scripts) loadJS(scripts, {{ getMarkmap: () => window.markmap }});
                    
                    const mm = Markmap.create('#mindmap', {{
                        initialExpandLevel: 3,
                        duration: 300
                    }}, root);
                    
                    // Reajustar centrado tras inyectar fuentes y estilos
                    setTimeout(() => {{
                        mm.fit();
                    }}, 300);
                    
                    window.addEventListener('resize', () => {{
                        mm.fit();
                    }});
                }} catch (e) {{
                    console.error("Error al renderizar Markmap:", e);
                }}
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=height)
