import streamlit as st
import yfinance as yf
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

# Configuração Visual
st.set_page_config(page_title="Wyckoff AI - Rodrigo", layout="wide")

# 1. Painel de Tendências
st.title("📊 Tendência do Mercado (24h)")
pares = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "Ouro": "GC=F", "Bitcoin": "BTC-USD", "Nasdaq": "^IXIC"}

cols = st.columns(5)
for i, (nome, ticker) in enumerate(pares.items()):
    try:
        val = yf.Ticker(ticker).history(period="2d")
        if len(val) > 1:
            diff = ((val['Close'].iloc[-1] - val['Close'].iloc[-2]) / val['Close'].iloc[-2]) * 100
            cols[i].metric(nome, f"{val['Close'].iloc[-1]:.2f}", f"{diff:.2f}%")
    except:
        cols[i].error("Off")

st.divider()

# 2. Analisador
st.header("🔍 Analisador de Estrutura Wyckoff")
paste_result = pbutton("📋 Clica aqui para Colar o Print", key="paste_button")

if paste_result.image_data is not None:
    st.image(paste_result.image_data, caption="Gráfico Carregado", use_container_width=True)
    
    if st.button("🚀 Analisar Estrutura"):
        with st.spinner("A IA está a analisar..."):
            try:
                # Configuração da Chave
                genai.configure(api_key="AIzaSyBQ9GBEzALasMWbr4K-acbp7IGds5bNh-0")
                
                # Nome do modelo corrigido para evitar o 404
                model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                
                prompt = "Analisa se este gráfico é uma estrutura de Wyckoff de Acumulação ou Distribuição. Explica as fases A-E."
                
                # Processamento da imagem
                res = model.generate_content([prompt, paste_result.image_data])
                
                st.success("Análise Concluída!")
                st.write(res.text)
                
            except Exception as e:
                st.error(f"Erro detalhado: {e}")
                st.info("Se o erro persistir, tenta fazer 'Reboot' no painel lateral do Streamlit.")

st.caption("Aviso: Ferramenta educativa. Trading envolve risco real.")
