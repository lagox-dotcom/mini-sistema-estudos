import streamlit as st
import requests
import pandas as pd
from datetime import date

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Tutory - Gestão Fiscal", layout="wide")

# LINK DA SUA API NO RENDER
API_URL = "https://api-gestao-estudos.onrender.com"

# Estilização CSS para os cards
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; background-color: #2e7bcf; color: white; }
    .card {
        border-radius: 10px; padding: 15px; background-color: #f8f9fa; 
        border-top: 5px solid #2e7bcf; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. MENU LATERAL
st.sidebar.title("🎯 Tutory")
menu = st.sidebar.radio("Navegação", ["📅 Planner de Hoje", "⏱️ Cronômetro", "📊 Meu Progresso"])

# --- FUNÇÃO DE BUSCA SEGURA ---
def buscar_dados(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}", timeout=15)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return None

# --- TELA 1: PLANNER DE HOJE ---
if menu == "📅 Planner de Hoje":
    st.header(f"📅 Planejamento: {date.today().strftime('%d/%m/%Y')}")
    
    with st.spinner("Conectando ao servidor..."):
        aulas = buscar_dados("planner/hoje")
    
    if aulas is None:
        st.error("🔌 O servidor está demorando a responder. Tente atualizar.")
        if st.button("🔄 Tentar Reconectar"): st.rerun()
    elif not aulas:
        st.success("✅ Tudo pronto! Nenhuma aula para hoje.")
    else:
        st.subheader("Matérias do Dia")
        cols = st.columns(len(aulas))
        for i, aula in enumerate(aulas):
            with cols[i]:
                cor = "#2e7bcf" if aula.get('status') == "Revisar" else "#28a745"
                st.markdown(f"""
                <div style="border-radius: 10px; padding: 15px; background-color: #f8f9fa; border-top: 5px solid {cor}; height: 160px;">
                    <h4 style="color: {cor}; margin:0;">{aula['disciplina']}</h4>
                    <p style="font-size: 0.9em; margin-bottom:2px;"><b>{aula['assunto']}</b></p>
                    <p style="font-size: 0.8em; color: #666;">Status: {aula['status']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🎯 Estudar {aula['disciplina'][:10]}", key=f"btn_{i}"):
                    st.session_state.aula_selecionada = aula
                    st.toast("Matéria selecionada!")

# --- TELA 2: CRONÔMETRO ---
elif menu == "⏱️ Cronômetro":
    st.header("⏱️ Sessão de Estudo")
    if 'aula_selecionada' not in st.session_state:
        st.warning("⚠️ Selecione uma matéria no Planner primeiro!")
    else:
        aula = st.session_state.aula_selecionada
        st.info(f"📚 Estudando: **{aula['disciplina']}**")
        
        c1, c2 = st.columns(2)
        with c1:
            tempo = st.number_input("Minutos Líquidos", 0, 300, 60)
            pagina = st.text_input("Página de Parada", "pág. ")
        with c2:
            questoes = st.number_input("Questões", 0, 100, 0)
            acertos = st.number_input("Acertos", 0, 100, 0)
        
        if st.button("🚀 Finalizar e Salvar"):
            dados = {
                "aula_id": aula['id'], "data": str(date.today()),
                "hora_inicio": "14:00", "hora_fim": "15:00",
                "hora_liquida": tempo, "pagina_parada": pagina,
                "questoes_feitas": questoes, "acertos": acertos, "status": "Concluído"
            }
            res = requests.post(f"{API_URL}/sessoes/", json=dados)
            if res.status_code == 200:
                st.balloons()
                st.success("Sessão registrada!")
            else:
                st.error("Erro ao salvar.")

# --- TELA 3: PROGRESSO ---
elif menu == "📊 Meu Progresso":
    st.header("📊 Desempenho")
    dados = buscar_dados("dashboard/")
    if dados:
        df = pd.DataFrame(dados)
        st.bar_chart(df.set_index('disciplina')['percentual_concluido'])
        st.dataframe(df[['disciplina', 'percentual_concluido']], use_container_width=True)
    else:
        st.info("Sem dados de progresso ainda.")