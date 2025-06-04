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

# CSS moderno e elegante
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Reset e base */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Ocultar elementos padrão */
#MainMenu {visibility: hidden;}
.stDeployButton {display:none;}
footer {visibility: hidden;}
.stActionButton {display:none;}

/* Variáveis CSS para paleta azul */
:root {
    --primary-blue: #0052CC;
    --secondary-blue: #0065FF;
    --light-blue: #4285F4;
    --sky-blue: #40A9FF;
    --ice-blue: #E3F2FD;
    --dark-blue: #001E3C;
    --navy-blue: #0D1421;
    
    --gradient-primary: linear-gradient(135deg, #0052CC 0%, #4285F4 50%, #40A9FF 100%);
    --gradient-secondary: linear-gradient(135deg, #001E3C 0%, #0052CC 50%, #0065FF 100%);
    --gradient-accent: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 50%, #90CAF9 100%);
    
    --shadow-soft: 0 4px 20px rgba(0, 82, 204, 0.15);
    --shadow-medium: 0 8px 32px rgba(0, 82, 204, 0.25);
    --shadow-strong: 0 16px 48px rgba(0, 82, 204, 0.35);
    
    --blur-glass: blur(16px);
    --border-radius: 20px;
    --border-radius-small: 12px;
}

/* Background principal com padrão animado */
.stApp {
    background: var(--navy-blue);
    background-image: 
        radial-gradient(circle at 20% 80%, rgba(0, 82, 204, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(66, 133, 244, 0.2) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(64, 169, 255, 0.1) 0%, transparent 50%);
    min-height: 100vh;
    animation: backgroundShift 20s ease-in-out infinite;
}

@keyframes backgroundShift {
    0%, 100% { 
        background-position: 0% 0%, 100% 100%, 50% 50%; 
    }
    50% { 
        background-position: 100% 100%, 0% 0%, 80% 20%; 
    }
}

/* Container responsivo */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
    padding-left: clamp(1rem, 5vw, 5rem);
    padding-right: clamp(1rem, 5vw, 5rem);
    max-width: 100%;
    font-family: 'Inter', sans-serif;
}

.element-container {
    margin-bottom: 0rem !important;
}

/* Header com glassmorphism */
.header-box {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: var(--blur-glass);
    -webkit-backdrop-filter: var(--blur-glass);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
    padding: clamp(1.5rem, 4vw, 2.5rem);
    border-radius: var(--border-radius);
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: var(--shadow-strong);
    position: relative;
    overflow: hidden;
    animation: fadeInUp 1s ease-out;
}

.header-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    animation: shine 3s infinite;
}

@keyframes shine {
    0% { left: -100%; }
    100% { left: 100%; }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.header-box .icon {
    font-size: clamp(3rem, 8vw, 5rem) !important;
    margin-bottom: 1rem;
    filter: drop-shadow(0 4px 8px rgba(64, 169, 255, 0.5));
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.header-box h1 {
    font-size: clamp(2rem, 6vw, 3.5rem) !important;
    margin: 1rem 0 0.5rem 0 !important;
    letter-spacing: clamp(2px, 0.5vw, 4px);
    line-height: 1.2;
    font-weight: 700;
    background: var(--gradient-accent);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.header-box p {
    font-size: clamp(1.1rem, 3.2vw, 1.4rem) !important;
    opacity: 0.9;
    margin: 0.5rem 0 !important;
    line-height: 1.5;
    font-weight: 400;
}

/* Seções com glassmorphism melhorado */
.section-box {
    max-width: 768px;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: var(--blur-glass);
    -webkit-backdrop-filter: var(--blur-glass);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    margin: 1.5rem 0;
    box-shadow: var(--shadow-medium);
    position: relative;
    overflow: hidden;
    animation: slideInLeft 0.8s ease-out;
    transition: all 0.3s ease;
}

.section-box:hover {
    background: rgba(255, 255, 255, 0.12);
    box-shadow: var(--shadow-strong);
    transform: translate(3px)
    }

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.section-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--gradient-primary);
    border-radius: var(--border-radius) var(--border-radius) 0 0;
}

.section-box h2 {
    color: white !important;
    font-size: clamp(1.3rem, 4vw, 1.8rem) !important;
    margin-bottom: 1rem !important;
    line-height: 1.3;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Textos de descrição nas seções */
.section-box p {
    font-size: clamp(1rem, 2.8vw, 1.2rem) !important;
    line-height: 1.5;
    margin-bottom: 0.8rem !important;
    
}

/* Cards internos */
.inner-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-small);
    padding: 1rem;
    margin: 0.5rem 0;
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
}

.inner-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(66, 133, 244, 0.3);
}

