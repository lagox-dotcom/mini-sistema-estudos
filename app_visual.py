import streamlit as st
import requests
import pandas as pd
from datetime import date

# 1. CONFIGURAÇÃO
st.set_page_config(page_title="Tutory - Gestão Fiscal", layout="wide")
API_URL = "https://api-gestao-estudos.onrender.com"

def get_data(endpoint):
    try:
        res = requests.get(f"{API_URL}/{endpoint}", timeout=15)
        if res.status_code == 200:
            return res.json()
        return []
    except:
        return None

# --- SIDEBAR ---
st.sidebar.title("🎯 Tutory")
menu = st.sidebar.radio("Navegação", ["📅 Planner", "⏱️ Registrar Sessão", "📊 Progresso"])

# --- TELA 1: PLANNER ---
if menu == "📅 Planner":
    st.header(f"📅 Planejamento: {date.today().strftime('%d/%m/%Y')}")
    
    with st.spinner("Sincronizando..."):
        planner = get_data("planner/hoje")
    
    if planner is None:
        st.error("🔌 Erro de conexão com o servidor.")
    elif not isinstance(planner, list) or len(planner) == 0:
        st.success("✅ Edital em dia! Nenhuma aula para hoje.")
    else:
        cols = st.columns(len(planner))
        for i, aula in enumerate(planner):
            # TRAVA DE SEGURANÇA 1: Verifica se 'aula' é realmente um dicionário
            if isinstance(aula, dict):
                with cols[i]:
                    status_aula = aula.get('status', 'Estudar')
                    cor = "#2e7bcf" if status_aula == "Revisar" else "#28a745"
                    
                    st.markdown(f"""
                    <div style="border-radius: 10px; padding: 15px; background-color: white; border-top: 6px solid {cor}; border: 1px solid #ddd;">
                        <h4 style="margin:0; color: {cor};">{aula.get('disciplina', 'Matéria')}</h4>
                        <p><b>{aula.get('assunto', 'Assunto')}</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"🎯 Selecionar", key=f"btn_{i}"):
                        st.session_state.aula_selecionada = aula
                        st.toast("Selecionado!")
            else:
                st.warning("Recebi um dado inválido do servidor.")

# --- TELA 2: REGISTRAR SESSÃO ---
elif menu == "⏱️ Registrar Sessão":
    st.header("⏱️ Cronômetro e Registro")
    if 'aula_selecionada' not in st.session_state:
        st.warning("⚠️ Selecione uma matéria no Planner primeiro.")
    else:
        aula = st.session_state.aula_selecionada
        # Outra trava de segurança aqui
        nome_disc = aula.get('disciplina', 'Matéria') if isinstance(aula, dict) else "Matéria"
        st.info(f"📚 Estudando: **{nome_disc}**")
        
        with st.form("registro"):
            tempo = st.number_input("Minutos Líquidos", 0, 300, 60)
            questoes = st.number_input("Questões", 0, 100, 0)
            acertos = st.number_input("Acertos", 0, 100, 0)
            if st.form_submit_button("🚀 Salvar"):
                st.success("Sessão salva!")

# --- TELA 3: PROGRESSO ---
elif menu == "📊 Progresso":
    st.header("📊 Desempenho")
    dados = get_data("dashboard/")
    
    if dados and isinstance(dados, list):
        df = pd.DataFrame(dados)
        # TRAVA DE SEGURANÇA 2: Verifica se a coluna existe antes de fazer o gráfico
        if not df.empty and 'disciplina' in df.columns and 'percentual_concluido' in df.columns:
            st.bar_chart(df.set_index('disciplina')['percentual_concluido'])
            st.table(df[['disciplina', 'percentual_concluido']])
        else:
            st.info("Dados do dashboard ainda não possuem o formato esperado.")
    else:
        st.info("Ainda não há dados de progresso. Salve sua primeira sessão!")