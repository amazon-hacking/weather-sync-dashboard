# streamlit/app_simple.py
"""
Versão simplificada e modular da aplicação Weather Sync
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from application.db import get_engine
from application.queries import *
from application.charts import *
from application.utils import checagem_data

# Configuração da página
st.set_page_config(
    page_title="Weather Sync",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS responsivo
st.markdown("""
<style>
/* Ocultar elementos padrão */
#MainMenu {visibility: hidden;}
.stDeployButton {display:none;}
footer {visibility: hidden;}
.stActionButton {display:none;}

/* Container responsivo */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    padding-left: clamp(1rem, 5vw, 5rem);
    padding-right: clamp(1rem, 5vw, 5rem);
    max-width: 100%;
}

.element-container {
    margin-bottom: 0rem !important;
}

/* Background principal */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Header responsivo */
.header-box {
    background: linear-gradient(135deg, #4285f4 0%, #1976d2 100%);
    color: white;
    padding: clamp(1rem, 4vw, 2rem);
    border-radius: 15px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 8px 25px rgba(66, 133, 244, 0.3);
}

.header-box h1 {
    font-size: clamp(1.5rem, 5vw, 2.5rem) !important;
    margin: 1rem 0 0.5rem 0 !important;
    letter-spacing: clamp(1px, 0.3vw, 2px);
    line-height: 1.2;
}

.header-box p {
    font-size: clamp(0.8rem, 2.5vw, 1.1rem) !important;
    opacity: 0.9;
    margin: 0.5rem 0 !important;
    line-height: 1.4;
}

.header-box div:first-child {
    font-size: clamp(2rem, 6vw, 3rem) !important;
}

/* Seções responsivas */
.section-box {
    background: #3C3C3C;
    border-radius: 15px;
    padding: clamp(1rem, 3vw, 1.5rem);
    margin: 1rem 0;
    border-left: 4px solid #4285f4;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.section-box h2 {
    font-size: clamp(1.1rem, 3.5vw, 1.5rem) !important;
    margin-bottom: 1rem !important;
    line-height: 1.3;
}

/* Botões responsivos */
.stButton > button {
    background: linear-gradient(135deg, #4285f4 0%, #1976d2 100%);
    color: white;
    border: none;
    border-radius: 25px;
    padding: clamp(0.4rem, 2vw, 0.6rem) clamp(1rem, 4vw, 2rem);
    font-weight: bold;
    font-size: clamp(0.8rem, 2.2vw, 1rem);
    transition: all 0.3s ease;
    width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Títulos de seção responsivos */
.stMarkdown h3 {
    font-size: clamp(1rem, 3vw, 1.2rem) !important;
    margin: 0.5rem 0 !important;
}

/* Inputs responsivos */
.stDateInput, .stMultiSelect, .stRadio {
    margin-bottom: 0rem;
}

.stDateInput label, .stMultiSelect label, .stRadio label {
    font-size: clamp(0.8rem, 2.2vw, 1rem) !important;
}

/* Radio buttons compactos */
.stRadio > div {
    padding: clamp(0.5rem, 2vw, 1rem);
}

.stRadio > div > label {
    font-size: clamp(0.75rem, 2vw, 0.9rem) !important;
}

/* Multiselect compacto */
.stMultiSelect > div > div {
    min-height: auto;
}

/* Colunas responsivas */
.stColumns {
    gap: clamp(0.25rem, 1vw, 0.5rem);
}

/* Gráficos responsivos */
.stPlotlyChart, .stAltairChart {
    background: transparent;
    margin: 0;
    padding: 0;
    overflow-x: auto;
}

/* DataFrames responsivos */
.stDataFrame {
    margin: 0;
    padding: 0;
    font-size: clamp(0.7rem, 1.8vw, 0.9rem);
}

/* Alertas responsivos */
.stAlert {
    font-size: clamp(0.8rem, 2vw, 0.9rem) !important;
    padding: clamp(0.5rem, 2vw, 1rem);
}

/* Media queries para ajustes específicos */
@media (max-width: 768px) {
    .stColumns > div {
        margin-bottom: 1rem;
    }
    
    .header-box {
        margin-bottom: 1rem;
    }
    
    .section-box {
        margin: 0.5rem 0;
    }
    
    /* Empilhar colunas em telas pequenas */
    .stColumns {
        flex-direction: column;
    }
    
    /* Ajustar largura dos gráficos */
    .stAltairChart > div, .stPlotlyChart > div {
        width: 100% !important;
    }
}

@media (max-width: 480px) {
    .block-container {
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }
    
    .card-box {
        padding: 0.6rem;
        margin: 0.25rem 0;
    }
    
    .section-box {
        border-radius: 10px;
    }
    
    .header-box {
        padding: 1rem;
        border-radius: 10px;
    }
    
    .stButton > button {
        padding: 0.4rem 0.8rem;
        font-size: 0.8rem;
    }
}

/* Remover espaços extras */
.stMarkdown {
    margin-bottom: 0rem;
}

.stVerticalBlock > div:empty {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-box">
    <div style="font-size: 3rem;">💧</div>
    <h1 style="margin: 1rem 0; letter-spacing: 2px;">WEATHER SYNC</h1>
    <p style="opacity: 0.9;">Acompanhe o clima das suas regiões favoritas de forma prática e inteligente</p>
</div>
""", unsafe_allow_html=True)

# Inicializar engine
engine = get_engine()

# 🏭 SEÇÃO POLUENTES
st.markdown("""
<div class="section-box">
    <h2 style="color: #FFFFFF">🏭 Análise de Poluentes (mouse por cima exibe opção de tela cheia)</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])

with col1:
    poluentes = get_poluentes_unicos(engine)
    st.markdown('### Escolha um Poluente')
    poluente_escolhido = st.radio("", poluentes["poluente"].tolist())
    
    if 'mostrar_grafico_poluentes' not in st.session_state:
        st.session_state.mostrar_grafico_poluentes = True
    
    st.button("🔄 Trocar Exibição", 
              key="troca_exibicao_poluentes",
              on_click=lambda: st.session_state.update({"mostrar_grafico_poluentes": not st.session_state.mostrar_grafico_poluentes}))

with col2:
    df_poluente = get_poluente_por_bairro(engine, poluente_escolhido)
    
    if st.session_state.mostrar_grafico_poluentes:
        st.altair_chart(chart_poluente(df_poluente, poluente_escolhido), use_container_width=True)
    else:
        st.dataframe(df_poluente, use_container_width=True)

# 🌡️ SEÇÃO TEMPERATURA E UMIDADE
st.markdown("""
<div class="section-box">
    <h2 style="color: #FFFFFF; margin-bottom: 1rem;">🌡️ Monitoramento de Temperatura e Umidade</h2>
</div>
""", unsafe_allow_html=True)

# Controles
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📅 Data Inicial**")
    data_ini = st.date_input("", key="data_ini", label_visibility="collapsed")
with col2:
    st.markdown("**📅 Data Final**")
    data_fim = st.date_input("", key="data_fim", label_visibility="collapsed")

with col3:
    st.markdown("**🏘️ Bairros (máximo de 3)**")
    bairros = st.multiselect("", get_bairros_disponiveis(engine)['bairro'].tolist(), 
                            max_selections=3,
                            key="bairros", 
                            label_visibility="collapsed")


# Botão centralizado
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if 'mostrar_grafico_umi_temp' not in st.session_state:
        st.session_state.mostrar_grafico_umi_temp = True
    
    st.button("🔄 Trocar Exibição dos Gráficos", 
              key="troca_exibicao_umi_temp",
              on_click=lambda: st.session_state.update({"mostrar_grafico_umi_temp": not st.session_state.mostrar_grafico_umi_temp}))

# Dados de temperatura e umidade
params = {"data_ini": data_ini, "data_fim": data_fim, "bairros": bairros}
df_temp = checagem_data(get_temperatura(engine, params))
df_umi = checagem_data(get_umidade(engine, params))

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🌡️ Temperatura (mouse por cima exibe opção de tela cheia)")
    
    if not df_temp.empty:
        if st.session_state.mostrar_grafico_umi_temp:
            st.altair_chart(chart_temperatura(df_temp).interactive(), use_container_width=True)
        else:
            st.dataframe(df_temp, use_container_width=True)
    else:
        st.warning("⚠️ Nenhum dado de temperatura encontrado.")
    


with col2:
    st.markdown("### 💧 Umidade (mouse por cima exibe opção de tela cheia)")
    
    if not df_umi.empty:
        if st.session_state.mostrar_grafico_umi_temp:
            st.altair_chart(chart_umidade(df_umi).interactive(), use_container_width=True)
        else:
            st.dataframe(df_umi, use_container_width=True)
    else:
        st.warning("⚠️ Nenhum dado de umidade encontrado.")
    


# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.8); margin-top: 3rem;">
    <hr style="border: none; height: 1px; background: linear-gradient(to right, transparent, rgba(255,255,255,0.3), transparent); margin: 2rem 0;">
    ⚡ Weather Sync - Recursos pensados para facilitar seu dia a dia
</div>
""", unsafe_allow_html=True)