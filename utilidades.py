#Limpiar texto de los versículos
#Quitar llamadas a notas al pie: Eliminar cualquier (A), (B), [a], [b], etc.
#Quitar títulos/subtítulos iniciales: Detectar si el texto comienza con palabras antes del primer número y descartar solo ese encabezado.
#Limpiar los números de versículos (al inicio e intermedios): Borrar los números aislados que van pegados al texto o entre pasajes sin cortar la frase.

import re

def limpiar_texto_biblico(texto):
    if not texto or str(texto).strip() in ["", "nan", "None"]:
        return ""
    
    texto_limpio = str(texto).replace('_x000D_', '').strip()
    
    # 1. Eliminar referencias a notas como (A), (B), [a], [b], (1), [2], etc.
    texto_limpio = re.sub(r'\([A-Za-z0-9]+\)|\[[A-Za-z0-9]+\]', '', texto_limpio)
    
    # 2. Si el texto inicia con un subtítulo antes del primer número (ej: "Doxología final 25 Y a aquel..."),
    # eliminamos lo que esté antes de ese primer número.
    if re.search(r'^\D+\d+', texto_limpio):
        texto_limpio = re.sub(r'^[^\d]+(?=\d+)', '', texto_limpio)
    
    # 3. Eliminar los números de versículos aislados (tanto el inicial como los intermedios del rango)
    # \b\d+\b busca números independientes para no borrar palabras que contengan números.
    texto_limpio = re.sub(r'\b\d+\b', '', texto_limpio)
    
    # 4. Limpiar espacios dobles o residuales que queden al inicio, medio o final
    texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
    
    return texto_limpio
