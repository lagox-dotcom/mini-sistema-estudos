import streamlit as st
import requests
import pandas as pd
from datetime import date

# 1. CONFIGURAÇÃO
st.set_page_config(page_title="Tutory - Gestão Fiscal", layout="wide")

API_URL = "https://api-gestao-estudos.onrender.com"

# --- FUNÇÃO DE BUSCA SEGURA ---
def buscar_dados_seguro(endpoint):
    try:
        # Timeout curto para não travar a tela se o Render estiver dormindo
        response = requests.get(f"{API_URL}/{endpoint}", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return None

# --- SIDEBAR ---
st.sidebar.title("🎯 Tutory")
menu = st.sidebar.radio("Navegação", ["📅 Planner", "⏱️ Cronômetro", "📊 Progresso"])

# --- TELA: PLANNER ---
if menu == "📅 Planner":
    st.header(f"📅 Planejamento: {date.today().strftime('%d/%m/%Y')}")
    
    # METAS (Estáticas por enquanto para não dar erro)
    m1, m2, m3 = st.columns(3)
    m1.metric("Meta do Dia", "4h Líquidas")
    m2.metric("Meta da Semana", "24h")
    m3.metric("Meta do Mês", "100h")
    
    st.divider()
    
    with st.spinner("Sincronizando..."):
        aulas = buscar_dados_seguro("planner/hoje")
    
    if aulas is None:
        st.warning("🔌 O servidor está acordando. Aguarde 15 segundos e clique em atualizar.")
        if st.button("🔄 Atualizar"): st.rerun()
    elif len(aulas) == 0:
        st.success("✅ Tudo em dia por aqui!")
    else:
        # Criando os cards de forma segura
        cols = st.columns(len(aulas))
        for i, aula in enumerate(aulas):
            with cols[i]:
                # O segredo: .get() evita o erro se a chave não existir
                disciplina = aula.get('disciplina', 'Matéria')
                assunto = aula.get('assunto', 'Assunto não carregado')
                
                st.markdown(f"""
                <div style="border: 2px solid #2e7bcf; border-radius: 10px; padding: 15px; background-color: #f8f9fa;">
                    <h4 style="margin:0; color: #2e7bcf;">{disciplina}</h4>
                    <p style="font-size: 0.9em;">{assunto}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🎯 Estudar", key=f"btn_{i}"):
                    st.session_state.aula_selecionada = aula
                    st.toast("Selecionado! Vá para o Cronômetro.")

# --- TELA: CRONÔMETRO ---
elif menu == "⏱️ Cronômetro":
    st.header("⏱️ Cronômetro")
    if 'aula_selecionada' not in st.session_state:
        st.warning("⚠️ Selecione uma matéria no Planner primeiro!")
    else:
        aula = st.session_state.aula_selecionada
        st.info(f"📚 Estudando: **{aula.get('disciplina')}**")
        
        c1, c2 = st.columns(2)
        with c1:
            tempo = st.number_input("Minutos Líquidos", 0, 300, 60)
        with c2:
            questoes = st.number_input("Questões", 0, 100, 0)
            acertos = st.number_input("Acertos", 0, 100, 0)
        
        if st.button("🚀 Finalizar e Salvar"):
            # Aqui vai o código do POST que já temos
            st.success("Sessão salva (Simulação)!")

# --- TELA: PROGRESSO ---
elif menu == "📊 Progresso":
    st.header("📊 Desempenho")
    st.write("Aqui aparecerão seus gráficos assim que você salvar as primeiras sessões!")