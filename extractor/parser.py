import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])



def extract_invoice_data(text: str) -> dict:
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
          You will receive the raw text of an invoice.
          Extract the following fields exactly and return them as a JSON object using these keys:
          - Tipo de Documento (Factura, Boleta  o Nota de Crédito)
          - Numero de Documento de Emisor
          - Nombre de Emisor
          - Numero_factura
          - Numero de Documento de Receptor
          - Nombre de Receptor
          - Tipo de Moneda
          - Forma de Pago
          - Fecha_emision
          - sub_total
          - valor
          - ISC
          - IGV
          - Otros Cargos
          - Importe Total

          Respond only with valid JSON and do not include any Markdown formatting like ```json and also
          respond with numbers without quotes and without thousand separators (e.g. 8000.00 not "8,000.00").
          Example:
          {{
            "tipo_documento": "Factura",
            "numero_documento_emisor": "123456789",
            "nombre_emisor": "Empresa ABC S.A.C.",
            "numero_documento_receptor": "987654321",
            "nombre_receptor": "Cliente XYZ",
            "tipo_moneda": "Soles",
            "forma_pago": "Contado",
            "fecha_emision": "2023-09-15",
            "sub_total": 150.00,
            "valor": 150.00,
            "ISC": 0.00,
            "IGV": 18.00,
            "Otros Cargos": 0.00,
            "importe_total": 168
          }}
          

          Invoice text:
          {text}"""

    response = model.generate_content(prompt)

    raw_output = response.text.strip()

    # Remove triple backticks if present
    if raw_output.startswith("```json") and raw_output.endswith("```"):
        raw_output = raw_output[7:-3].strip()

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError as e:
        print("JSON parsing error:", e)
        print("Raw Gemini output:\n", raw_output)
        return {}