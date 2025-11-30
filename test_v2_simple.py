"""
Teste simples do sistema V2 para verificar se funciona
"""

try:
    print("Importando módulos...")
    from fuzzy_system_v2 import AvaliacaoApresentacaoFuzzyV2

    print("✅ Importação bem-sucedida!")

    print("\nCriando sistema com Gaussiana...")
    sistema = AvaliacaoApresentacaoFuzzyV2(resolution=1001, function_type='gaussian')

    print("✅ Sistema criado!")

    print("\nTestando avaliação...")
    resultado = sistema.avaliar(
        clareza_val=9.0,
        dominio_val=9.0,
        ritmo_val=5.0,
        materiais_val=9.0,
        engajamento_val=9.0,
        organizacao_val=9.0
    )

    print(f"\n✅ Avaliação bem-sucedida!")
    print(f"Nota: {resultado['nota']}/10")
    print(f"Raw Score: {resultado['raw_score']:.6f}")
    print(f"Classificação: {resultado['classificacao']}")

    print("\n" + "="*70)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("="*70)

except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
