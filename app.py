import streamlit as st
import pandas as pd
import requests
import time
import hmac
import hashlib

st.title("📊 Mi Panel de Binance Real")

# Obtener credenciales desde los Secrets
api_key = st.secrets["BINANCE_API_KEY"]
secret_key = st.secrets["BINANCE_SECRET_KEY"]

# Configuración básica de Binance
base_url = "https://api.binance.com"
endpoint = "/api/v3/myTrades"
symbol = "USDTVES" # Ajusta esto a tu moneda principal si es necesario

# Función para firmar la petición (seguridad de Binance)
def get_signature(params, secret):
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

# Preparar la consulta
params = {
    "symbol": "USDTTRY", # O la moneda que operes (ej: USDTUSDT no existe, usa un par real)
    "timestamp": int(time.time() * 1000),
    "limit": 10
}
params["signature"] = get_signature(params, secret_key)
headers = {"X-MBX-APIKEY": api_key}

# Llamada a la API
response = requests.get(base_url + endpoint, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    if data:
        df = pd.DataFrame(data)
        st.write("### Tus últimas operaciones:")
        st.dataframe(df[['time', 'symbol', 'price', 'qty', 'side']])
    else:
        st.write("No se encontraron operaciones recientes.")
else:
    st.error(f"Error al conectar con Binance: {response.text}")