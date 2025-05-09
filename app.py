import streamlit as st
import fitz
import pandas as pd
from extractor.parser import extract_invoice_data

def extract_text_from_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        return "\n".join(page.get_text() for page in doc)

st.set_page_config(page_title="Invoice Extractor", layout="centered")
st.title("📄 Invoice Extractor using Gemini API")

uploaded_files = st.file_uploader("Upload invoice PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.info("Processing invoices...")
    results = []

    for file in uploaded_files:
        text = extract_text_from_pdf(file)
        data = extract_invoice_data(text)
        data["archivo"] = file.name
        results.append(data)

    df = pd.DataFrame(results)
    st.success("✅ Extraction complete!")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "invoices.csv", "text/csv")