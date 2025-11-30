"""
Exemplos de uso direto do Sistema Fuzzy de Avaliação de Apresentações
Execute: python exemplo_uso.py
"""

from fuzzy_system import AvaliacaoApresentacaoFuzzy


def exemplo_basico():
    """Exemplo básico de uso do sistema"""
    print("\n" + "="*70)
    print("EXEMPLO 1: Uso Básico")
    print("="*70)

    
    sistema = AvaliacaoApresentacaoFuzzy()


    resultado = sistema.avaliar(
        clareza_val=7.5,
        dominio_val=8.0,
        ritmo_val=6.0,
        materiais_val=7.0,
        engajamento_val=8.5,
        organizacao_val=8.0
    )

    
    print(f"\nNota: {resultado['nota']}/10")
    print(f"Classificação: {resultado['classificacao']}")
    print(f"\nFeedback:\n{resultado['feedback']}")


def exemplo_multiplos_casos():
    """Avalia múltiplos casos e compara resultados"""
    print("\n" + "="*70)
    print("EXEMPLO 2: Avaliação de Múltiplos Casos")
    print("="*70)

    sistema = AvaliacaoApresentacaoFuzzy()

    casos = [
        {
            'nome': 'Estudante A - Muito preparado',
            'valores': (9.0, 9.0, 6.0, 8.0, 9.0, 9.0)
        },
        {
            'nome': 'Estudante B - Bem preparado',
            'valores': (7.0, 7.5, 5.5, 7.0, 7.0, 7.5)
        },
        {
            'nome': 'Estudante C - Razoável',
            'valores': (5.0, 5.5, 5.0, 5.0, 4.5, 5.0)
        },
        {
            'nome': 'Estudante D - Precisa melhorar',
            'valores': (3.0, 4.0, 4.0, 3.0, 3.0, 3.0)
        }
    ]

    resultados = []
    for caso in casos:
        c, d, r, m, e, o = caso['valores']
        resultado = sistema.avaliar(c, d, r, m, e, o)
        resultados.append({
            'nome': caso['nome'],
            'nota': resultado['nota'],
            'classificacao': resultado['classificacao']
        })

    
    print("\nComparação de Notas:")
    print("-" * 70)
    for res in resultados:
        print(f"{res['nome']:35s} → {res['nota']:4.1f}/10 - {res['classificacao']}")

    
    notas = [r['nota'] for r in resultados]
    print("\nEstatísticas:")
    print(f"  Média: {sum(notas)/len(notas):.2f}")
    print(f"  Máxima: {max(notas):.2f}")
    print(f"  Mínima: {min(notas):.2f}")


def exemplo_analise_criterio():
    """Analisa como cada critério afeta a nota"""
    print("\n" + "="*70)
    print("EXEMPLO 3: Análise de Impacto dos Critérios")
    print("="*70)

    sistema = AvaliacaoApresentacaoFuzzy()


    base = [5.0, 5.0, 5.0, 5.0, 5.0, 5.0]
    resultado_base = sistema.avaliar(*base)

    print(f"\nCaso Base (todos 5.0): {resultado_base['nota']:.2f}/10")
    print("\nImpacto ao aumentar cada critério para 9.0:\n")

    criterios = ['Clareza', 'Domínio', 'Ritmo', 'Materiais', 'Engajamento', 'Organização']

    for i, criterio in enumerate(criterios):
        valores = base.copy()
        valores[i] = 9.0
        resultado = sistema.avaliar(*valores)
        impacto = resultado['nota'] - resultado_base['nota']
        print(f"  {criterio:15s}: {resultado['nota']:4.2f}/10 (Δ +{impacto:4.2f})")


