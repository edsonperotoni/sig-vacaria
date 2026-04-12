import streamlit as st
import streamlit_authenticator as stauth
import folium
from streamlit_folium import st_folium
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA (Sempre o primeiro comando Streamlit)
st.set_page_config(layout="wide", page_title="SIG Colaborativo - Vacaria")

# --- CONFIGURAÇÃO DE USUÁRIOS ---
# Em vez de escrever as senhas aqui, pedimos ao Streamlit para buscar nos segredos
# Em vez de passar o st.secrets direto, vamos converter para um dicionário comum (dict) - um xérox do conteúdo, para evitar problemas de tipo.
config = dict(st.secrets["credentials_config"])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# 2. TELA DE LOGIN
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # --- TUDO DAQUI PARA BAIXO SÓ APARECE SE LOGAR ---
    authenticator.logout('Sair', 'sidebar')
    
    st.title("🌎 Sistema de Informações Geográficas de Vacaria")
    st.write(f"Bem-vindo, {name}! Você está acessando o mapa colaborativo.")

    # --- CONFIGURAÇÃO DO DESENVOLVEDOR ---
    URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1NU5xpPUmBpw4Tgj9fsZDQ6HOkg3K_71I4Tr8bDNn8NI/edit?usp=sharing"

    def formatar_url_google_sheets(url):
        try:
            if "/edit" in url:
                base_url = url.split("/edit")[0]
                return f"{base_url}/export?format=csv"
            return url
        except:
            return url

    try:
        # 1. Leitura dos dados remotos
        csv_url = formatar_url_google_sheets(URL_PLANILHA)
        df = pd.read_csv(csv_url)

        # --- TRATAMENTO PARA PADRÃO BRASILEIRO (VÍRGULA PARA PONTO) ---
        # Isso garante que se o pai digitar -28,50 ou -28.50, o Python entenda.
        df['lat'] = df['lat'].astype(str).str.replace(',', '.').astype(float)
        df['lon'] = df['lon'].astype(str).str.replace(',', '.').astype(float)

        # 2. Criação do Mapa
        mapa = folium.Map(location=[-28.5085, -50.9333], zoom_start=14)
        
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
            attr='Google',
            name='Google Satellite'
        ).add_to(mapa)

        # 3. Distribuição dos pontos
        for _, row in df.iterrows():
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
        st.info("💡 Para atualizar o mapa, basta editar a Planilha do Google e recarregar esta página.")

    except Exception as e:
        st.warning("🚀 Prontos para começar? Cole o link da planilha no código para visualizar os dados.")

elif authentication_status == False:
    st.error('Usuário ou senha incorretos')
elif authentication_status == None:
    st.warning('Por favor, insira seu usuário e senha para acessar o mapa de Vacaria.')