import streamlit as st
import fitz
import pandas as pd
from extractor.parser import extract_invoice_data

def extract_text_from_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        return "\n".join(page.get_text() for page in doc)

st.set_page_config(page_title="Procesador de Documentos", layout="centered")
st.title("📄 Procesador de Documentos")

uploaded_files = st.file_uploader("Subir Documentos PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.info("Procesando Documentos...")
    results = []

    for file in uploaded_files:
        text = extract_text_from_pdf(file)
        data = extract_invoice_data(text)
        data["archivo"] = file.name
        results.append(data)

    df = pd.DataFrame(results)
    st.success("✅ Extracción completa!")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Descargar CSV", csv, "facturas_extraidas.csv", "text/csv")