def exemplo_casos_extremos():
    """Testa casos extremos do sistema"""
    print("\n" + "="*70)
    print("EXEMPLO 4: Casos Extremos")
    print("="*70)

    sistema = AvaliacaoApresentacaoFuzzy()

    casos_extremos = [
        {
            'nome': 'Tudo Perfeito (9.5, 9.5, 5, 9, 9.5, 9.5)',
            'valores': (9.5, 9.5, 5.0, 9.0, 9.5, 9.5)
        },
        {
            'nome': 'Tudo Mínimo (0, 0, 0, 0, 0, 0)',
            'valores': (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        },
        {
            'nome': 'Apenas Clareza Alta (10, 0, 0, 0, 0, 0)',
            'valores': (10.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        },
        {
            'nome': 'Apenas Organização Alta (0, 0, 0, 0, 0, 10)',
            'valores': (0.0, 0.0, 0.0, 0.0, 0.0, 10.0)
        }
    ]

    print()
    for caso in casos_extremos:
        resultado = sistema.avaliar(*caso['valores'])
        print(f"{caso['nome']:45s}")
        print(f"  → Nota: {resultado['nota']:4.2f}/10 - {resultado['classificacao']}\n")


def exemplo_cenario_real():
    """Simula avaliação de uma apresentação real"""
    print("\n" + "="*70)
    print("EXEMPLO 5: Cenário Real - Apresentação de TCC")
    print("="*70)

    sistema = AvaliacaoApresentacaoFuzzy()

    print("\n🎓 Situação:")
    print("  João apresentou seu TCC sobre IA. O avaliador observou:")
    print("  - Explicou o conteúdo de forma clara (8/10)")
    print("  - Demonstrou bom domínio do assunto (9/10)")
    print("  - Falou um pouco rápido no início (6.5/10)")
    print("  - Slides bem elaborados (8.5/10)")
    print("  - Boa interação com a banca (7.5/10)")
    print("  - Apresentação bem organizada (8/10)")

    resultado = sistema.avaliar(
        clareza_val=8.0,
        dominio_val=9.0,
        ritmo_val=6.5,
        materiais_val=8.5,
        engajamento_val=7.5,
        organizacao_val=8.0
    )

    print("\n📊 Avaliação Fuzzy:")
    print(f"  Nota Final: {resultado['nota']}/10")
    print(f"  Classificação: {resultado['classificacao']}")
    print(f"\n💡 Feedback para João:")
    print(resultado['feedback'])


def exemplo_visualizacao():
    """Gera visualização das funções de pertinência"""
    print("\n" + "="*70)
    print("EXEMPLO 6: Visualização de Funções de Pertinência")
    print("="*70)

    sistema = AvaliacaoApresentacaoFuzzy()

    print("\nGerando gráficos das funções de pertinência...")

    try:
        import matplotlib.pyplot as plt
        fig = sistema.visualizar_pertinencias()
        plt.savefig('funcoes_pertinencia.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Gráficos salvos em: funcoes_pertinencia.png")
        print("   (Abra o arquivo para visualizar)")
    except Exception as e:
        print(f"⚠️ Erro ao gerar visualização: {e}")
        print("   Use a interface Streamlit para visualizar os gráficos")


def exemplo_comparacao_avaliadores():
    """Simula comparação entre múltiplos avaliadores"""
    print("\n" + "="*70)
    print("EXEMPLO 7: Consenso entre Avaliadores")
    print("="*70)

    sistema = AvaliacaoApresentacaoFuzzy()

    print("\n📋 Situação:")
    print("  Três professores avaliaram a mesma apresentação:")
    print()

    avaliadores = [
        {
            'nome': 'Prof. Silva',
            'valores': (8.0, 8.5, 6.0, 7.5, 8.0, 8.0)
        },
        {
            'nome': 'Prof. Santos',
            'valores': (7.5, 9.0, 5.5, 8.0, 7.5, 8.5)
        },
        {
            'nome': 'Prof. Oliveira',
            'valores': (8.5, 8.0, 6.5, 7.0, 8.5, 7.5)
        }
    ]

    notas = []
    for aval in avaliadores:
        resultado = sistema.avaliar(*aval['valores'])
        notas.append(resultado['nota'])
        print(f"{aval['nome']:20s}: {resultado['nota']:.2f}/10 - {resultado['classificacao']}")

    media = sum(notas) / len(notas)
    print(f"\n{'Média Fuzzy':20s}: {media:.2f}/10")
    print(f"Desvio Padrão: {(sum((n-media)**2 for n in notas)/len(notas))**0.5:.2f}")


def exemplo_autoavaliacao():
    """Exemplo de uso para autoavaliação"""
    print("\n" + "="*70)
    print("EXEMPLO 8: Autoavaliação")
    print("="*70)

    sistema = AvaliacaoApresentacaoFuzzy()

    print("\n🤔 Você está preparando uma apresentação importante.")
    print("   Avalie a si mesmo nos seguintes critérios (0-10):\n")


    autoavaliacao = {
        'clareza': 6.5,
        'dominio': 7.0,
        'ritmo': 5.0,
        'materiais': 8.0,
        'engajamento': 5.5,
        'organizacao': 6.0
    }

    print(f"  Clareza da explicação: {autoavaliacao['clareza']}")
    print(f"  Domínio do conteúdo: {autoavaliacao['dominio']}")
    print(f"  Ritmo da fala: {autoavaliacao['ritmo']}")
    print(f"  Qualidade dos slides: {autoavaliacao['materiais']}")
    print(f"  Engajamento: {autoavaliacao['engajamento']}")
    print(f"  Organização: {autoavaliacao['organizacao']}")

    resultado = sistema.avaliar(
        autoavaliacao['clareza'],
        autoavaliacao['dominio'],
        autoavaliacao['ritmo'],
        autoavaliacao['materiais'],
        autoavaliacao['engajamento'],
        autoavaliacao['organizacao']
    )

    print(f"\n📊 Sua avaliação atual: {resultado['nota']:.2f}/10 - {resultado['classificacao']}")
    print(f"\n💡 Sugestões de melhoria:")
    print(resultado['feedback'])


def menu_principal():
    """Menu para escolher qual exemplo executar"""
    print("\n" + "="*70)
    print("🎤 EXEMPLOS DE USO - Sistema de Avaliação Fuzzy")
    print("="*70)
    print("\nEscolha um exemplo para executar:")
    print("  1. Uso Básico")
    print("  2. Múltiplos Casos")
    print("  3. Análise de Impacto dos Critérios")
    print("  4. Casos Extremos")
    print("  5. Cenário Real (Apresentação de TCC)")
    print("  6. Visualização de Funções de Pertinência")
    print("  7. Consenso entre Avaliadores")
    print("  8. Autoavaliação")
    print("  9. Executar TODOS os exemplos")
    print("  0. Sair")
    print("\n" + "="*70)


def executar_todos():
    """Executa todos os exemplos"""
    exemplo_basico()
    exemplo_multiplos_casos()
    exemplo_analise_criterio()
    exemplo_casos_extremos()
    exemplo_cenario_real()
    exemplo_visualizacao()
    exemplo_comparacao_avaliadores()
    exemplo_autoavaliacao()


if __name__ == "__main__":
    try:
        
        print("\n🚀 Executando todos os exemplos...\n")
        executar_todos()

        print("\n" + "="*70)
        print("✅ EXEMPLOS CONCLUÍDOS!")
        print("="*70)
        print("\n📝 Próximos passos:")
        print("  1. Execute: streamlit run app.py")
        print("  2. Abra o notebook: avaliacao_fuzzy_colab.ipynb")
        print("  3. Leia a documentação: README.md")
        print("\n" + "="*70 + "\n")

    except ImportError as e:
        print("\n❌ ERRO: Dependências não instaladas!")
        print("\n📦 Execute primeiro:")
        print("   pip install -r requirements.txt")
        print(f"\nDetalhes: {e}\n")
    except Exception as e:
        print(f"\n❌ ERRO: {e}\n")
        import traceback
        traceback.print_exc()
