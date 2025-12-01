
import streamlit as st
import matplotlib.pyplot as plt
from fuzzy_system_v2 import AvaliacaoApresentacaoFuzzyV2
from fuzzy_core import MembershipFunctionFactory
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Avaliador Fuzzy",
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
    .raw-score-display {
        font-size: 1rem;
        text-align: center;
        color: #888;
        font-family: monospace;
    }
    .classificacao-display {
        font-size: 1.5rem;
        text-align: center;
        color: #555;
        margin-top: 10px;
    }
    .config-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        background-color: #e3f2fd;
        color: #1976d2;
        font-size: 0.85rem;
        margin: 4px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🎤 Avaliador de Apresentações Fuzzy</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sistema modular com funções configuráveis e valores decimais precisos</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Configurações do Sistema")

    st.markdown("### 🔧 Tipo de Função de Pertinência")
    function_type = st.selectbox(
        "Escolha o tipo de função:",
        options=['gaussian', 'triangular', 'trapezoidal', 'bell', 'sigmoidal'],
        format_func=lambda x: {
            'gaussian': '🔵 Gaussiana (suave)',
            'triangular': '🔺 Triangular (linear)',
            'trapezoidal': '🔶 Trapezoidal (plateau)',
            'bell': '🔔 Bell (sino generalizado)',
            'sigmoidal': '📈 Sigmoidal (curva S)'
        }[x],
        help="Diferentes tipos produzem resultados ligeiramente diferentes"
    )

    resolution = 1001

    st.divider()

    st.markdown("### 📚 Sobre o Sistema")
    st.markdown(f"""
    **Configuração Atual:**

    <div class="config-badge">🔧 {function_type.title()}</div>
    <div class="config-badge">📊 1001 pontos (alta precisão)</div>

    **Características:**

    ✅ **Valores decimais reais** (ex: 7.347, 8.923)

    ✅ **5 tipos de funções** configuráveis

    ✅ **Nota máxima 10.0**

    ✅ **Regras com compensação** inteligente

    ✅ **Pesos implícitos** por critério

    ✅ **Arquitetura modular** escalável

    ### 📖 Critérios Avaliados:

    - **Clareza** (peso: 1.2) 🔍
    - **Domínio** (peso: 1.3) 📚
    - **Ritmo** (peso: 0.8) ⏱️
    - **Materiais** (peso: 0.9) 📊
    - **Engajamento** (peso: 1.1) 🤝
    - **Organização** (peso: 1.15) 📋
    """, unsafe_allow_html=True)

    st.divider()

    if st.button("📖 Ver Documentação"):
        st.session_state['show_docs'] = True

@st.cache_resource
def carregar_sistema(func_type, res):
    try:
        return AvaliacaoApresentacaoFuzzyV2(
            resolution=res,
            function_type=func_type
        )
    except Exception as e:
        st.error(f"Erro ao carregar sistema: {e}")
        return None

sistema = carregar_sistema(function_type, resolution)

if sistema is None:
    st.error("❌ Falha ao inicializar o sistema fuzzy. Verifique os logs do Docker.")
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs(["🎯 Avaliação", "📊 Comparação de Funções", "📈 Gráficos", "🧪 Testes"])

