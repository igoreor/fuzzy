import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional
from fuzzy_core import MembershipFunctionFactory, CriteriaFactory, FuzzyController
from fuzzy_core.criteria_factory import FuzzyCriterion, OutputVariable
from skfuzzy import control as ctrl


class AvaliacaoApresentacaoFuzzyV2:

    def __init__(
        self,
        resolution: int = 1001,
        function_type: str = 'gaussian',
        custom_criteria: Optional[List[FuzzyCriterion]] = None,
        custom_output: Optional[OutputVariable] = None,
        custom_rules_builder: Optional[callable] = None
    ):
        self.resolution = resolution
        self.function_type = function_type

        if custom_criteria is None:
            self.criteria = CriteriaFactory.create_standard_input_criteria(
                resolution=resolution,
                function_type=function_type
            )
        else:
            self.criteria = custom_criteria

        if custom_output is None:
            self.output = CriteriaFactory.create_standard_output(
                resolution=resolution,
                function_type=function_type
            )
        else:
            self.output = custom_output

        self.controller = FuzzyController(
            criteria=self.criteria,
            output=self.output,
            custom_rules=custom_rules_builder
        )

        self.criteria_dict = {c.name: c for c in self.criteria}

    def avaliar(
        self,
        clareza_val: float,
        dominio_val: float,
        ritmo_val: float,
        materiais_val: float,
        engajamento_val: float,
        organizacao_val: float
    ) -> Dict:
        inputs = {
            'clareza': clareza_val,
            'dominio': dominio_val,
            'ritmo': ritmo_val,
            'materiais': materiais_val,
            'engajamento': engajamento_val,
            'organizacao': organizacao_val
        }

        result = self.controller.evaluate(inputs)

        feedback = self._gerar_feedback(inputs, result['score'])

        return {
            'nota': result['score'],
            'classificacao': result['classification'],
            'feedback': feedback,
            'raw_score': result['raw_score']
        }

    def avaliar_dict(self, inputs: Dict[str, float]) -> Dict:
        result = self.controller.evaluate(inputs)
        feedback = self._gerar_feedback(inputs, result['score'])

        return {
            'nota': result['score'],
            'classificacao': result['classification'],
            'feedback': feedback
        }

    def _gerar_feedback(self, inputs: Dict[str, float], nota: float) -> str:
        sugestoes = []

        if inputs.get('clareza', 10) < 5:
            sugestoes.append("• Organize melhor os tópicos e use exemplos práticos")

        if inputs.get('dominio', 10) < 5:
            sugestoes.append("• Estude mais o conteúdo e prepare respostas para perguntas")

        ritmo = inputs.get('ritmo', 5)
        if ritmo < 4:
            sugestoes.append("• Acelere um pouco o ritmo da fala")
        elif ritmo > 7:
            sugestoes.append("• Diminua o ritmo e faça pausas")

        if inputs.get('materiais', 10) < 5:
            sugestoes.append("• Melhore os slides com mais recursos visuais")

        if inputs.get('engajamento', 10) < 5:
            sugestoes.append("• Faça mais contato visual e interaja com a plateia")

        if inputs.get('organizacao', 10) < 5:
            sugestoes.append("• Estruture melhor com introdução, desenvolvimento e conclusão")

        if not sugestoes:
            sugestoes.append("• Excelente! Continue assim!")

        return "\n".join(sugestoes)

    def visualizar_pertinencias(self):
        n_criteria = len(self.criteria)
        n_rows = (n_criteria + 2) // 2  

        fig, axes = plt.subplots(n_rows, 2, figsize=(15, 4 * n_rows))
        axes = axes.flatten() if n_rows > 1 else [axes]

        fig.suptitle(
            f'Funções de Pertinência ({self.function_type.title()}) - Alta Resolução ({self.resolution} pontos)',
            fontsize=16, fontweight='bold'
        )

        for idx, criterion in enumerate(self.criteria):
            criterion.variable.view(ax=axes[idx])
            axes[idx].set_title(f'{criterion.name.title()} (peso: {criterion.weight})')

        self.output.variable.view(ax=axes[len(self.criteria)])
        axes[len(self.criteria)].set_title('Avaliação Final')

        for idx in range(len(self.criteria) + 1, len(axes)):
            fig.delaxes(axes[idx])

        plt.tight_layout()
        return fig

    def get_info(self) -> Dict:
        return {
            'resolution': self.resolution,
            'function_type': self.function_type,
            'criteria': [c.get_info() for c in self.criteria],
            'available_functions': MembershipFunctionFactory.available_types(),
            'total_rules': len(self.controller.rules)
        }

    def add_criterion(self, criterion: FuzzyCriterion):
        self.criteria.append(criterion)
        self.criteria_dict[criterion.name] = criterion
        print(f"⚠️ Critério '{criterion.name}' adicionado. Recrie o controlador para usar.")


if __name__ == "__main__":
    print("="*70)
    print("SISTEMA FUZZY V2.0 - ARQUITETURA MODULAR")
    print("="*70)

    print("\n1️⃣ Testando com funções GAUSSIANAS (padrão)...")
    sistema_gauss = AvaliacaoApresentacaoFuzzyV2(
        resolution=1001,
        function_type='gaussian'
    )

    resultado = sistema_gauss.avaliar(9.5, 9.5, 5.0, 9.0, 9.5, 9.5)
    print(f"   Nota: {resultado['nota']}/10 ({resultado['classificacao']})")
    print(f"   Raw Score: {resultado['raw_score']:.4f}")

    print("\n2️⃣ Testando com funções TRIANGULARES...")
    sistema_tri = AvaliacaoApresentacaoFuzzyV2(
        resolution=1001,
        function_type='triangular'
    )

    resultado = sistema_tri.avaliar(9.5, 9.5, 5.0, 9.0, 9.5, 9.5)
    print(f"   Nota: {resultado['nota']}/10 ({resultado['classificacao']})")

    print("\n3️⃣ Testando com valores DECIMAIS PRECISOS...")
    resultado = sistema_gauss.avaliar(7.34, 8.12, 5.89, 6.77, 8.45, 7.91)
    print(f"   Nota: {resultado['nota']}/10 ({resultado['classificacao']})")
    print(f"   Precisão mantida com {sistema_gauss.resolution} pontos no universo")

    print("\n4️⃣ Informações do Sistema:")
    info = sistema_gauss.get_info()
    print(f"   Resolução: {info['resolution']} pontos")
    print(f"   Tipo de função: {info['function_type']}")
    print(f"   Total de regras: {info['total_rules']}")
    print(f"   Funções disponíveis: {', '.join(info['available_functions'])}")

    print("\n" + "="*70)
    print("✅ TODOS OS TESTES CONCLUÍDOS!")
    print("="*70)
