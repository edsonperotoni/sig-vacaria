import streamlit as st
import streamlit_authenticator as stauth
import folium
from streamlit_folium import st_folium
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(layout="wide", page_title="SIG Colaborativo - Vacaria")

# --- CONFIGURAÇÃO DE USUÁRIOS ---
# Usamos o .to_dict() para garantir que os segredos sejam lidos como um dicionário comum
config = st.secrets["credentials_config"].to_dict()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# 2. TELA DE LOGIN
# O método login agora lida com o estado internamente
authenticator.login(location='main')

# --- VERIFICAÇÃO DE STATUS DE AUTENTICAÇÃO ---
if st.session_state["authentication_status"]:
    # SUCESSO: O usuário está logado
    
    # Barra lateral com Boas-vindas e Botão de Sair
    with st.sidebar:
        st.write(f"## Olá, {st.session_state['name']}!")
        authenticator.logout(button_name='Sair do Sistema', location='sidebar')
    
    st.title("🌎 Sistema de Informações Geográficas de Vacaria")
    st.markdown(f"**Cartógrafo logado:** {st.session_state['username']}")

    # --- CONFIGURAÇÃO DOS DADOS ---
    URL_PLANILHA = st.secrets["database"]["url_planilha"]

    def formatar_url_google_sheets(url):
        try:
            if "/edit" in url:
                base_url = url.split("/edit")[0]
                return f"{base_url}/export?format=csv"
            return url
        except:
            return url

    try:
        # 1. Leitura dos dados
        csv_url = formatar_url_google_sheets(URL_PLANILHA)
        df = pd.read_csv(csv_url)

        # 2. Tratamento de coordenadas (aceita vírgula e ponto)
        df['lat'] = df['lat'].astype(str).str.replace(',', '.').astype(float)
        df['lon'] = df['lon'].astype(str).str.replace(',', '.').astype(float)

        # 3. Criação do Mapa
        # Centralizado em Vacaria/RS
        mapa = folium.Map(location=[-28.5085, -50.9333], zoom_start=14)
        
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
            attr='Google',
            name='Google Satellite'
        ).add_to(mapa)

        # 4. Marcadores
        for _, row in df.iterrows():
            html_popup = f"""
            <div style='width: 200px; font-family: sans-serif;'>
                <h4 style='margin:0 0 5px 0; color: #333;'>{row['nome']}</h4>
                <img src="{row['foto']}" style="width:100%; border-radius:8px; display:block;">
                <p style='font-size:11px; color:#666; margin-top:5px;'>
                    <b>Lat:</b> {row['lat']}<br>
                    <b>Lon:</b> {row['lon']}
                </p>
            </div>
            """
            
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=folium.Popup(html_popup, max_width=250),
                icon=folium.Icon(color=row['cor'], icon="map-marker", prefix="fa")
            ).add_to(mapa)

        # Exibição do Mapa
        st_folium(mapa, width="100%", height=600)
        st.success("✅ Dados carregados com sucesso da planilha!")

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        st.warning("Verifique se a planilha tem as colunas: nome, lat, lon, foto, cor")

elif st.session_state["authentication_status"] is False:
    st.error('Usuário ou senha incorretos.')
elif st.session_state["authentication_status"] is None:
    st.info('Por favor, utilize suas credenciais para acessar o SIG Vacaria.')