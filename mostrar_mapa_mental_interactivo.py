import base64
import streamlit.components.v1 as components

def mostrar_mapa_interactivo(texto_markmap, height=550):
    # Codificamos el texto Markdown en Base64 para evitar errores de sintaxis en JS
    b64_markdown = base64.b64encode(texto_markmap.encode('utf-8')).decode('utf-8')
    
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
            .markmap-node text {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
                font-size: 14px !important;
                fill: #1f2937 !important;
            }}
        </style>
        <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-lib@0.15.4/dist/browser/index.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-view@0.15.4/dist/index.js"></script>
    </head>
    <body>
        <svg id="mindmap"></svg>
        <script>
            document.addEventListener("DOMContentLoaded", () => {{
                try {{
                    const {{ Transformer, Markmap, loadCSS, loadJS }} = window.markmap;
                    
                    // Decodificamos de forma segura el texto desde Base64
                    const markdownText = decodeURIComponent(escape(atob("{b64_markdown}")));
                    
                    const transformer = new Transformer();
                    const {{ root, features }} = transformer.transform(markdownText);
                    
                    const {{ styles, scripts }} = transformer.getUsedAssets(features);
                    if (styles) loadCSS(styles);
                    if (scripts) loadJS(scripts, {{ getMarkmap: () => window.markmap }});
                    
                    const mm = Markmap.create('#mindmap', {{
                        initialExpandLevel: 3,
                        duration: 300
                    }}, root);
                    
                    // Forzar encuadre de zoom tras renderizar los nodos
                    setTimeout(() => {{
                        mm.fit();
                    }}, 250);
                    
                    window.addEventListener('resize', () => mm.fit());
                }} catch (e) {{
                    console.error("Error cargando Markmap:", e);
                }}
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=height)
