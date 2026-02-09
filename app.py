import streamlit as st
import yfinance as yf
import google.generativeai as genai
from PIL import Image

# Configuração Visual Clean
st.set_page_config(page_title="Wyckoff AI", layout="wide")

# Painel de Tendências no topo
st.title("📊 Tendência do Mercado (24h)")
pares = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "Ouro": "GC=F", "BTC": "BTC-USD", "Nasdaq": "^IXIC"}
cols = st.columns(5)
for i, (nome, ticker) in enumerate(pares.items()):
    val = yf.Ticker(ticker).history(period="2d")
    if len(val) > 1:
        diff = ((val['Close'].iloc[-1] - val['Close'].iloc[-2]) / val['Close'].iloc[-2]) * 100
        cols[i].metric(nome, f"{val['Close'].iloc[-1]:.2f}", f"{diff:.2f}%")

st.divider()

# Analisador de Imagem
st.header("🔍 Analisador de Estrutura Wyckoff")
upload = st.file_uploader("Envia o teu print do gráfico", type=["png", "jpg", "jpeg"])

if upload:
    img = Image.open(upload)
    st.image(img, use_container_width=True)
    if st.button("Analisar com IA"):
        genai.configure(api_key="gen-lang-client-0267773444")
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(["Analisa este gráfico e identifica a estrutura de Wyckoff (Acumulação/Distribuição) e as fases visíveis.", img])
        st.write(res.text)
