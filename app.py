import streamlit as st
import pandas as pd
import requests
import time
import hmac
import hashlib
import os

st.title("📊 Mi Panel de Binance Real")

# USAMOS SOLO VARIABLES DE ENTORNO (configuradas en Render)
api_key = os.environ.get("BINANCE_API_KEY")
secret_key = os.environ.get("BINANCE_SECRET_KEY")

if not api_key or not secret_key:
    st.error("Error: Las variables de entorno no están configuradas correctamente en Render.")
    st.stop()

st.write("Conectado exitosamente a la API.")

# Lógica de conexión (Simplificada)
base_url = "https://api.binance.com"
endpoint = "/api/v3/account"
timestamp = int(time.time() * 1000)

query_string = f"timestamp={timestamp}"
signature = hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

url = f"{base_url}{endpoint}?{query_string}&signature={signature}"
headers = {"X-MBX-APIKEY": api_key}

try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        st.success("¡Conexión exitosa con Binance!")
        st.json(response.json()) # Esto mostrará tus datos básicos
    else:
        st.error(f"Error de Binance: {response.text}")
except Exception as e:
    st.error(f"Error técnico: {e}")
