import streamlit as st
import requests
import pandas as pd
from datetime import date
import time

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Tutory - Gestão Fiscal", layout="wide")

# LINK DA SUA API (VERIFIQUE SE ESTÁ EXATAMENTE ASSIM)
API_URL = "https://api-gestao-estudos.onrender.com"

# 2. FUNÇÃO DE BUSCA ROBUSTA (O SEGREDO)
def buscar_dados_seguro(endpoint):
    url = f"{API_URL}/{endpoint}"
    try:
        # Tentamos a conexão com um tempo de espera (timeout) e ignorando erros de SSL comuns em nuvem
        response = requests.get(url, timeout=20, verify=True) 
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        # Se der erro, ele nos avisa o que é na tela de log
        return None

# --- INTERFACE ---
st.sidebar.title("🎯 Tutory")
menu = st.sidebar.radio("Navegação", ["📅 Planner de Hoje", "⏱️ Cronômetro", "📊 Meu Progresso"])

if menu == "📅 Planner de Hoje":
    st.header(f"📅 Planejamento: {date.today().strftime('%d/%m/%Y')}")
    
    # Metas Visuais
    st.subheader("🚀 Minhas Metas")
    m1, m2, m3 = st.columns(3)
    m1.metric("Meta do Dia", "4h Líquidas", "Foco!")
    m2.metric("Meta da Semana", "24h", "No ritmo")
    
    # Tentativa de carregar os dados
    with st.spinner("Sincronizando com o Render..."):
        aulas = buscar_dados_seguro("planner/hoje")
        # Damos um segundo para o Streamlit processar
        if aulas is None:
            st.warning("⚠️ O sistema está tentando acordar o servidor. Se não carregar em 10 segundos, clique no botão abaixo.")
            if st.button("🔄 Forçar Sincronização"):
                st.rerun()
        elif not aulas:
            st.success("✅ Sem pendências para hoje!")
        else:
            st.subheader("Disciplinas Sugeridas")
            cols = st.columns(len(aulas))
            for i, aula in enumerate(aulas):
                with cols[i]:
                    st.info(f"**{aula['disciplina']}**\n\n{aula['assunto']}")
                    if st.button(f"🎯 Iniciar", key=f"btn_{i}"):
                        st.session_state.aula_selecionada = aula
                        st.toast("Pronto! Vá para o Cronômetro.")

# (Mantenha o resto do código de Cronômetro e Progresso que já tínhamos)