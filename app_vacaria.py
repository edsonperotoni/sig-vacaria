import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd

# --- CONFIGURAÇÃO DO DESENVOLVEDOR ---
# O pai deve te enviar o link de "Compartilhar" da planilha dele.
# Certifique-se de que esteja como "Qualquer pessoa com o link pode ler".
URL_PLANILHA = "COLE_AQUI_O_LINK_DA_PLANILHA_DO_PAI"

def formatar_url_google_sheets(url):
    """Transforma o link de visualização do Google Sheets em um link de download de dados."""
    try:
        if "/edit" in url:
            base_url = url.split("/edit")[0]
            return f"{base_url}/export?format=csv"
        return url
    except:
        return url

st.set_page_config(layout="wide", page_title="SIG Colaborativo - Vacaria")

st.title("🌎 Sistema de Informações Geográficas de Vacaria")
st.markdown("Projeto colaborativo de Geografia: Pai e Filho")

try:
    # 1. Leitura dos dados remotos
    csv_url = formatar_url_google_sheets(URL_PLANILHA)
    df = pd.read_csv(csv_url)

    # 2. Criação do Mapa
    mapa = folium.Map(location=[-28.5085, -50.9333], zoom_start=14)
    
    # Camada Satélite (Essencial para o Professor de Geografia)
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite'
    ).add_to(mapa)

    # 3. Distribuição dos pontos
    for _, row in df.iterrows():
        # O HTML agora usa o link direto da internet que o pai colocar na planilha
        html_popup = f"""
        <div style='width: 200px; font-family: sans-serif;'>
            <h4 style='margin:0 0 5px 0; color: #333;'>{row['nome']}</h4>
            <img src="{row['foto']}" style="width:100%; border-radius:8px; display:block;">
            <p style='font-size:11px; color:#666; margin-top:5px;'>
                <b>Latitude:</b> {row['lat']}<br>
                <b>Longitude:</b> {row['lon']}
            </p>
        </div>
        """
        
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(html_popup, max_width=250),
            icon=folium.Icon(color=row['cor'], icon="map-marker", prefix="fa")
        ).add_to(mapa)

    # Exibição
    st_folium(mapa, width="100%", height=600)
    
    st.info("💡 Para atualizar o mapa, basta o pai ou o filho editarem a Planilha do Google e recarregarem esta página.")

except Exception as e:
    st.warning("🚀 Prontos para começar? Cole o link da planilha no código para visualizar os dados de Vacaria.")
    st.image("https://www.gstatic.com/images/branding/product/2x/sheets_2020q4_48dp.png", width=50)