with tab1:
    st.header("Avalie a Apresentação")

    st.info(f"💡 **Modo Avançado Ativo:** Usando funções **{function_type}** com **{resolution} pontos** de resolução. Você pode inserir valores decimais precisos!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Conteúdo e Comunicação")

        input_mode = st.radio(
            "Modo de entrada:",
            options=['slider', 'decimal'],
            format_func=lambda x: '🎚️ Slider (0.5 steps)' if x == 'slider' else '🔢 Decimal Preciso',
            horizontal=True
        )

        if input_mode == 'slider':
            clareza = st.slider(
                "**Clareza** - Quão clara foi a explicação?",
                min_value=0.0, max_value=10.0, value=5.0, step=0.5,
                help="Peso: 1.2 | 0 = Muito confusa | 10 = Extremamente clara"
            )

            dominio = st.slider(
                "**Domínio do Conteúdo** - Conhecimento demonstrado",
                min_value=0.0, max_value=10.0, value=5.0, step=0.5,
                help="Peso: 1.3 (mais importante) | 0 = Não domina | 10 = Domínio completo"
            )

            ritmo = st.slider(
                "**Ritmo da Fala** - Velocidade e fluidez",
                min_value=0.0, max_value=10.0, value=5.0, step=0.5,
                help="Peso: 0.8 (menos crítico) | 0 = Muito devagar | 5 = Ideal | 10 = Muito rápido"
            )
        else:
            clareza = st.number_input(
                "**Clareza** - Valor decimal preciso",
                min_value=0.0, max_value=10.0, value=5.0, step=0.001, format="%.3f",
                help="Peso: 1.2 | Exemplo: 7.347"
            )

            dominio = st.number_input(
                "**Domínio do Conteúdo** - Valor decimal preciso",
                min_value=0.0, max_value=10.0, value=5.0, step=0.001, format="%.3f",
                help="Peso: 1.3 (mais importante) | Exemplo: 8.923"
            )

            ritmo = st.number_input(
                "**Ritmo da Fala** - Valor decimal preciso",
                min_value=0.0, max_value=10.0, value=5.0, step=0.001, format="%.3f",
                help="Peso: 0.8 (menos crítico) | Exemplo: 6.147"
            )

    with col2:
        st.subheader("Recursos e Interação")

        if input_mode == 'slider':
            materiais = st.slider(
                "**Qualidade dos Materiais** - Slides e recursos visuais",
                min_value=0.0, max_value=10.0, value=5.0, step=0.5,
                help="Peso: 0.9 | 0 = Ruins/inexistentes | 10 = Excelentes"
            )

            engajamento = st.slider(
                "**Engajamento** - Interação com a plateia",
                min_value=0.0, max_value=10.0, value=5.0, step=0.5,
                help="Peso: 1.1 | 0 = Nenhuma interação | 10 = Muito envolvente"
            )

            organizacao = st.slider(
                "**Organização** - Estrutura e sequência lógica",
                min_value=0.0, max_value=10.0, value=5.0, step=0.5,
                help="Peso: 1.15 | 0 = Desorganizada | 10 = Perfeitamente estruturada"
            )
        else:
            materiais = st.number_input(
                "**Qualidade dos Materiais** - Valor decimal preciso",
                min_value=0.0, max_value=10.0, value=5.0, step=0.001, format="%.3f",
                help="Peso: 0.9 | Exemplo: 7.891"
            )

            engajamento = st.number_input(
                "**Engajamento** - Valor decimal preciso",
                min_value=0.0, max_value=10.0, value=5.0, step=0.001, format="%.3f",
                help="Peso: 1.1 | Exemplo: 8.456"
            )

            organizacao = st.number_input(
                "**Organização** - Valor decimal preciso",
                min_value=0.0, max_value=10.0, value=5.0, step=0.001, format="%.3f",
                help="Peso: 1.15 | Exemplo: 9.234"
            )

    st.divider()

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        avaliar_btn = st.button("🎯 Avaliar Apresentação", type="primary", use_container_width=True)

    if avaliar_btn:
        with st.spinner(f"Processando inferência fuzzy {function_type} com {resolution} pontos..."):
            resultado = sistema.avaliar(clareza, dominio, ritmo, materiais, engajamento, organizacao)

        st.success("✅ Avaliação concluída!")

        col_res1, col_res2 = st.columns(2)

        with col_res1:
            st.markdown('<div class="resultado-box">', unsafe_allow_html=True)
            st.markdown(f'<div class="nota-display">{resultado["nota"]}/10</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="raw-score-display">Raw Score: {resultado["raw_score"]:.6f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="classificacao-display">{resultado["classificacao"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_res2:
            st.markdown('<div class="resultado-box">', unsafe_allow_html=True)
            st.markdown("### 💡 Feedback e Sugestões")
            st.markdown(resultado['feedback'])
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("### 📋 Valores Processados")
        input_df = pd.DataFrame({
            'Critério': ['Clareza', 'Domínio', 'Ritmo', 'Materiais', 'Engajamento', 'Organização'],
            'Valor Inserido': [clareza, dominio, ritmo, materiais, engajamento, organizacao],
            'Peso': [1.2, 1.3, 0.8, 0.9, 1.1, 1.15]
        })
        st.dataframe(input_df, use_container_width=True, hide_index=True)

        st.subheader("📊 Análise dos Critérios")

        import plotly.graph_objects as go

        categorias = ['Clareza', 'Domínio', 'Ritmo', 'Materiais', 'Engajamento', 'Organização']
        valores = [clareza, dominio, ritmo, materiais, engajamento, organizacao]

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
    st.header("📊 Comparação de Tipos de Funções")
    st.markdown("Veja como diferentes funções de pertinência afetam o resultado para **os mesmos valores de entrada**")

    st.info("💡 Esta comparação usa resolução de 1001 pontos para todos os tipos")

    col_comp1, col_comp2 = st.columns(2)

    with col_comp1:
        st.subheader("Valores de Entrada")
        comp_clareza = st.number_input("Clareza:", 0.0, 10.0, 9.0, 0.1, key='comp_clareza')
        comp_dominio = st.number_input("Domínio:", 0.0, 10.0, 9.0, 0.1, key='comp_dominio')
        comp_ritmo = st.number_input("Ritmo:", 0.0, 10.0, 5.0, 0.1, key='comp_ritmo')

    with col_comp2:
        st.write("")  
        st.write("")  
        comp_materiais = st.number_input("Materiais:", 0.0, 10.0, 9.0, 0.1, key='comp_materiais')
        comp_engajamento = st.number_input("Engajamento:", 0.0, 10.0, 9.0, 0.1, key='comp_engajamento')
        comp_organizacao = st.number_input("Organização:", 0.0, 10.0, 9.0, 0.1, key='comp_organizacao')

    if st.button("🔍 Comparar Todos os Tipos", type="primary"):
        tipos = ['gaussian', 'triangular', 'trapezoidal', 'bell', 'sigmoidal']

        comparacao_results = []

        progress_bar = st.progress(0)

        for i, tipo in enumerate(tipos):
            sistema_temp = AvaliacaoApresentacaoFuzzyV2(
                resolution=1001,
                function_type=tipo
            )

            resultado = sistema_temp.avaliar(
                clareza_val=comp_clareza,
                dominio_val=comp_dominio,
                ritmo_val=comp_ritmo,
                materiais_val=comp_materiais,
                engajamento_val=comp_engajamento,
                organizacao_val=comp_organizacao
            )

            comparacao_results.append({
                'Tipo de Função': tipo.title(),
                'Nota Final': resultado['nota'],
                'Raw Score': f"{resultado['raw_score']:.6f}",
                'Classificação': resultado['classificacao']
            })

            progress_bar.progress((i + 1) / len(tipos))

        st.success("✅ Comparação concluída!")

        df_comp = pd.DataFrame(comparacao_results)
        st.dataframe(df_comp, use_container_width=True, hide_index=True)

        import plotly.express as px

        fig = px.bar(
            df_comp,
            x='Tipo de Função',
            y='Nota Final',
            color='Classificação',
            title='Comparação de Notas por Tipo de Função de Pertinência',
            height=400,
            text='Nota Final'
        )
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 📊 Análise Estatística")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Nota Média", f"{df_comp['Nota Final'].mean():.2f}")
        with col2:
            st.metric("Variação", f"{df_comp['Nota Final'].max() - df_comp['Nota Final'].min():.2f}")
        with col3:
            st.metric("Desvio Padrão", f"{df_comp['Nota Final'].std():.3f}")

