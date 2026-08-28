import streamlit.components.v1 as components

def mostrar_mapa_interactivo(texto_markmap, height=500):
    """
    Renders an interactive Markmap SVG directly inside the Streamlit app.
    """
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
            #mindmap {{
                width: 100%;
                height: 100%;
            }}
        </style>
        <!-- Librerías oficiales de Markmap vía CDN -->
        <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-lib@0.15.4/dist/browser/index.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-view@0.15.4/dist/index.js"></script>
    </head>
    <body>
        <svg id="mindmap"></svg>
        <script>
            const {{ Markmap, loadCSS, loadJS }} = window.markmap;
            const markdownText = `{texto_markmap.replace("`", "'")}`;
            
            const {{ root }} = window.markmap.Transformer ? 
                new window.markmap.Transformer().transform(markdownText) : 
                window.markmap.transform(markdownText);
                
            Markmap.create('#mindmap', null, root);
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=height)
