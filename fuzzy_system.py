"""
Sistema de Avaliação de Apresentações usando Lógica Fuzzy
Autor: Sistema Fuzzy
Data: 2025-11-29

VERSÃO MELHORADA - Agora usa arquitetura modular!
Para usar a versão avançada com configurações personalizadas, veja fuzzy_system_v2.py
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Tenta importar a nova arquitetura modular
try:
    from fuzzy_system_v2 import AvaliacaoApresentacaoFuzzyV2
    MODULAR_AVAILABLE = True
except ImportError:
    MODULAR_AVAILABLE = False


class AvaliacaoApresentacaoFuzzy:
    """
    Sistema de inferência fuzzy para avaliar apresentações orais
    baseado em múltiplos critérios qualitativos.
    """

    def __init__(self):
        """Inicializa o sistema fuzzy com variáveis e regras"""
        self._criar_variaveis()
        self._criar_funcoes_pertinencia()
        self._criar_regras()
        self._criar_sistema_controle()

    def _criar_variaveis(self):
        """Define as variáveis de entrada e saída do sistema"""
        # Variáveis de entrada (universo de 0 a 10 com precisão de 0.01)
        self.clareza = ctrl.Antecedent(np.arange(0, 10.1, 0.01), 'clareza')
        self.dominio = ctrl.Antecedent(np.arange(0, 10.1, 0.01), 'dominio')
        self.ritmo = ctrl.Antecedent(np.arange(0, 10.1, 0.01), 'ritmo')
        self.materiais = ctrl.Antecedent(np.arange(0, 10.1, 0.01), 'materiais')
        self.engajamento = ctrl.Antecedent(np.arange(0, 10.1, 0.01), 'engajamento')
        self.organizacao = ctrl.Antecedent(np.arange(0, 10.1, 0.01), 'organizacao')

        # Variável de saída
        self.avaliacao = ctrl.Consequent(np.arange(0, 10.1, 0.01), 'avaliacao')

    def _criar_funcoes_pertinencia(self):
        """Define as funções de pertinência para cada variável usando Gaussianas"""

        # CLAREZA: Baixa, Média, Alta (Gaussianas)
        self.clareza['baixa'] = fuzz.gaussmf(self.clareza.universe, 0, 1.5)
        self.clareza['media'] = fuzz.gaussmf(self.clareza.universe, 5, 1.5)
        self.clareza['alta'] = fuzz.gaussmf(self.clareza.universe, 9.0, 1.0)

        # DOMÍNIO: Fraco, Médio, Forte (Gaussianas)
        self.dominio['fraco'] = fuzz.gaussmf(self.dominio.universe, 0, 1.5)
        self.dominio['medio'] = fuzz.gaussmf(self.dominio.universe, 5, 1.5)
        self.dominio['forte'] = fuzz.gaussmf(self.dominio.universe, 9.0, 1.0)

        # RITMO: Devagar, Adequado, Rápido (Gaussianas)
        self.ritmo['devagar'] = fuzz.gaussmf(self.ritmo.universe, 0, 1.5)
        self.ritmo['adequado'] = fuzz.gaussmf(self.ritmo.universe, 5, 1.2)
        self.ritmo['rapido'] = fuzz.gaussmf(self.ritmo.universe, 9.0, 1.5)

        # MATERIAIS: Ruins, Aceitáveis, Bons (Gaussianas)
        self.materiais['ruins'] = fuzz.gaussmf(self.materiais.universe, 0, 1.5)
        self.materiais['aceitaveis'] = fuzz.gaussmf(self.materiais.universe, 5, 1.5)
        self.materiais['bons'] = fuzz.gaussmf(self.materiais.universe, 9.0, 1.0)

        # ENGAJAMENTO: Baixo, Médio, Alto (Gaussianas)
        self.engajamento['baixo'] = fuzz.gaussmf(self.engajamento.universe, 0, 1.5)
        self.engajamento['medio'] = fuzz.gaussmf(self.engajamento.universe, 5, 1.5)
        self.engajamento['alto'] = fuzz.gaussmf(self.engajamento.universe, 9.0, 1.0)

        # ORGANIZAÇÃO: Desorganizada, Estruturada, Excelente (Gaussianas)
        self.organizacao['desorganizada'] = fuzz.gaussmf(self.organizacao.universe, 0, 1.5)
        self.organizacao['estruturada'] = fuzz.gaussmf(self.organizacao.universe, 5, 1.5)
        self.organizacao['excelente'] = fuzz.gaussmf(self.organizacao.universe, 9.5, 0.8)

        # AVALIAÇÃO FINAL: 5 níveis (Gaussianas - ajustado para permitir nota 10)
        self.avaliacao['precisa_melhorar'] = fuzz.gaussmf(self.avaliacao.universe, 0, 1)
        self.avaliacao['aceitavel'] = fuzz.gaussmf(self.avaliacao.universe, 4, 1)
        self.avaliacao['bom'] = fuzz.gaussmf(self.avaliacao.universe, 6.5, 1)
        self.avaliacao['muito_bom'] = fuzz.gaussmf(self.avaliacao.universe, 8.0, 0.8)
        self.avaliacao['excelente'] = fuzz.gaussmf(self.avaliacao.universe, 10.0, 0.5)

    def _criar_regras(self):
        """
        Define a base de regras fuzzy (mínimo 10 regras)
        Formato: IF antecedente THEN consequente
        """

        # REGRA 1: Excelência total
        regra1 = ctrl.Rule(
            self.clareza['alta'] & self.dominio['forte'] & self.engajamento['alto'],
            self.avaliacao['excelente']
        )

        # REGRA 2: Muito bom com pequenas falhas
        regra2 = ctrl.Rule(
            self.clareza['alta'] & self.dominio['forte'] & self.materiais['bons'],
            self.avaliacao['muito_bom']
        )

        # REGRA 3: Bom desempenho geral
        regra3 = ctrl.Rule(
            self.clareza['media'] & self.dominio['medio'] & self.engajamento['medio'],
            self.avaliacao['bom']
        )

        # REGRA 4: Clareza e domínio compensam materiais ruins
        regra4 = ctrl.Rule(
            self.clareza['alta'] & self.dominio['forte'] & self.materiais['ruins'],
            self.avaliacao['bom']
        )

        # REGRA 5: Ritmo inadequado prejudica avaliação
        regra5 = ctrl.Rule(
            (self.ritmo['devagar'] | self.ritmo['rapido']) & self.engajamento['baixo'],
            self.avaliacao['aceitavel']
        )

        # REGRA 6: Falta de clareza é crítica
        regra6 = ctrl.Rule(
            self.clareza['baixa'] & self.dominio['fraco'],
            self.avaliacao['precisa_melhorar']
        )

        # REGRA 7: Materiais excelentes ajudam
        regra7 = ctrl.Rule(
            self.materiais['bons'] & self.clareza['media'] & self.dominio['medio'],
            self.avaliacao['bom']
        )

        # REGRA 8: Engajamento alto compensa outros fatores
        regra8 = ctrl.Rule(
            self.engajamento['alto'] & self.ritmo['adequado'],
            self.avaliacao['muito_bom']
        )

        # REGRA 9: Desempenho aceitável
        regra9 = ctrl.Rule(
            self.clareza['media'] & self.dominio['medio'] & self.materiais['aceitaveis'],
            self.avaliacao['aceitavel']
        )

        # REGRA 10: Todos os fatores baixos
        regra10 = ctrl.Rule(
            self.clareza['baixa'] & self.dominio['fraco'] & self.engajamento['baixo'],
            self.avaliacao['precisa_melhorar']
        )

        # REGRA 11: Bom domínio com clareza média
        regra11 = ctrl.Rule(
            self.dominio['forte'] & self.clareza['media'] & self.ritmo['adequado'],
            self.avaliacao['bom']
        )

        # REGRA 12: Ritmo adequado é importante
        regra12 = ctrl.Rule(
            self.ritmo['adequado'] & self.clareza['alta'] & self.materiais['bons'],
            self.avaliacao['muito_bom']
        )

        # REGRA 13: Materiais ruins prejudicam muito
        regra13 = ctrl.Rule(
            self.materiais['ruins'] & self.engajamento['baixo'] & self.clareza['baixa'],
            self.avaliacao['precisa_melhorar']
        )

        # REGRA 14: Apresentação mediana
        regra14 = ctrl.Rule(
            self.clareza['media'] & self.ritmo['adequado'] & self.engajamento['medio'],
            self.avaliacao['aceitavel']
        )

        # REGRA 15: Alto engajamento com bom domínio
        regra15 = ctrl.Rule(
            self.engajamento['alto'] & self.dominio['forte'] & self.materiais['aceitaveis'],
            self.avaliacao['muito_bom']
        )

        # REGRA 16: Perfeição total - todos os critérios altos (REFORÇADA)
        regra16 = ctrl.Rule(
            self.clareza['alta'] & self.dominio['forte'] & self.engajamento['alto'] &
            self.materiais['bons'] & self.ritmo['adequado'] & self.organizacao['excelente'],
            self.avaliacao['excelente']
        )

        # REGRA 17: Excelência mesmo sem materiais perfeitos (REFORÇADA)
        regra17 = ctrl.Rule(
            self.clareza['alta'] & self.dominio['forte'] & self.engajamento['alto'] &
            self.ritmo['adequado'] & self.organizacao['excelente'],
            self.avaliacao['excelente']
        )

        # REGRA 18: Compensação - organização excelente compensa materiais aceitáveis
        regra18 = ctrl.Rule(
            self.clareza['alta'] & self.dominio['forte'] & self.organizacao['excelente'] &
            self.materiais['aceitaveis'],
            self.avaliacao['excelente']
        )

        # REGRA 19: Compensação - organização excelente com ritmo adequado
        regra19 = ctrl.Rule(
            self.clareza['alta'] & self.dominio['forte'] & self.organizacao['excelente'] &
            self.ritmo['adequado'],
            self.avaliacao['excelente']
        )

        # REGRA 20: Organização estruturada com bons critérios
        regra20 = ctrl.Rule(
            self.clareza['alta'] & self.dominio['forte'] & self.organizacao['estruturada'] &
            self.engajamento['alto'],
            self.avaliacao['muito_bom']
        )

        # REGRA 21: Organização desorganizada prejudica
        regra21 = ctrl.Rule(
            self.organizacao['desorganizada'] & self.clareza['baixa'],
            self.avaliacao['precisa_melhorar']
        )

        # REGRA 22: Organização excelente sozinha não garante excelência
        regra22 = ctrl.Rule(
            self.organizacao['excelente'] & self.clareza['media'] & self.dominio['medio'],
            self.avaliacao['bom']
        )

        # Armazena todas as regras
        self.regras = [
            regra1, regra2, regra3, regra4, regra5,
            regra6, regra7, regra8, regra9, regra10,
            regra11, regra12, regra13, regra14, regra15,
            regra16, regra17, regra18, regra19, regra20,
            regra21, regra22
        ]

    def _criar_sistema_controle(self):
        """Cria o sistema de controle fuzzy com as regras definidas"""
        self.sistema_ctrl = ctrl.ControlSystem(self.regras)
        self.simulacao = ctrl.ControlSystemSimulation(self.sistema_ctrl)

    def avaliar(self, clareza_val, dominio_val, ritmo_val, materiais_val, engajamento_val, organizacao_val):
        """
        Avalia uma apresentação com base nos valores de entrada.

        Parâmetros:
            clareza_val (float): Clareza da apresentação (0-10)
            dominio_val (float): Domínio do conteúdo (0-10)
            ritmo_val (float): Ritmo da fala (0-10)
            materiais_val (float): Qualidade dos materiais (0-10)
            engajamento_val (float): Engajamento com a plateia (0-10)
            organizacao_val (float): Organização da apresentação (0-10)

        Retorna:
            dict: Dicionário com nota numérica e classificação linguística
        """
        # Define os valores de entrada
        self.simulacao.input['clareza'] = clareza_val
        self.simulacao.input['dominio'] = dominio_val
        self.simulacao.input['ritmo'] = ritmo_val
        self.simulacao.input['materiais'] = materiais_val
        self.simulacao.input['engajamento'] = engajamento_val
        self.simulacao.input['organizacao'] = organizacao_val

        # Executa a inferência
        self.simulacao.compute()

        # Obtém o resultado
        nota = self.simulacao.output['avaliacao']
        classificacao = self._obter_classificacao(nota)
        feedback = self._gerar_feedback(clareza_val, dominio_val, ritmo_val,
                                       materiais_val, engajamento_val, organizacao_val, nota)

        return {
            'nota': round(nota, 2),
            'classificacao': classificacao,
            'feedback': feedback
        }

    def _obter_classificacao(self, nota):
        """Converte a nota numérica em classificação linguística"""
        if nota < 3:
            return "Precisa Melhorar"
        elif nota < 5:
            return "Aceitável"
        elif nota < 7:
            return "Bom"
        elif nota < 8.5:
            return "Muito Bom"
        else:
            return "Excelente"

    def _gerar_feedback(self, clareza, dominio, ritmo, materiais, engajamento, organizacao, nota):
        """Gera feedback construtivo baseado nos valores de entrada"""
        sugestoes = []

        if clareza < 5:
            sugestoes.append("• Organize melhor os tópicos e use exemplos práticos para melhorar a clareza")

        if dominio < 5:
            sugestoes.append("• Estude mais o conteúdo e prepare respostas para possíveis perguntas")

        if ritmo < 4 or ritmo > 7:
            if ritmo < 4:
                sugestoes.append("• Pratique para acelerar um pouco o ritmo da fala")
            else:
                sugestoes.append("• Diminua o ritmo e faça pausas para facilitar o acompanhamento")

        if materiais < 5:
            sugestoes.append("• Melhore os slides com mais recursos visuais e menos texto")

        if engajamento < 5:
            sugestoes.append("• Faça mais contato visual e interaja com a plateia através de perguntas")

        if organizacao < 5:
            sugestoes.append("• Estruture melhor a apresentação com introdução, desenvolvimento e conclusão claros")
            sugestoes.append("• Use roteiros e marcadores para manter a sequência lógica do conteúdo")

        if not sugestoes:
            sugestoes.append("• Continue assim! Sua apresentação está excelente!")

        return "\n".join(sugestoes)

    def visualizar_pertinencias(self):
        """Gera gráficos das funções de pertinência de todas as variáveis"""
        fig, axes = plt.subplots(4, 2, figsize=(15, 16))
        fig.suptitle('Funções de Pertinência Gaussianas - Sistema de Avaliação de Apresentações',
                     fontsize=16, fontweight='bold')

        # Clareza
        self.clareza.view(ax=axes[0, 0])
        axes[0, 0].set_title('Clareza')

        # Domínio
        self.dominio.view(ax=axes[0, 1])
        axes[0, 1].set_title('Domínio do Conteúdo')

        # Ritmo
        self.ritmo.view(ax=axes[1, 0])
        axes[1, 0].set_title('Ritmo da Fala')

        # Materiais
        self.materiais.view(ax=axes[1, 1])
        axes[1, 1].set_title('Qualidade dos Materiais')

        # Engajamento
        self.engajamento.view(ax=axes[2, 0])
        axes[2, 0].set_title('Engajamento')

        # Organização (NOVA)
        self.organizacao.view(ax=axes[2, 1])
        axes[2, 1].set_title('Organização')

        # Avaliação Final
        self.avaliacao.view(ax=axes[3, 0])
        axes[3, 0].set_title('Avaliação Final')

        # Remove o subplot vazio
        fig.delaxes(axes[3, 1])

        plt.tight_layout()
        return fig


# Exemplo de uso
if __name__ == "__main__":
    # Cria o sistema
    sistema = AvaliacaoApresentacaoFuzzy()

    # Exemplo de avaliação
    resultado = sistema.avaliar(
        clareza_val=7.5,
        dominio_val=8.0,
        ritmo_val=6.0,
        materiais_val=7.0,
        engajamento_val=8.5,
        organizacao_val=8.0
    )

    print("=" * 60)
    print("RESULTADO DA AVALIAÇÃO")
    print("=" * 60)
    print(f"Nota: {resultado['nota']}/10")
    print(f"Classificação: {resultado['classificacao']}")
    print(f"\nFeedback:")
    print(resultado['feedback'])
    print("=" * 60)
