import streamlit as st
import yfinance as yf
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

# Configuração Visual Clean
st.set_page_config(page_title="Wyckoff AI - Rodrigo", layout="wide")

# 1. Painel de Tendências no topo
st.title("📊 Tendência do Mercado (24h)")
pares = {
    "EUR/USD": "EURUSD=X", 
    "GBP/USD": "GBPUSD=X", 
    "Ouro (XAU)": "GC=F", 
    "Bitcoin": "BTC-USD", 
    "Nasdaq": "^IXIC"
}

cols = st.columns(5)
for i, (nome, ticker) in enumerate(pares.items()):
    try:
        val = yf.Ticker(ticker).history(period="2d")
        if len(val) > 1:
            fecho_atual = val['Close'].iloc[-1]
            fecho_ontem = val['Close'].iloc[-2]
            diff = ((fecho_atual - fecho_ontem) / fecho_ontem) * 100
            cols[i].metric(nome, f"{fecho_atual:.2f}", f"{diff:.2f}%")
    except:
        cols[i].error("Erro")

st.divider()

# 2. Analisador com Botão de Colar
st.header("🔍 Analisador de Estrutura Wyckoff")
st.write("Tira um print do gráfico (Win+Shift+S) e clica no botão abaixo:")

# Botão para colar imagem diretamente
paste_result = pbutton("📋 Clica aqui para Colar o Print", key="paste_button")

if paste_result.image_data is not None:
    st.image(paste_result.image_data, caption="Gráfico Carregado", use_container_width=True)
    
    if st.button("🚀 Analisar Estrutura"):
        with st.spinner("A IA está a estudar o gráfico..."):
            try:
                # Configuração da tua Chave
                genai.configure(api_key="AIzaSyAmYKPcinhyyBUJv12MGZqlb29j_WVY2mY")
                
                # Modelo atualizado para evitar erro 404
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                
                # Instrução para a IA
                prompt = "Analisa este gráfico financeiro. Identifica se é uma estrutura de Wyckoff de Acumulação ou Distribuição. Descreve as fases A, B, C, D, E e eventos como Spring, UTAD, SC, AR se visíveis."
                
                res = model.generate_content([prompt, paste_result.image_data])
                
                st.subheader("Veredito da IA:")
                st.write(res.text)
            except Exception as e:
                st.error(f"Erro na análise: {e}")
                st.info("Dica: Se o erro persistir, faz 'Reboot' na barra 'Manage App' do Streamlit.")

st.markdown("---")
st.caption("Aviso: Ferramenta educacional. Trading envolve risco real de perda de capital.")
