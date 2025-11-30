"""
Controlador Fuzzy Modular
Orquestra o sistema fuzzy completo com regras configuráveis
"""

from typing import List, Dict, Callable
from skfuzzy import control as ctrl
from .criteria_factory import FuzzyCriterion, OutputVariable


class FuzzyRuleBuilder:
    """Construtor de regras fuzzy com compensação e pesos"""

    @staticmethod
    def create_excellence_rules(criteria: Dict[str, FuzzyCriterion], output: OutputVariable) -> List[ctrl.Rule]:
        """Regras para excelência com compensação"""
        rules = []

        # Regra 1: Perfeição total
        rules.append(ctrl.Rule(
            criteria['clareza'].variable['alta'] &
            criteria['dominio'].variable['forte'] &
            criteria['engajamento'].variable['alto'] &
            criteria['organizacao'].variable['excelente'],
            output.variable['excelente']
        ))

        # Regra 2: Organização compensa materiais
        rules.append(ctrl.Rule(
            criteria['clareza'].variable['alta'] &
            criteria['dominio'].variable['forte'] &
            criteria['organizacao'].variable['excelente'],
            output.variable['excelente']
        ))

        # Regra 3: Domínio e clareza fortes
        rules.append(ctrl.Rule(
            criteria['clareza'].variable['alta'] &
            criteria['dominio'].variable['forte'] &
            criteria['engajamento'].variable['alto'],
            output.variable['excelente']
        ))

        return rules

    @staticmethod
    def create_good_rules(criteria: Dict[str, FuzzyCriterion], output: OutputVariable) -> List[ctrl.Rule]:
        """Regras para bom desempenho"""
        rules = []

        # Regra: Maioria média/alta
        rules.append(ctrl.Rule(
            criteria['clareza'].variable['media'] &
            criteria['dominio'].variable['medio'] &
            criteria['engajamento'].variable['medio'],
            output.variable['bom']
        ))

        # Regra: Bons materiais compensam
        rules.append(ctrl.Rule(
            criteria['materiais'].variable['bons'] &
            criteria['clareza'].variable['media'] &
            criteria['dominio'].variable['medio'],
            output.variable['bom']
        ))

        return rules

    @staticmethod
    def create_poor_rules(criteria: Dict[str, FuzzyCriterion], output: OutputVariable) -> List[ctrl.Rule]:
        """Regras para desempenho fraco"""
        rules = []

        # Regra: Clareza e domínio fracos
        rules.append(ctrl.Rule(
            criteria['clareza'].variable['baixa'] &
            criteria['dominio'].variable['fraco'],
            output.variable['precisa_melhorar']
        ))

        # Regra: Desorganização prejudica
        rules.append(ctrl.Rule(
            criteria['organizacao'].variable['desorganizada'] &
            criteria['clareza'].variable['baixa'],
            output.variable['precisa_melhorar']
        ))

        return rules


