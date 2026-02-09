import streamlit as st
import yfinance as yf
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

st.set_page_config(page_title="Wyckoff AI - Rodrigo", layout="wide")

st.title("📊 Tendência do Mercado (24h)")
pares = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "Ouro": "GC=F", "BTC": "BTC-USD", "Nasdaq": "^IXIC"}
cols = st.columns(5)
for i, (nome, ticker) in enumerate(pares.items()):
    try:
        val = yf.Ticker(ticker).history(period="2d")
        if len(val) > 1:
            diff = ((val['Close'].iloc[-1] - val['Close'].iloc[-2]) / val['Close'].iloc[-2]) * 100
            cols[i].metric(nome, f"{val['Close'].iloc[-1]:.2f}", f"{diff:.2f}%")
    except: cols[i].error("Erro")

st.divider()
st.header("🔍 Analisador de Estrutura Wyckoff")
paste_result = pbutton("📋 Clica aqui para Colar o Print", key="paste_button")

if paste_result.image_data is not None:
    st.image(paste_result.image_data, use_container_width=True)
    if st.button("🚀 Analisar Estrutura"):
        with st.spinner("Analisando..."):
            try:
                genai.configure(api_key="AIzaSyAmYKPcinhyyBUJv12MGZqlb29j_WVY2mY")
                # MUDANÇA AQUI: gemini-2.0-flash é o modelo atual suportado
                model = genai.GenerativeModel('gemini-2.0-flash')
                res = model.generate_content(["Analisa se é Wyckoff Acumulação ou Distribuição.", paste_result.image_data])
                st.write(res.text)
            except Exception as e:
                st.error(f"Erro: {e}")
