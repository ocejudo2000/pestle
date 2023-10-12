import openai
import streamlit as st

# Configura tu API key para OpenAI

openai_api_key = st.secrets["mykey"]

openai.api_key = openai_api_key




def generar_resumen_pestle(nombre_empresa, caracteres_resumen):
    dimensiones_pestle = ["Político", "Económico", "Sociocultural", "Tecnológico", "Legal", "Ecológico"]
    resumen_pestle = {}

    for dim in dimensiones_pestle:
        prompt = f"Genera un resumen en formato bullet point sobre el aspecto {dim} de la empresa {nombre_empresa} en {caracteres_resumen} caracteres:"
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-0613",
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