"""import openai
import streamlit as st

# Configura tu API key para OpenAI

openai_api_key = st.secrets["mykey"]

openai.api_key = openai_api_key




def generar_resumen_pestle(nombre_empresa, caracteres_resumen):
    dimensiones_pestle = ["Político", "Económico", "Sociocultural", "Tecnológico", "Legal", "Ecológico"]
    resumen_pestle = {}

    for dim in dimensiones_pestle:
        prompt = f"Genera un resumen en formato bullet point sobre el aspecto {dim} de la empresa {nombre_empresa} en {caracteres_resumen} caracteres sin final cortado, pon cada aspecto en una tabla. Adicional Muestra a sus principales competidores en una tabla:"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=caracteres_resumen
        )
        resumen_pestle[dim] = response.choices[0].text.strip()

    return resumen_pestle

# Interfaz Streamlit
st.title("Análisis PESTLE")
nombre_empresa = st.text_input("Ingresa el nombre de la Empresa:")

caracteres_resumen = st.slider("Cantidad de caracteres para resumir por dimensión PESTLE:", 50, 500, 250)

if st.button("Generar Resumen PESTLE"):
    resumenes = generar_resumen_pestle(nombre_empresa, caracteres_resumen)
    for dim, resumen in resumenes.items():
        st.write(f"**{dim}**")
        st.write(resumen)

export_option = st.selectbox("¿Quieres exportar los resúmenes?", ["No", "Excel", "PowerPoint"])

if export_option == "Excel":
    st.write("Funcionalidad para exportar a Excel aún no implementada.")

elif export_option == "PowerPoint":
    st.write("Funcionalidad para exportar a PowerPoint aún no implementada.")
    """

import openai
import streamlit as st
import pandas as pd  # New: For Excel Export
from pptx import Presentation  # New: For PowerPoint Export

# Configure your OpenAI API key
openai_api_key = st.secrets["mykey"]
openai.api_key = openai_api_key

# Function to generate PESTLE summary
def generar_resumen_pestle(nombre_empresa, caracteres_resumen):
    dimensiones_pestle = ["Político", "Económico", "Sociocultural", "Tecnológico", "Legal", "Ecológico"]
    resumen_pestle = {}
    for dim in dimensiones_pestle:
        prompt = f"Genera un resumen en formato bullet point sobre el aspecto {dim} de la empresa {nombre_empresa} en {caracteres_resumen} caracteres  sin final cortado, pon cada aspecto en una tabla. Adicional Muestra a sus principales competidores en una tabla:"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=caracteres_resumen
        )
        resumen_pestle[dim] = response.choices[0].text.strip()
    return resumen_pestle

# Streamlit Interface
st.title("Análisis PESTLE")
nombre_empresa = st.text_input("Ingresa el nombre de la Empresa:")
caracteres_resumen = st.slider("Cantidad de caracteres para resumir por dimensión PESTLE:", 50, 500, 250)

if st.button("Generar Resumen PESTLE"):
    resumenes = generar_resumen_pestle(nombre_empresa, caracteres_resumen)
    for dim, resumen in resumenes.items():
        st.write(f"**{dim}**")
        st.write(resumen)
    
    # New: Export to Excel
    df = pd.DataFrame(list(resumenes.items()), columns=['Dimension', 'Resumen'])
    with st.download_button("Descargar Excel", "resumenes_pestle.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
        df.to_excel("resumenes_pestle.xlsx", index=False)

    # New: Export to PowerPoint
    prs = Presentation()
    for dim, resumen in resumenes.items():
        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout, dim, '')
        content = slide.shapes.title
        content.text = resumen
    prs.save("resumenes_pestle.pptx")
    with st.download_button("Descargar PowerPoint", "resumenes_pestle.pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation"):
        prs.save("resumenes_pestle.pptx")
