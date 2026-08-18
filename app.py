import streamlit as st
import pandas as pd
from generador_pdf import crear_pdf_estudio
from utilidades import limpiar_texto_biblico
from generador_html import crear_html_estudio

# Configuración de la página web
st.set_page_config(page_title="Mi Estudio Bíblico Devocional", page_icon="📖", layout="centered")

# Estilos visuales personalizados (Estilo Biblia de Estudio)
st.markdown("""
    <style>
    .tema-titulo { color: #3B82F6; font-size: 28px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .subtema-titulo { color: #0D9488; font-size: 20px; font-weight: bold; margin-top: 30px; border-bottom: 2px solid #0D9488; padding-bottom: 5px; }
    .idea-titulo { color: #F59E0B; font-size: 16px; font-weight: bold; margin-top: 15px; margin-left: 15px; }
    
    /* Contenedor General (Gris neutro con texto oscuro o claro adaptativo) */
    .verso-contenedor { 
        background-color: rgba(148, 163, 184, 0.1); 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 4px solid #94A3B8; 
        margin-bottom: 10px; 
        margin-left: 25px;
    }
    
    /* Contenedor de Ideas (Fondo ámbar translúcido que reacciona bien al fondo negro o blanco) */
    .verso-contenedor-idea { 
        background-color: rgba(245, 158, 11, 0.15); 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 4px solid #F59E0B; 
        margin-bottom: 10px; 
        margin-left: 35px;
    }
    
    .cita { font-weight: bold; color: #60A5FA; }
    .leyenda-adicional { font-style: italic; color: #94A3B8; margin-left: 25px; margin-top: 15px; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 1. CARGAR LA BASE DE DATOS DESDE GOOGLE SHEETS
# =====================================================================
SHEET_ID = '1vUPyJOzAWLt85v_ZtjD6z-hu72_0shOJsoDnLHH_D0k' #TU_ID_DE_GOOGLE_SHEET_AQUI
SHEET_NAME = "BD"  # Asegúrate de usar el nombre exacto de la pestaña

URL_GSHEETS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

@st.cache_data(ttl=300)
def cargar_datos():
    try:
        df = pd.read_csv(URL_GSHEETS)
        
        # Limpieza de nombres de columnas (quita espacios extras si los hay)
        df.columns = df.columns.str.strip()
        
        if 'Capítulo' in df.columns:
            df['Capítulo'] = pd.to_numeric(df['Capítulo'], errors='coerce').fillna(0).astype(int).astype(str)
            
        if 'Versículo' in df.columns:
            df['Versículo'] = df['Versículo'].astype(str)
            
        return df
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        return None

df = cargar_datos()
### Hasta aquí ok 1 

if df is not None:
    st.title("📖 Sistema de Cadenas Devocionales")
    st.write("Herramienta de estudio bíblico personalizado para el discipulado.")

    # 2. Buscador en la barra lateral
    lista_temas = sorted(df['Tema_Principal'].dropna().unique())
    tema_seleccionado = st.sidebar.selectbox("Selecciona un Tema de Estudio:", lista_temas)

    if tema_seleccionado:
        # Filtrar registros y asegurar el orden secuencial por ID_REF
        resultado = df[df['Tema_Principal'] == tema_seleccionado].sort_values(by=['ID_REF'])
        
        # Título Principal del Estudio
        st.markdown(f'<div class="tema-titulo">ESTUDIO: {tema_seleccionado.upper()}</div>', unsafe_allow_html=True)
        st.markdown(f"**Total de pasajes en este estudio:** {len(resultado)}")
        
        # =====================================================================
        # RENDERIZADO EN CASCADA CON AUTOAGRUPAMIENTO DE SUBTEMAS E IDEAS (CORREGIDO)
        # =====================================================================
        for subtema, grupo_subtema in resultado.groupby('Subtema', sort=False):
            subtema_str = str(subtema).strip() if pd.notna(subtema) else "ESTUDIO GENERAL"
            st.markdown(f'<div class="subtema-titulo">🔹 {subtema_str.upper()}</div>', unsafe_allow_html=True)
            
            # Aseguramos limpiar espacios en blanco extras de toda la columna 'Ideas' para evitar duplicados visuales
            grupo_subtema['Ideas'] = grupo_subtema['Ideas'].astype(str).str.strip()
            
            # Separar versos que tienen una idea asociada de los que no (filtramos los "nan" o vacíos)
            con_idea = grupo_subtema[(grupo_subtema['Ideas'].notna()) & (grupo_subtema['Ideas'] != "") & (grupo_subtema['Ideas'] != "nan")]
            sin_idea = grupo_subtema[(grupo_subtema['Ideas'].isna()) | (grupo_subtema['Ideas'] == "") | (grupo_subtema['Ideas'] == "nan")]
            
            # -----------------------------------------------------------------
            # BLOQUE 1: Versículos con ideas específicas (AUTOAGRUPADOS)
            # -----------------------------------------------------------------
            idea_actual = None  # Reiniciamos el control de la idea al cambiar de subtema
            
            for _, fila in con_idea.iterrows():
                idea_fila = fila['Ideas'] # Ya viene limpia de la línea anterior
                
                # EFECTÚA EL AUTOAGRUPAMIENTO: Compara de forma estricta textos limpios
                if idea_fila != idea_actual:
                    idea_actual = idea_fila
                    st.markdown(f'<div class="idea-titulo">🔸 {idea_actual}</div>', unsafe_allow_html=True)
                
                # Datos del pasaje
                cita = f"{fila['Libro']} {fila['Capítulo']}:{fila['Versículo']}"
                texto_verso = limpiar_texto_biblico(fila['Texto_Verso'])
                
                # Renderiza el versículo
                st.markdown(f"""
                    <div class="verso-contenedor-idea">
                        <span class="cita">📖 {cita}</span> — {texto_verso}
                    </div>
                """, unsafe_allow_html=True)
                
            # -----------------------------------------------------------------
            # BLOQUE 2: Versículos adicionales del subtema (Soporte general)
            # -----------------------------------------------------------------
            if not sin_idea.empty:
                if not con_idea.empty:
                    st.markdown('<div class="leyenda-adicional">[Versículos adicionales del subtema:]</div>', unsafe_allow_html=True)
                
                for _, fila in sin_idea.iterrows():
                    cita = f"{fila['Libro']} {fila['Capítulo']}:{fila['Versículo']}"
                    texto_verso = limpiar_texto_biblico(fila['Texto_Verso'])
                    
                    st.markdown(f"""
                        <div class="verso-contenedor">
                            <span class="cita">📖 {cita}</span> — {texto_verso}
                        </div>
                    """, unsafe_allow_html=True)
if tema_seleccionado:
    resultado = df[df['Tema_Principal'] == tema_seleccionado].sort_values(by=['ID_REF'])
    
    # -----------------------------------------------------------------
    # BOTONES DE DESCARGA (PDF Carta e HTML Móvil)
    # -----------------------------------------------------------------
    col1, col2 = st.columns(2)
    
    with col1:
        # Opción 1: PDF para Impresión
        bytes_pdf = crear_pdf_estudio(resultado, tema_seleccionado)
        st.download_button(
            label="📄 PDF para Imprimir (Carta)",
            data=bytes_pdf,
            file_name=f"Estudio_{tema_seleccionado.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
    with col2:
        # Opción 2: HTML Responsivo para Móvil
        bytes_html = crear_html_estudio(resultado, tema_seleccionado)
        st.download_button(
            label="📱 Versión Móvil (.html)",
            data=bytes_html,
            file_name=f"Estudio_{tema_seleccionado.replace(' ', '_')}_movil.html",
            mime="text/html",
            use_container_width=True
        )