class FuzzyController:
    """Controlador principal do sistema fuzzy"""

    def __init__(
        self,
        criteria: List[FuzzyCriterion],
        output: OutputVariable,
        custom_rules: Callable = None
    ):
        """
        Inicializa o controlador

        Args:
            criteria: Lista de critérios de entrada
            output: Variável de saída
            custom_rules: Função para criar regras customizadas
        """
        self.criteria_list = criteria
        self.criteria_dict = {c.name: c for c in criteria}
        self.output = output

        # Cria regras
        if custom_rules:
            self.rules = custom_rules(self.criteria_dict, output)
        else:
            self.rules = self._create_default_rules()

        # Cria sistema de controle
        self.control_system = ctrl.ControlSystem(self.rules)
        self.simulation = ctrl.ControlSystemSimulation(self.control_system)

    def _create_default_rules(self) -> List[ctrl.Rule]:
        """Cria conjunto completo de regras padrão"""
        builder = FuzzyRuleBuilder()
        rules = []

        rules.extend(builder.create_excellence_rules(self.criteria_dict, self.output))
        rules.extend(builder.create_good_rules(self.criteria_dict, self.output))
        rules.extend(builder.create_poor_rules(self.criteria_dict, self.output))

        # Adiciona regras adicionais para garantir que TODOS os critérios sejam usados
        rules.extend(self._create_comprehensive_rules())

        return rules

    def _create_comprehensive_rules(self) -> List[ctrl.Rule]:
        """Cria regras abrangentes usando TODOS os critérios"""
        rules = []
        c = self.criteria_dict
        o = self.output.variable

        # Regras de excelência
        if all(k in c for k in ['clareza', 'dominio', 'ritmo', 'materiais', 'engajamento', 'organizacao']):
            # Perfeição total - TODOS altos
            rules.append(ctrl.Rule(
                c['clareza'].variable['alta'] &
                c['dominio'].variable['forte'] &
                c['ritmo'].variable['adequado'] &
                c['materiais'].variable['bons'] &
                c['engajamento'].variable['alto'] &
                c['organizacao'].variable['excelente'],
                o['excelente']
            ))

            # Excelente mesmo sem materiais perfeitos
            rules.append(ctrl.Rule(
                c['clareza'].variable['alta'] &
                c['dominio'].variable['forte'] &
                c['ritmo'].variable['adequado'] &
                c['engajamento'].variable['alto'] &
                c['organizacao'].variable['excelente'],
                o['excelente']
            ))

            # Muito bom - maioria alta
            rules.append(ctrl.Rule(
                c['clareza'].variable['alta'] &
                c['dominio'].variable['forte'] &
                c['engajamento'].variable['alto'] &
                c['organizacao'].variable['estruturada'],
                o['muito_bom']
            ))

            # Muito bom - compensação por ritmo adequado
            rules.append(ctrl.Rule(
                c['clareza'].variable['alta'] &
                c['dominio'].variable['forte'] &
                c['ritmo'].variable['adequado'] &
                c['materiais'].variable['aceitaveis'],
                o['muito_bom']
            ))

            # Bom - desempenho médio geral
            rules.append(ctrl.Rule(
                c['clareza'].variable['media'] &
                c['dominio'].variable['medio'] &
                c['ritmo'].variable['adequado'] &
                c['engajamento'].variable['medio'],
                o['bom']
            ))

            # Aceitável - base
            rules.append(ctrl.Rule(
                c['clareza'].variable['media'] &
                c['dominio'].variable['medio'] &
                c['materiais'].variable['aceitaveis'],
                o['aceitavel']
            ))

            # Precisa melhorar - ritmo ruim prejudica
            rules.append(ctrl.Rule(
                c['clareza'].variable['baixa'] &
                c['dominio'].variable['fraco'] &
                c['ritmo'].variable['devagar'],
                o['precisa_melhorar']
            ))

            # Precisa melhorar - materiais ruins e desorganização
            rules.append(ctrl.Rule(
                c['materiais'].variable['ruins'] &
                c['organizacao'].variable['desorganizada'] &
                c['engajamento'].variable['baixo'],
                o['precisa_melhorar']
            ))

        return rules

    def evaluate(self, inputs: Dict[str, float]) -> Dict:
        """
        Avalia entradas e retorna resultado

        Args:
            inputs: Dicionário {criterio: valor}

        Returns:
            Dict com 'score' e 'classification'
        """
        # Validação
        for name, value in inputs.items():
            if name not in self.criteria_dict:
                raise ValueError(f"Critério '{name}' não reconhecido")
            if not self.criteria_dict[name].validate_value(value):
                raise ValueError(f"Valor {value} fora do range para '{name}'")

        # Define entradas
        for name, value in inputs.items():
            self.simulation.input[name] = value

        # Computa
        self.simulation.compute()

        # Resultado
        score = self.simulation.output['avaliacao']

        return {
            'score': round(score, 2),
            'raw_score': score,
            'classification': self._classify(score)
        }

    def _classify(self, score: float) -> str:
        """Classifica nota em categoria linguística"""
        if score < 3:
            return "Precisa Melhorar"
        elif score < 5:
            return "Aceitável"
        elif score < 7:
            return "Bom"
        elif score < 8.5:
            return "Muito Bom"
        else:
            return "Excelente"
