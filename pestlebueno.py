import openai
import streamlit as st
import pandas as pd
from pptx import Presentation
from pptx.util import Inches

# Configura tu API key para OpenAI
openai_api_key = st.secrets["mykey"]
openai.api_key = openai_api_key

def generar_resumen_pestle(nombre_empresa, caracteres_resumen):
    dimensiones_pestle = ["Político", "Económico", "Sociocultural", "Tecnológico", "Legal", "Ecológico"]
    resumen_pestle = {}

    for dim in dimensiones_pestle:
        prompt = f"Genera un resumen en formato bullet point sobre el aspecto {dim} de la empresa {nombre_empresa} en {caracteres_resumen} caracteres:"
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
        st.table({"Resumen": [resumen]})  # Presentación en tabla

    export_option = st.selectbox("¿Quieres exportar los resúmenes?", ["No", "Excel", "PowerPoint"])

    if export_option == "Excel":
        df = pd.DataFrame(list(resumenes.items()), columns=["Aspect", "Summary"])
        df.to_excel('resumenes_pestle.xlsx', index=False)
        st.download_button("Descargar Excel", 'resumenes_pestle.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    elif export_option == "PowerPoint":
        # Generar PowerPoint
        prs = Presentation()
        for dim, resumen in resumenes.items():
            slide_layout = prs.slide_layouts[1]
            slide = prs.slides.add_slide(slide_layout)
            title = slide.shapes.title
            title.text = dim

            content = slide.placeholders[1]
            content.text = resumen

        prs.save('resumenes_pestle.pptx')
        st.download_button("Descargar PowerPoint", 'resumenes_pestle.pptx', "application/vnd.openxmlformats-officedocument.presentationml.presentation")