/* Botões modernos */
.stButton > button {
    background: var(--gradient-primary) !important;
    color: white !important;
    border: none !important;
    border-radius: 30px !important;
    padding: clamp(0.6rem, 2.5vw, 0.8rem) clamp(1.5rem, 5vw, 2.5rem) !important;
    font-weight: 600 !important;
    font-size: clamp(0.9rem, 2.5vw, 1.1rem) !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    width: 100% !important;
    box-shadow: var(--shadow-soft) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button:hover {
    background: var(--gradient-secondary) !important;
    box-shadow: var(--shadow-medium) !important;
    transform: translateY(-2px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Inputs elegantes */
.stDateInput > div > div, 
.stMultiSelect > div > div,
.stRadio > div {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: var(--border-radius-small) !important;
    backdrop-filter: blur(8px) !important;
    transition: all 0.3s ease !important;
}

.stDateInput > div > div:focus-within,
.stMultiSelect > div > div:focus-within {
    border-color: var(--light-blue) !important;
    box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.2) !important;
}

/* Labels estilizados */
.stDateInput label, 
.stMultiSelect label, 
.stRadio label {
    color: white !important;
    font-size: clamp(1rem, 2.8vw, 1.2rem) !important;
    font-weight: 500 !important;
    margin-bottom: 0.5rem !important;
}

/* Radio buttons personalizados */
.stRadio > div {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-small);
    padding: 1rem;
    margin: 0.5rem 0;
}

.stRadio > div > label {
    color: white !important;
    font-size: clamp(0.95rem, 2.5vw, 1.1rem) !important;
    font-weight: 400 !important;
}

.stRadio > div > label > div {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
}

.stRadio > div > label > div[data-checked="true"] {
    background: var(--gradient-primary) !important;
    border-color: var(--light-blue) !important;
}

/* Títulos de seção */
.stMarkdown h3 {
    color: white !important;
    font-size: clamp(1.1rem, 3.2vw, 1.4rem) !important;
    margin: 1rem 0 !important;
    font-weight: 600 !important;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Gráficos com bordas elegantes */
.stPlotlyChart, .stAltairChart {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: var(--border-radius-small) !important;
    padding: 1rem !important;
    margin: 1rem 0 !important;
    backdrop-filter: blur(8px) !important;
    overflow: hidden !important;
    transition: all 0.3s ease !important;
}

.stPlotlyChart:hover, .stAltairChart:hover {
    border-color: rgba(66, 133, 244, 0.3) !important;
    box-shadow: var(--shadow-soft) !important;
}

/* DataFrames estilizados */
.stDataFrame {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: var(--border-radius-small) !important;
    overflow: hidden !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: clamp(0.75rem, 2vw, 0.9rem) !important;
}

.stDataFrame > div {
    background: transparent !important;
}

/* Alertas personalizados */
.stAlert {
    background: rgba(255, 193, 7, 0.1) !important;
    border: 1px solid rgba(255, 193, 7, 0.3) !important;
    border-radius: var(--border-radius-small) !important;
    color: #FFF3CD !important;
    font-size: clamp(0.95rem, 2.5vw, 1.1rem) !important;
    padding: 1rem !important;
    backdrop-filter: blur(8px) !important;
}

/* Textos em markdown (como **Data Inicial**) */
.stMarkdown p {
    font-size: clamp(1rem, 2.8vw, 1.2rem) !important;
    color: white !important;
    line-height: 1.4;
}

.stMarkdown strong {
    font-weight: 600 !important;
}

/* Colunas com espaçamento */
.stColumns {
    gap: clamp(0.5rem, 2vw, 1rem) !important;
}

/* Footer elegante */
.footer {
    text-align: center;
    padding: 2rem 0;
    color: rgba(255,255,255,0.7);
    margin-top: 2rem;
    position: relative;
}

.footer::before {
    content: '';
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(255,255,255,0.3), transparent);
}

/* Animações de entrada */
.fadeIn {
    animation: fadeIn 1s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Responsividade melhorada */
@media (max-width: 768px) {
    .stColumns > div {
        margin-bottom: 1rem;
    }
    
    .header-box {
        margin-bottom: 1.5rem;
        padding: 1.5rem 1rem;
    }
    
    .section-box {
        margin: 1rem 0;
        padding: 1rem;
    }
    
    .stColumns {
        flex-direction: column;
    }
    
    .stAltairChart > div, .stPlotlyChart > div {
        width: 100% !important;
    }
}

@media (max-width: 480px) {
    .block-container {
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }
    
    .inner-card {
        padding: 0.8rem;
        margin: 0.3rem 0;
    }
    
    .section-box {
        border-radius: 15px;
        padding: 0.8rem;
    }
    
    .header-box {
        padding: 1.2rem;
        border-radius: 15px;
    }
    
    .stButton > button {
        padding: 0.6rem 1rem !important;
        font-size: 0.9rem !important;
    }
}

/* Scrollbar personalizada */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: var(--gradient-primary);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--light-blue);
}

