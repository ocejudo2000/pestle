import openai
import streamlit as st
import pandas as pd
from pptx import Presentation
from pptx.util import Inches
import os

# Configura tu API key para OpenAI
openai_api_key = st.secrets["mykey"]
openai.api_key = openai_api_key

def generar_resumen_pestle(nombre_empresa, caracteres_resumen):
    dimensiones_pestle = ["Político", "Económico", "Sociocultural", "Tecnológico", "Legal", "Ecológico"]
    resumen_pestle = {}
    competidores = None  # Placeholder for now

    for dim in dimensiones_pestle:
        prompt = f"Genera un resumen en formato bullet point sobre el aspecto {dim} alrededor de la empresa {nombre_empresa} en {caracteres_resumen} caracteres. Además, dime quiénes son sus principales competidores:"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=caracteres_resumen
        )
        resumen_pestle[dim] = response.choices[0].text.strip().split("\n")

    return resumen_pestle, competidores

# Interfaz Streamlit
st.title("Análisis PESTLE")
nombre_empresa = st.text_input("Ingresa el nombre de la Empresa:")
caracteres_resumen = st.slider("Cantidad de caracteres para resumir por dimensión PESTLE:", 50, 500, 250)

if st.button("Generar Resumen PESTLE"):
    resumenes, competidores = generar_resumen_pestle(nombre_empresa, caracteres_resumen)
    for dim, resumen in resumenes.items():
        st.write(f"**{dim}**")
        st.table(pd.DataFrame({"Resumen": resumen}))

    export_option = st.selectbox("¿Quieres exportar los resúmenes?", ["No", "Excel", "PowerPoint"])

    if export_option == "Excel":
        df = pd.DataFrame(list(resumenes.items()), columns=["Aspect", "Summary"])
        df.to_excel("resumenes_pestle.xlsx", index=False)

        with open("resumenes_pestle.xlsx", "rb") as f:
            st.download_button("Descargar Excel", f.read(), file_name="resumenes_pestle.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    elif export_option == "PowerPoint":
        prs = Presentation()
        for dim, resumen in resumenes.items():
            slide = prs.slides.add_slide(prs.slide_layouts[1])
            title = slide.shapes.title
            title.text = dim
            content = slide.shapes.placeholders[1]
            for point in resumen:
                p = content.text = content.text + "\n" + point

        prs.save("resumenes_pestle.pptx")
        
        with open("resumenes_pestle.pptx", "rb") as f:
            st.download_button("Descargar PowerPoint", f.read(), file_name="resumenes_pestle.pptx", mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")

