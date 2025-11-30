"""
Interface Web para o Sistema de Avaliação de Apresentações com Lógica Fuzzy
Desenvolvido com Streamlit
"""

import streamlit as st
import matplotlib.pyplot as plt
from fuzzy_system import AvaliacaoApresentacaoFuzzy
import pandas as pd

st.set_page_config(
    page_title="Avaliador Fuzzy de Apresentações",
    page_icon="🎤",
    layout="wide"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .resultado-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 20px 0;
    }
    .nota-display {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
    }
    .classificacao-display {
        font-size: 1.5rem;
        text-align: center;
        color: #555;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown('<h1 class="main-header">🎤 Avaliador de Apresentações com Lógica Fuzzy</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sistema inteligente para avaliar apresentações orais usando inferência fuzzy</p>', unsafe_allow_html=True)

# Inicializa o sistema fuzzy (usando cache para performance)
@st.cache_resource
def carregar_sistema():
    return AvaliacaoApresentacaoFuzzy()

sistema = carregar_sistema()

# Sidebar com informações
with st.sidebar:
    st.header("📚 Sobre o Sistema")
    st.markdown("""
    Este sistema utiliza **Lógica Fuzzy** para avaliar apresentações orais
    com base em 5 critérios principais:

    - **Clareza**: Quão clara foi a explicação
    - **Domínio**: Conhecimento do assunto
    - **Ritmo**: Velocidade e fluidez da fala
    - **Materiais**: Qualidade dos slides/recursos
    - **Engajamento**: Interação com a plateia

    ### Como funciona?
    1. Ajuste os sliders para cada critério (0-10)
    2. Clique em "Avaliar Apresentação"
    3. Receba nota, classificação e feedback

    ### Classificações possíveis:
    - 🔴 Precisa Melhorar (0-3)
    - 🟡 Aceitável (3-5)
    - 🟢 Bom (5-7)
    - 🔵 Muito Bom (7-8.5)
    - 🟣 Excelente (8.5-10)
    """)

    st.divider()

    if st.button("📊 Mostrar Funções de Pertinência"):
        st.session_state['mostrar_graficos'] = True

tab1, tab2, tab3 = st.tabs(["🎯 Avaliação", "📈 Gráficos", "🧪 Exemplos de Teste"])

# TAB 1: Avaliação
with tab1:
    st.header("Avalie a Apresentação")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Conteúdo e Comunicação")
        clareza = st.slider(
            "**Clareza** - Quão clara foi a explicação?",
            min_value=0.0, max_value=10.0, value=5.0, step=0.5,
            help="0 = Muito confusa | 10 = Extremamente clara"
        )

        dominio = st.slider(
            "**Domínio do Conteúdo** - Conhecimento demonstrado",
            min_value=0.0, max_value=10.0, value=5.0, step=0.5,
            help="0 = Não domina | 10 = Domínio completo"
        )

        ritmo = st.slider(
            "**Ritmo da Fala** - Velocidade e fluidez",
            min_value=0.0, max_value=10.0, value=5.0, step=0.5,
            help="0 = Muito devagar | 5 = Ideal | 10 = Muito rápido"
        )

    with col2:
        st.subheader("Recursos e Interação")
        materiais = st.slider(
            "**Qualidade dos Materiais** - Slides e recursos visuais",
            min_value=0.0, max_value=10.0, value=5.0, step=0.5,
            help="0 = Ruins/inexistentes | 10 = Excelentes"
        )

        engajamento = st.slider(
            "**Engajamento** - Interação com a plateia",
            min_value=0.0, max_value=10.0, value=5.0, step=0.5,
            help="0 = Nenhuma interação | 10 = Muito envolvente"
        )

    st.divider()

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        avaliar_btn = st.button("🎯 Avaliar Apresentação", type="primary", use_container_width=True)

    if avaliar_btn:
        with st.spinner("Processando avaliação fuzzy..."):
            resultado = sistema.avaliar(clareza, dominio, ritmo, materiais, engajamento)

        st.success("Avaliação concluída!")

        # Exibir resultados
        col_res1, col_res2 = st.columns(2)

        with col_res1:
            st.markdown('<div class="resultado-box">', unsafe_allow_html=True)
            st.markdown(f'<div class="nota-display">{resultado["nota"]}/10</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="classificacao-display">{resultado["classificacao"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_res2:
            st.markdown('<div class="resultado-box">', unsafe_allow_html=True)
            st.markdown("### 💡 Feedback e Sugestões")
            st.markdown(resultado['feedback'])
            st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("📊 Análise dos Critérios")

        import plotly.graph_objects as go

        categorias = ['Clareza', 'Domínio', 'Ritmo', 'Materiais', 'Engajamento']
        valores = [clareza, dominio, ritmo, materiais, engajamento]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=valores,
            theta=categorias,
            fill='toself',
            name='Avaliação',
            line_color='#1f77b4'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=False,
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Funções de Pertinência")
    st.markdown("Visualização das funções de pertinência fuzzy para cada variável do sistema")

    if st.button("🔄 Gerar Gráficos", type="primary"):
        with st.spinner("Gerando gráficos..."):
            fig = sistema.visualizar_pertinencias()
            st.pyplot(fig)
            plt.close()

with tab3:
    st.header("🧪 Exemplos de Teste do Sistema")
    st.markdown("10+ exemplos demonstrando diferentes cenários de avaliação")

    # Define 10 casos de teste
    casos_teste = [
        {
            'nome': 'Apresentação Excelente',
            'clareza': 9.0, 'dominio': 9.5, 'ritmo': 6.0, 'materiais': 8.5, 'engajamento': 9.0
        },
        {
            'nome': 'Muito Boa com Materiais Simples',
            'clareza': 8.0, 'dominio': 8.5, 'ritmo': 5.5, 'materiais': 6.0, 'engajamento': 8.0
        },
        {
            'nome': 'Boa Apresentação Geral',
            'clareza': 7.0, 'dominio': 7.0, 'ritmo': 6.0, 'materiais': 7.0, 'engajamento': 6.5
        },
        {
            'nome': 'Aceitável com Baixo Engajamento',
            'clareza': 5.0, 'dominio': 6.0, 'ritmo': 5.0, 'materiais': 5.0, 'engajamento': 3.0
        },
        {
            'nome': 'Precisa Melhorar',
            'clareza': 2.0, 'dominio': 3.0, 'ritmo': 4.0, 'materiais': 2.5, 'engajamento': 2.0
        },
        {
            'nome': 'Bom Domínio, Clareza Média',
            'clareza': 5.5, 'dominio': 8.0, 'ritmo': 5.5, 'materiais': 6.0, 'engajamento': 6.0
        },
        {
            'nome': 'Ritmo Rápido Demais',
            'clareza': 6.0, 'dominio': 7.0, 'ritmo': 9.0, 'materiais': 6.5, 'engajamento': 5.0
        },
        {
            'nome': 'Excelentes Materiais',
            'clareza': 7.0, 'dominio': 7.5, 'ritmo': 6.0, 'materiais': 9.5, 'engajamento': 7.0
        },
        {
            'nome': 'Alto Engajamento Compensa',
            'clareza': 6.0, 'dominio': 6.5, 'ritmo': 5.5, 'materiais': 5.5, 'engajamento': 9.0
        },
        {
            'nome': 'Apresentação Mediana',
            'clareza': 5.0, 'dominio': 5.0, 'ritmo': 5.0, 'materiais': 5.0, 'engajamento': 5.0
        },
        {
            'nome': 'Clareza Baixa Prejudica',
            'clareza': 3.0, 'dominio': 7.0, 'ritmo': 6.0, 'materiais': 7.0, 'engajamento': 6.0
        },
        {
            'nome': 'Ritmo Devagar',
            'clareza': 6.0, 'dominio': 6.5, 'ritmo': 2.0, 'materiais': 6.0, 'engajamento': 5.5
        }
    ]

    if st.button("▶️ Executar Todos os Testes", type="primary"):
        resultados_testes = []

        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, caso in enumerate(casos_teste):
            status_text.text(f"Testando: {caso['nome']}...")

            resultado = sistema.avaliar(
                caso['clareza'], caso['dominio'], caso['ritmo'],
                caso['materiais'], caso['engajamento']
            )

            resultados_testes.append({
                'Cenário': caso['nome'],
                'Clareza': caso['clareza'],
                'Domínio': caso['dominio'],
                'Ritmo': caso['ritmo'],
                'Materiais': caso['materiais'],
                'Engajamento': caso['engajamento'],
                'Nota Final': resultado['nota'],
                'Classificação': resultado['classificacao']
            })

            progress_bar.progress((i + 1) / len(casos_teste))

        status_text.text("✅ Testes concluídos!")

        # Exibir resultados em tabela
        df_resultados = pd.DataFrame(resultados_testes)
        st.dataframe(df_resultados, use_container_width=True, hide_index=True)

        # Estatísticas
        st.subheader("📊 Estatísticas dos Testes")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Nota Média", f"{df_resultados['Nota Final'].mean():.2f}")
        with col2:
            st.metric("Nota Máxima", f"{df_resultados['Nota Final'].max():.2f}")
        with col3:
            st.metric("Nota Mínima", f"{df_resultados['Nota Final'].min():.2f}")

        # Gráfico de distribuição
        import plotly.express as px

        fig = px.bar(
            df_resultados,
            x='Cenário',
            y='Nota Final',
            color='Classificação',
            title='Distribuição de Notas por Cenário',
            height=400
        )
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Sistema de Avaliação de Apresentações com Lógica Fuzzy</strong></p>
    <p>Desenvolvido com Python, scikit-fuzzy e Streamlit</p>
</div>
""", unsafe_allow_html=True)
