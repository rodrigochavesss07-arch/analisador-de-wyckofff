import streamlit as st
import yfinance as yf
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

# Configuração Visual Estilo Clean
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
        cols[i].error("Off")

st.divider()

# 2. Analisador com Botão de Colar
st.header("🔍 Analisador de Estrutura Wyckoff")
st.write("Tire um print (Win+Shift+S), volte aqui e clique no botão azul:")

# Botão para colar imagem diretamente
paste_result = pbutton("📋 Clica aqui para Colar o Print", key="paste_button")

if paste_result.image_data is not None:
    st.image(paste_result.image_data, caption="Gráfico Carregado", use_container_width=True)
    
    if st.button("🚀 Analisar Estrutura"):
        with st.spinner("A IA está a estudar o gráfico..."):
            try:
                # Configuração da tua NOVA Chave
                genai.configure(api_key="AIzaSyBQ9GBEzALasMWbr4K-acbp7IGds5bNh-0")
                
                # Modelo estável para evitar erro 404 e 429
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                
                # Instrução detalhada para a IA
                prompt = (
                    "Age como um analista sénior de trading. Analisa este gráfico e identifica "
                    "se estamos numa estrutura de Wyckoff de Acumulação ou Distribuição. "
                    "Identifica as fases (A a E) e aponta eventos como SC, AR, ST, Spring ou UTAD."
                )
                
                res = model.generate_content([prompt, paste_result.image_data])
                
                st.success("✅ Análise Concluída!")
                st.subheader("Veredito da IA:")
                st.write(res.text)
                
            except Exception as e:
                if "429" in str(e):
                    st.error("⚠️ Quota Excedida: O Google limitou os teus pedidos por hoje. Tenta daqui a uns minutos.")
                elif "404" in str(e):
                    st.error("⚠️ Erro 404: O modelo Gemini está em manutenção ou o ID mudou. Tenta novamente.")
                else:
                    st.error(f"❌ Erro na análise: {e}")

st.markdown("---")
st.caption("Aviso: Ferramenta educativa. O trading de ativos financeiros envolve risco elevado.")
