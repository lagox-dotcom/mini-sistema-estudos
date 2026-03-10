import streamlit as st
import requests
import pandas as pd
from datetime import date

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Tutory - Gestão Fiscal", layout="wide")

# LINK DA SUA API NO RENDER
API_URL = "https://api-gestao-estudos.onrender.com"

# --- FUNÇÃO DE BUSCA SEGURA ---
def buscar_dados_seguro(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}", timeout=15)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return None

# 2. MENU LATERAL
st.sidebar.title("🎯 Tutory")
menu = st.sidebar.radio("Navegação", ["📅 Planner", "⏱️ Cronômetro", "📊 Progresso"])

# --- TELA 1: PLANNER ---
if menu == "📅 Planner":
    st.header(f"📅 Planejamento: {date.today().strftime('%d/%m/%Y')}")
    
    # METAS NO TOPO
    st.subheader("🚀 Minhas Metas")
    m1, m2, m3 = st.columns(3)
    m1.metric("Meta do Dia", "4h Líquidas")
    m2.metric("Meta da Semana", "24h")
    m3.metric("Meta do Mês", "100h")
    
    st.divider()
    
    with st.spinner("Sincronizando com o motor de estudos..."):
        aulas = buscar_dados_seguro("planner/hoje")
    
    if aulas is None:
        st.warning("🔌 O servidor está acordando. Aguarde alguns segundos e clique em atualizar.")
        if st.button("🔄 Atualizar"): st.rerun()
    elif not isinstance(aulas, list) or len(aulas) == 0:
        st.success("✅ Tudo em dia! Nenhuma aula pendente para hoje.")
    else:
        st.subheader("Disciplinas Sugeridas")
        cols = st.columns(len(aulas))
        for i, aula in enumerate(aulas):
            with cols[i]:
                # O SEGREDO DA CORREÇÃO: .get() evita o erro de Key
                disciplina = aula.get('disciplina', 'Matéria Indefinida')
                assunto = aula.get('assunto', 'Assunto não carregado')
                status = aula.get('status', 'Estudar')
                
                st.markdown(f"""
                <div style="border: 2px solid #2e7bcf; border-radius: 10px; padding: 15px; background-color: #f8f9fa; height: 160px;">
                    <h4 style="margin:0; color: #2e7bcf;">{disciplina}</h4>
                    <p style="font-size: 0.9em; color: #333;"><b>{assunto}</b></p>
                    <span style="font-size: 0.8em; color: #666;">Status: {status}</span>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🎯 Selecionar", key=f"btn_{i}"):
                    st.session_state.aula_selecionada = aula
                    st.toast(f"{disciplina} selecionada!")

# --- TELA 2: CRONÔMETRO ---
elif menu == "⏱️ Cronômetro":
    st.header("⏱️ Sessão de Estudo")
    if 'aula_selecionada' not in st.session_state:
        st.warning("⚠️ Selecione uma matéria no Planner primeiro!")
    else:
        aula = st.session_state.aula_selecionada
        st.info(f"📚 Estudando agora: **{aula.get('disciplina', 'Matéria')}**")
        
        c1, c2 = st.columns(2)
        with c1:
            tempo = st.number_input("Minutos Líquidos", 0, 300, 60)
            pagina = st.text_input("Página de Parada", "pág. ")
        with c2:
            questoes = st.number_input("Questões", 0, 100, 0)
            acertos = st.number_input("Acertos", 0, 100, 0)
        
        if st.button("🚀 Finalizar e Salvar"):
            dados = {
                "aula_id": aula.get('id'),
                "data": str(date.today()),
                "hora_inicio": "14:00",
                "hora_fim": "15:00",
                "hora_liquida": tempo,
                "pagina_parada": pagina,
                "questoes_feitas": questoes,
                "acertos": acertos,
                "status": "Concluído"
            }
            res = requests.post(f"{API_URL}/sessoes/", json=dados)
            if res.status_code == 200:
                st.balloons()
                st.success("Sessão salva com sucesso!")
            else:
                st.error("Erro ao salvar sessão.")

# --- TELA 3: PROGRESSO ---
elif menu == "📊 Progresso":
    st.header("📊 Meu Desempenho")
    st.info("Aqui você verá os gráficos de evolução assim que salvar suas primeiras sessões.")