with tab3:
    st.header("Funções de Pertinência")
    st.markdown(f"Visualização das funções de pertinência **{function_type}** com **{resolution} pontos** de resolução")

    if st.button("🔄 Gerar Gráficos das Funções", type="primary"):
        with st.spinner("Gerando gráficos..."):
            fig = sistema.visualizar_pertinencias()
            st.pyplot(fig)
            plt.close()

with tab4:
    st.header("🧪 Exemplos de Teste do Sistema")
    st.markdown("Teste o sistema com casos predefinidos ou valores decimais aleatórios")

    casos_teste = [
        {
            'nome': '🟣 Perfeição (Nota ~10.0)',
            'clareza': 9.5, 'dominio': 9.5, 'ritmo': 5.0, 'materiais': 9.0, 'engajamento': 9.5, 'organizacao': 9.5
        },
        {
            'nome': '🟣 Excelente',
            'clareza': 9.0, 'dominio': 9.5, 'ritmo': 6.0, 'materiais': 8.5, 'engajamento': 9.0, 'organizacao': 9.0
        },
        {
            'nome': '🟣 Organização Compensa Materiais',
            'clareza': 8.5, 'dominio': 9.0, 'ritmo': 5.0, 'materiais': 5.0, 'engajamento': 8.0, 'organizacao': 9.5
        },
        {
            'nome': '🔵 Muito Bom',
            'clareza': 8.0, 'dominio': 8.5, 'ritmo': 5.5, 'materiais': 6.0, 'engajamento': 8.0, 'organizacao': 7.5
        },
        {
            'nome': '🟢 Bom',
            'clareza': 7.0, 'dominio': 7.0, 'ritmo': 6.0, 'materiais': 7.0, 'engajamento': 6.5, 'organizacao': 7.0
        },
        {
            'nome': '🟡 Aceitável',
            'clareza': 5.0, 'dominio': 5.0, 'ritmo': 5.0, 'materiais': 5.0, 'engajamento': 5.0, 'organizacao': 5.0
        },
        {
            'nome': '🔴 Precisa Melhorar',
            'clareza': 2.0, 'dominio': 3.0, 'ritmo': 4.0, 'materiais': 2.5, 'engajamento': 2.0, 'organizacao': 2.0
        },
        {
            'nome': '🔬 Teste com Decimais Precisos',
            'clareza': 7.347, 'dominio': 8.923, 'ritmo': 5.147, 'materiais': 6.789, 'engajamento': 8.456, 'organizacao': 7.891
        }
    ]

    col_test1, col_test2 = st.columns(2)

    with col_test1:
        if st.button("▶️ Executar Testes Predefinidos", type="primary", use_container_width=True):
            resultados_testes = []

            progress_bar = st.progress(0)
            status_text = st.empty()

            for i, caso in enumerate(casos_teste):
                status_text.text(f"Testando: {caso['nome']}...")

                resultado = sistema.avaliar(
                    caso['clareza'], caso['dominio'], caso['ritmo'],
                    caso['materiais'], caso['engajamento'], caso['organizacao']
                )

                resultados_testes.append({
                    'Cenário': caso['nome'],
                    'Clareza': caso['clareza'],
                    'Domínio': caso['dominio'],
                    'Ritmo': caso['ritmo'],
                    'Materiais': caso['materiais'],
                    'Engajamento': caso['engajamento'],
                    'Organização': caso['organizacao'],
                    'Nota Final': resultado['nota'],
                    'Raw Score': f"{resultado['raw_score']:.6f}",
                    'Classificação': resultado['classificacao']
                })

                progress_bar.progress((i + 1) / len(casos_teste))

            status_text.text("✅ Testes concluídos!")

            df_resultados = pd.DataFrame(resultados_testes)
            st.dataframe(df_resultados, use_container_width=True, hide_index=True)

            st.subheader("📊 Estatísticas dos Testes")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Nota Média", f"{df_resultados['Nota Final'].mean():.2f}")
            with col2:
                st.metric("Nota Máxima", f"{df_resultados['Nota Final'].max():.2f}")
            with col3:
                st.metric("Nota Mínima", f"{df_resultados['Nota Final'].min():.2f}")

            import plotly.express as px

            fig = px.bar(
                df_resultados,
                x='Cenário',
                y='Nota Final',
                color='Classificação',
                title=f'Distribuição de Notas ({function_type.title()}, {resolution} pontos)',
                height=400
            )
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

    with col_test2:
        if st.button("🎲 Gerar Teste Aleatório com Decimais", type="secondary", use_container_width=True):
            np.random.seed()
            random_values = {
                'clareza': round(np.random.uniform(0, 10), 3),
                'dominio': round(np.random.uniform(0, 10), 3),
                'ritmo': round(np.random.uniform(0, 10), 3),
                'materiais': round(np.random.uniform(0, 10), 3),
                'engajamento': round(np.random.uniform(0, 10), 3),
                'organizacao': round(np.random.uniform(0, 10), 3)
            }

            resultado_random = sistema.avaliar(
                random_values['clareza'],
                random_values['dominio'],
                random_values['ritmo'],
                random_values['materiais'],
                random_values['engajamento'],
                random_values['organizacao']
            )

            st.success("🎲 Valores aleatórios gerados!")

            st.markdown("### 📋 Valores Aleatórios:")
            for criterio, valor in random_values.items():
                st.write(f"**{criterio.title()}:** {valor}")

            st.markdown("### 📊 Resultado:")
            st.markdown(f"**Nota:** {resultado_random['nota']}/10")
            st.markdown(f"**Raw Score:** {resultado_random['raw_score']:.6f}")
            st.markdown(f"**Classificação:** {resultado_random['classificacao']}")

st.divider()

col_footer1, col_footer2 = st.columns(2)

with col_footer1:
    st.markdown("### 📚 Recursos")
    st.markdown("""
    - Código fonte no GitHub
    """)

with col_footer2:
    st.markdown("### 🔧 Configuração Atual")
    st.markdown(f"""
    - **Função:** {function_type}
    - **Resolução:** {resolution} pontos (fixa)
    - **Total de Regras:** {sistema.get_info()['total_rules']}
    """)

st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Sistema de Avaliação de Apresentações com Lógica Fuzzy</strong></p>
    <p>Desenvolvido com Python, scikit-fuzzy, Streamlit e arquitetura modular</p>
    <p>Suporta valores decimais precisos e múltiplos tipos de funções de pertinência</p>
</div>
""", unsafe_allow_html=True)