/* Remover espaços extras */
.stMarkdown {
    margin-bottom: 0rem;
}

.stVerticalBlock > div:empty {
    display: none;
}

/* Efeitos especiais para interatividade */
.glow-on-hover {
    transition: all 0.3s ease;
}

.glow-on-hover:hover {
    box-shadow: 0 0 20px rgba(66, 133, 244, 0.4) !important;
}
</style>
""", unsafe_allow_html=True)

# Header moderno
st.markdown("""
<div class="header-box">
    <div class="icon">💧</div>
    <h1>WEATHER SYNC</h1>
    <p>Acompanhe o clima das suas regiões favoritas de forma prática e inteligente</p>
</div>
""", unsafe_allow_html=True)

# Inicializar engine
engine = get_engine()

# 🏭 SEÇÃO POLUENTES
st.markdown("""
<div class="section-box">
    <h2>🏭 Análise de Poluentes</h2>
    <p style="color: rgba(255,255,255,0.8); margin-bottom: 1rem;">Monitore a qualidade do ar em tempo real com visualizações interativas</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])

with col1:
    poluentes = get_poluentes_unicos(engine)
    st.markdown("### 🔬 Escolha um Poluente:")
    poluente_escolhido = st.radio("", poluentes["poluente"].tolist())
    
    if 'mostrar_grafico_poluentes' not in st.session_state:
        st.session_state.mostrar_grafico_poluentes = True
    
    st.button("🔄 Alternar Visualização", 
              key="troca_exibicao_poluentes",
              on_click=lambda: st.session_state.update({"mostrar_grafico_poluentes": not st.session_state.mostrar_grafico_poluentes}))
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    df_poluente = get_poluente_por_bairro(engine, poluente_escolhido)
    st.markdown("")
    st.markdown("---")
    if st.session_state.mostrar_grafico_poluentes:
        st.altair_chart(chart_poluente(df_poluente, poluente_escolhido), use_container_width=True)
    else:
        st.dataframe(df_poluente, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 🌡️ SEÇÃO TEMPERATURA E UMIDADE
st.markdown("""
<div class="section-box">
    <h2>🌡️ Monitoramento Climático Avançado</h2>
    <p style="color: rgba(255,255,255,0.8); margin-bottom: 1rem;">Análise detalhada de temperatura e umidade por região e período</p>
</div>
""", unsafe_allow_html=True)

# Controles em cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📅 Data Inicial**")
    data_ini = st.date_input("", key="data_ini", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("**📅 Data Final**")
    data_fim = st.date_input("", key="data_fim", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown("**🏘️ Bairros (máximo de 3)**")
    bairros = st.multiselect("", get_bairros_disponiveis(engine)['bairro'].tolist(), 
                            max_selections=3,
                            key="bairros", 
                            label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

# Botão centralizado com estilo
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if 'mostrar_grafico_umi_temp' not in st.session_state:
        st.session_state.mostrar_grafico_umi_temp = True
    
    st.button("🔄 Alternar Modo de Visualização", 
              key="troca_exibicao_umi_temp",
              on_click=lambda: st.session_state.update({"mostrar_grafico_umi_temp": not st.session_state.mostrar_grafico_umi_temp}))

# Dados de temperatura e umidade
params = {"data_ini": data_ini, "data_fim": data_fim, "bairros": bairros}
df_temp = checagem_data(get_temperatura(engine, params))
df_umi = checagem_data(get_umidade(engine, params))

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🌡️ Análise de Temperatura")
    
    if not df_temp.empty:
        if st.session_state.mostrar_grafico_umi_temp:
            st.altair_chart(chart_temperatura(df_temp).interactive(), use_container_width=True)
        else:
            st.dataframe(df_temp, use_container_width=True)
    else:
        st.warning("⚠️ Nenhum dado de temperatura encontrado para os filtros selecionados.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 💧 Análise de Umidade")
    
    if not df_umi.empty:
        if st.session_state.mostrar_grafico_umi_temp:
            st.altair_chart(chart_umidade(df_umi).interactive(), use_container_width=True)
        else:
            st.dataframe(df_umi, use_container_width=True)
    else:
        st.warning("⚠️ Nenhum dado de umidade encontrado para os filtros selecionados.")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer elegante
st.markdown("""
<div class="footer">
    <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">⚡ Weather Sync</p>
    <p style="font-size: 0.9rem; opacity: 0.7;">Tecnologia avançada para monitoramento climático inteligente</p>
</div>
""", unsafe_allow_html=True)