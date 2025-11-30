"""
Script de teste rápido do sistema fuzzy
Execute: python teste_rapido.py
"""

from fuzzy_system import AvaliacaoApresentacaoFuzzy

def teste_rapido():
    """Executa testes rápidos do sistema"""
    print("=" * 70)
    print("🧪 TESTE RÁPIDO - Sistema de Avaliação Fuzzy")
    print("=" * 70)

    # Cria o sistema
    print("\n1️⃣ Criando sistema fuzzy...")
    sistema = AvaliacaoApresentacaoFuzzy()
    print("✅ Sistema criado com sucesso!")

    # Define casos de teste (agora com 6 parâmetros: +organizacao)
    casos_teste = [
        {
            'nome': '🟣 Apresentação PERFEITA (Nota ~10)',
            'valores': (9.5, 9.5, 5.0, 9.0, 9.5, 9.5),
            'esperado': 'Excelente'
        },
        {
            'nome': '🟣 Apresentação EXCELENTE',
            'valores': (9.0, 9.5, 6.0, 8.5, 9.0, 9.0),
            'esperado': 'Excelente'
        },
        {
            'nome': '🟣 Organização Compensa Materiais',
            'valores': (8.5, 9.0, 5.0, 5.0, 8.0, 9.5),
            'esperado': 'Excelente'
        },
        {
            'nome': '🔵 Apresentação MUITO BOA',
            'valores': (8.0, 8.5, 5.5, 6.0, 8.0, 7.5),
            'esperado': 'Muito Bom'
        },
        {
            'nome': '🟢 Apresentação BOA',
            'valores': (7.0, 7.0, 6.0, 7.0, 6.5, 7.0),
            'esperado': 'Bom'
        },
        {
            'nome': '🟡 Apresentação ACEITÁVEL',
            'valores': (5.0, 5.0, 5.0, 5.0, 5.0, 5.0),
            'esperado': 'Aceitável'
        },
        {
            'nome': '🔴 Apresentação PRECISA MELHORAR',
            'valores': (2.0, 3.0, 4.0, 2.5, 2.0, 2.0),
            'esperado': 'Precisa Melhorar'
        }
    ]

    # Executa testes
    print("\n2️⃣ Executando 7 casos de teste...\n")

    sucessos = 0
    for i, caso in enumerate(casos_teste, 1):
        print(f"\n{'-' * 70}")
        print(f"Teste {i}: {caso['nome']}")
        print(f"{'-' * 70}")

        clareza, dominio, ritmo, materiais, engajamento, organizacao = caso['valores']

        print(f"  Clareza:      {clareza}/10")
        print(f"  Domínio:      {dominio}/10")
        print(f"  Ritmo:        {ritmo}/10")
        print(f"  Materiais:    {materiais}/10")
        print(f"  Engajamento:  {engajamento}/10")
        print(f"  Organização:  {organizacao}/10")

        resultado = sistema.avaliar(clareza, dominio, ritmo, materiais, engajamento, organizacao)

        print(f"\n  📊 RESULTADO:")
        print(f"     Nota: {resultado['nota']}/10")
        print(f"     Classificação: {resultado['classificacao']}")

        # Verifica se está correto
        if resultado['classificacao'] == caso['esperado']:
            print(f"  ✅ PASSOU (esperado: {caso['esperado']})")
            sucessos += 1
        else:
            print(f"  ❌ FALHOU (esperado: {caso['esperado']}, obtido: {resultado['classificacao']})")

    # Resumo
    print(f"\n{'=' * 70}")
    print(f"📈 RESUMO DOS TESTES")
    print(f"{'=' * 70}")
    print(f"  Total de testes: {len(casos_teste)}")
    print(f"  ✅ Sucessos: {sucessos}")
    print(f"  ❌ Falhas: {len(casos_teste) - sucessos}")
    print(f"  Taxa de acerto: {(sucessos/len(casos_teste))*100:.1f}%")

    if sucessos == len(casos_teste):
        print(f"\n🎉 PERFEITO! Todos os testes passaram!")
    else:
        print(f"\n⚠️ Alguns testes falharam. Verifique as regras fuzzy.")

    print(f"{'=' * 70}\n")

    # Teste de visualização
    print("3️⃣ Testando visualização de funções de pertinência...")
    try:
        import matplotlib
        matplotlib.use('Agg')  # Backend não-interativo para teste
        fig = sistema.visualizar_pertinencias()
        print("✅ Visualização criada com sucesso!")
        print("   (Gráficos disponíveis na interface Streamlit)")
    except Exception as e:
        print(f"⚠️ Erro ao criar visualização: {e}")

    print("\n" + "=" * 70)
    print("✅ TESTE RÁPIDO CONCLUÍDO!")
    print("=" * 70)
    print("\n📝 Próximos passos:")
    print("   1. Execute: streamlit run app.py")
    print("   2. Abra o navegador em http://localhost:8501")
    print("   3. Teste a interface interativa!")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    try:
        teste_rapido()
    except ImportError as e:
        print("\n❌ ERRO: Dependências não instaladas!")
        print("\n📦 Execute primeiro:")
        print("   pip install -r requirements.txt")
        print(f"\nDetalhes do erro: {e}\n")
    except Exception as e:
        print(f"\n❌ ERRO durante o teste: {e}\n")
        import traceback
        traceback.print_exc()
