import streamlit as st
import pandas as pd

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

# 1. Cargar la Base de Datos
@st.cache_data # Optimiza la app para que no lea el Excel en cada clic
def cargar_datos():
    archivo_excel = "BD_Temas.xlsm"
    try:
        df = pd.read_excel(archivo_excel, sheet_name="BD", engine='openpyxl')
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo BD_Temas.xlsm: {e}")
        return None

df = cargar_datos()

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
        
        # 3. Renderizado con la lógica de tu Colab
        for subtema, grupo_subtema in resultado.groupby('Subtema', sort=False):
            subtema_str = str(subtema).strip() if pd.notna(subtema) else "ESTUDIO GENERAL"
            st.markdown(f'<div class="subtema-titulo">🔹 {subtema_str.upper()}</div>', unsafe_allow_html=True)
            
            # Separar versos con idea y sin idea
            con_idea = grupo_subtema[grupo_subtema['Ideas'].notna() & (grupo_subtema['Ideas'].astype(str).str.strip() != "")]
            sin_idea = grupo_subtema[grupo_subtema['Ideas'].isna() | (grupo_subtema['Ideas'].astype(str).str.strip() == "")]
            
            # Bloque 1: Versículos con ideas específicas
            idea_actual = None
            for _, fila in con_idea.iterrows():
                idea_fila = str(fila['Ideas']).strip()
                if idea_fila != idea_actual:
                    idea_actual = idea_fila
                    st.markdown(f'<div class="idea-titulo">🔸 {idea_actual}</div>', unsafe_allow_html=True)
                
                cita = f"{fila['Libro']} {fila['Capítulo']}:{fila['Versículo']}"
                texto_verso = str(fila['Texto_Verso']).replace('_x000D_', '').strip()
                
                st.markdown(f"""
                    <div class="verso-contenedor-idea">
                        <span class="cita">📖 {cita}</span> — {texto_verso}
                    </div>
                """, unsafe_allow_html=True)
                
            # Bloque 2: Versículos adicionales del subtema
            if not sin_idea.empty:
                if not con_idea.empty:
                    st.markdown('<div class="leyenda-adicional">[Versículos adicionales del subtema:]</div>', unsafe_allow_html=True)
                
                for _, fila in sin_idea.iterrows():
                    cita = f"{fila['Libro']} {fila['Capítulo']}:{fila['Versículo']}"
                    texto_verso = str(fila['Texto_Verso']).replace('_x000D_', '').strip()
                    
                    st.markdown(f"""
                        <div class="verso-contenedor">
                            <span class="cita">📖 {cita}</span> — {texto_verso}
                        </div>
                    """, unsafe_allowed_index=True)
