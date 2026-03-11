import streamlit as st
import requests
import pandas as pd
from datetime import date

# 1. CONFIGURAÇÃO DO AMBIENTE
st.set_page_config(page_title="Tutory - Gestão Estratégica", layout="wide")
API_URL = "https://api-gestao-estudos.onrender.com"

# Estilização para ficar com cara de App Profissional
st.markdown("""
    <style>
    .metric-card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #2e7bcf; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #2e7bcf; color: white; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE CONEXÃO COM O MOTOR 3R ---
def get_data(endpoint):
    try:
        res = requests.get(f"{API_URL}/{endpoint}", timeout=15)
        return res.json() if res.status_code == 200 else []
    except:
        return None

# --- SIDEBAR DE NAVEGAÇÃO ---
st.sidebar.title("🎯 Tutory")
st.sidebar.markdown(f"**Usuária:** {st.session_state.get('user', 'Sara')}")
menu = st.sidebar.radio("Navegação", ["📅 Painel de Metas & Planner", "⏱️ Registrar Sessão (Estudo)", "📊 Progresso do Edital"])

# --- TELA 1: PLANNER & METAS ---
if menu == "📅 Painel de Metas & Planner":
    st.header(f"📊 Gestão Estratégica de Estudos - {date.today().strftime('%d/%m/%Y')}")
    
    # SEÇÃO DE METAS (DIÁRIA, SEMANAL, MENSAL)
    st.subheader("🚀 Minhas Metas")
    col1, col2, col3 = st.columns(3)
    
   # Buscamos dados do dashboard para alimentar as metas
    stats = get_data("dashboard/")
    
    # Garantimos que stats seja uma lista antes de tentar somar
    if isinstance(stats, list):
        total_horas = sum([d.get('horas_estudadas', 0) for d in stats if isinstance(d, dict)])
    else:
        total_horas = 0

    # MOTOR 3R: DISCIPLINAS DO DIA
    st.subheader("🧠 Planner Inteligente (Motor 3R)")
    with st.spinner("Consultando o algoritmo de revisões..."):
        planner = get_data("planner/hoje")
    
    if planner is None:
        st.error("🔌 Erro: O servidor no Render não respondeu. Abra o link da API para 'acordar' o sistema.")
    elif not planner:
        st.success("✅ Edital em dia! Nenhuma aula ou revisão pendente para hoje.")
    else:
        cols = st.columns(len(planner))
        for i, aula in enumerate(planner):
            with cols[i]:
                cor = "#2e7bcf" if aula.get('status') == "Revisar" else "#28a745"
                st.markdown(f"""
                <div style="border: 1px solid {cor}; border-radius: 10px; padding: 15px; background-color: white; border-top: 6px solid {cor};">
                    <h4 style="margin:0; color: {cor};">{aula.get('disciplina')}</h4>
                    <p style="font-size: 0.9em;"><b>Assunto:</b> {aula.get('assunto')}</p>
                    <p style="font-size: 0.8em;">Status: {aula.get('status')} | ⭐ {aula.get('dificuldade')}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🎯 Iniciar {aula.get('disciplina')}", key=f"plan_{i}"):
                    st.session_state.aula_selecionada = aula
                    st.toast("Aula selecionada! Vá para a aba de Registro.")

# --- TELA 2: REGISTRO DE SESSÃO DETALHADO ---
elif menu == "⏱️ Registrar Sessão (Estudo)":
    st.header("⏱️ Cronômetro e Registro de Performance")
    
    if 'aula_selecionada' not in st.session_state:
        st.warning("⚠️ Selecione uma matéria no Planner primeiro para carregar os dados automaticamente.")
    else:
        aula = st.session_state.aula_selecionada
        st.info(f"📌 **Disciplina:** {aula.get('disciplina')} | **Assunto:** {aula.get('assunto')}")
        
        with st.form("form_sessao"):
            c1, c2, c3 = st.columns(3)
            with c1:
                data_estudo = st.date_input("Data", date.today())
                tempo = st.number_input("Minutos Líquidos", 0, 300, 60)
            with c2:
                questoes = st.number_input("Questões Feitas", 0, 100, 0)
                acertos = st.number_input("Acertos", 0, 100, 0)
            with c3:
                pagina = st.text_input("Página de Parada", placeholder="Ex: pág 45")
                status_aula = st.selectbox("Status da Aula", ["Em Progresso", "Concluído"])

            if st.form_submit_button("🚀 Finalizar e Atualizar Base"):
                payload = {
                    "aula_id": aula.get('id'),
                    "data": str(data_estudo),
                    "hora_liquida": tempo,
                    "questoes_feitas": questoes,
                    "acertos": acertos,
                    "pagina_parada": pagina,
                    "status": status_aula
                }
                res = requests.post(f"{API_URL}/sessoes/", json=payload)
                if res.status_code == 200:
                    st.balloons()
                    st.success("✅ Sessão salva! O Motor 3R já recalculou sua próxima revisão.")
                else:
                    st.error("❌ Erro ao salvar na base de dados.")

# --- TELA 3: PROGRESSO DO EDITAL ---
elif menu == "📊 Progresso do Edital":
    st.header("📈 Dashboard de Evolução")
    dados = get_data("dashboard/")
    if dados:
        df = pd.DataFrame(dados)
        st.subheader("Percentual de Conclusão por Matéria")
        st.bar_chart(df.set_index('disciplina')['percentual_concluido'])
        st.table(df[['disciplina', 'aulas_concluidas', 'percentual_concluido']])
    else:
        st.info("Ainda não há dados suficientes para gerar o gráfico.")