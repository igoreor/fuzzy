"""
Factory Pattern para Configuração de Critérios Fuzzy
Permite criar critérios de forma modular e configurável
"""

import numpy as np
from typing import Dict, Tuple, List, Optional
from skfuzzy import control as ctrl
from .membership_functions import MembershipFunctionFactory, MembershipFunctionStrategy


class FuzzyCriterion:
    """Representa um critério fuzzy com suas funções de pertinência"""

    def __init__(
        self,
        name: str,
        universe_range: Tuple[float, float],
        resolution: int = 1001,
        function_type: str = 'gaussian',
        terms: Optional[Dict[str, str]] = None,
        custom_params: Optional[Dict[str, Dict]] = None,
        weight: float = 1.0,
        description: str = ""
    ):
        """
        Inicializa um critério fuzzy

        Args:
            name: Nome do critério
            universe_range: Tupla (min, max) do universo de discurso
            resolution: Número de pontos no universo (maior = mais preciso)
            function_type: Tipo de função de pertinência
            terms: Dicionário mapeando termos linguísticos para posições
                  Ex: {'baixa': 'low', 'media': 'medium', 'alta': 'high'}
            custom_params: Parâmetros customizados para cada termo
            weight: Peso relativo do critério (0-1)
            description: Descrição do critério
        """
        self.name = name
        self.universe_range = universe_range
        self.resolution = resolution
        self.function_type = function_type
        self.weight = weight
        self.description = description

        # Termos padrão se não especificado
        if terms is None:
            terms = {
                'baixo': 'low',
                'medio': 'medium',
                'alto': 'high'
            }
        self.terms = terms

        # Cria o universo de discurso com alta resolução
        self.universe = np.linspace(
            universe_range[0],
            universe_range[1],
            resolution
        )

        # Cria a variável antecedente
        self.variable = ctrl.Antecedent(self.universe, name)

        # Cria estratégia de função de pertinência
        self.mf_strategy = MembershipFunctionFactory.create(function_type)

        # Cria as funções de pertinência
        self._create_membership_functions(custom_params or {})

    def _create_membership_functions(self, custom_params: Dict[str, Dict]):
        """Cria as funções de pertinência para cada termo linguístico"""
        for term_name, position in self.terms.items():
            if term_name in custom_params:
                # Usa parâmetros customizados
                params = custom_params[term_name]
            else:
                # Usa parâmetros padrão da estratégia
                params = self.mf_strategy.get_default_params(position, self.universe_range)

            # Cria a função de pertinência
            self.variable[term_name] = self.mf_strategy.create_function(
                self.universe,
                params
            )

    def get_variable(self) -> ctrl.Antecedent:
        """Retorna a variável antecedente"""
        return self.variable

    def validate_value(self, value: float) -> bool:
        """Valida se um valor está dentro do universo"""
        return self.universe_range[0] <= value <= self.universe_range[1]

    def get_info(self) -> Dict:
        """Retorna informações sobre o critério"""
        return {
            'name': self.name,
            'range': self.universe_range,
            'resolution': self.resolution,
            'function_type': self.function_type,
            'terms': list(self.terms.keys()),
            'weight': self.weight,
            'description': self.description
        }


class OutputVariable:
    """Representa a variável de saída do sistema fuzzy"""

    def __init__(
        self,
        name: str,
        universe_range: Tuple[float, float],
        resolution: int = 1001,
        function_type: str = 'gaussian',
        levels: Optional[List[Dict]] = None
    ):
        """
        Inicializa variável de saída

        Args:
            name: Nome da variável
            universe_range: Tupla (min, max) do universo
            resolution: Número de pontos
            function_type: Tipo de função de pertinência
            levels: Lista de níveis de saída
                   Ex: [{'name': 'baixo', 'position': 'low'},
                        {'name': 'medio', 'position': 'medium'}, ...]
        """
        self.name = name
        self.universe_range = universe_range
        self.resolution = resolution
        self.function_type = function_type

        # Níveis padrão se não especificado
        if levels is None:
            levels = [
                {'name': 'precisa_melhorar', 'position': 'low', 'center': 0.0},
                {'name': 'aceitavel', 'position': 'low-medium', 'center': 0.25},
                {'name': 'bom', 'position': 'medium', 'center': 0.50},
                {'name': 'muito_bom', 'position': 'medium-high', 'center': 0.75},
                {'name': 'excelente', 'position': 'high', 'center': 1.0}
            ]
        self.levels = levels

        # Cria o universo com alta resolução
        self.universe = np.linspace(
            universe_range[0],
            universe_range[1],
            resolution
        )

        # Cria a variável consequente
        self.variable = ctrl.Consequent(self.universe, name)

        # Cria estratégia de função de pertinência
        self.mf_strategy = MembershipFunctionFactory.create(function_type)

        # Cria as funções de pertinência
        self._create_output_functions()

    def _create_output_functions(self):
        """
        Cria funções de pertinência para saída
        CRÍTICO: Evita sobreposição excessiva que limita a nota máxima
        """
        min_val, max_val = self.universe_range
        range_size = max_val - min_val

        for level in self.levels:
            name = level['name']
            center_ratio = level.get('center', 0.5)
            center = min_val + range_size * center_ratio

            # Sigma mais estreito para evitar sobreposição excessiva
            # Isso é CRUCIAL para permitir notas até 10
            sigma = range_size * 0.08  # Reduzido de 0.15 para 0.08

            if self.function_type == 'gaussian':
                # Gaussiana centrada
                params = {'mean': center, 'sigma': sigma}
                self.variable[name] = self.mf_strategy.create_function(
                    self.universe,
                    params
                )
            elif self.function_type == 'triangular':
                # Triangular com menos sobreposição
                if center_ratio == 0.0:
                    params = {'a': min_val, 'b': min_val, 'c': min_val + range_size * 0.25}
                elif center_ratio == 1.0:
                    params = {'a': max_val - range_size * 0.15, 'b': max_val, 'c': max_val}
                else:
                    width = range_size * 0.2
                    params = {'a': center - width, 'b': center, 'c': center + width}

                self.variable[name] = self.mf_strategy.create_function(
                    self.universe,
                    params
                )
            else:
                # Para outros tipos, usa a estratégia padrão
                position = level.get('position', 'medium')
                params = self.mf_strategy.get_default_params(position, self.universe_range)
                self.variable[name] = self.mf_strategy.create_function(
                    self.universe,
                    params
                )

    def get_variable(self) -> ctrl.Consequent:
        """Retorna a variável consequente"""
        return self.variable


class CriteriaFactory:
    """Factory para criar critérios pré-configurados"""

    @staticmethod
    def create_standard_input_criteria(
        resolution: int = 1001,
        function_type: str = 'gaussian'
    ) -> List[FuzzyCriterion]:
        """
        Cria os critérios padrão de entrada para avaliação de apresentações

        Args:
            resolution: Resolução do universo (padrão 1001 pontos)
            function_type: Tipo de função de pertinência

        Returns:
            Lista de critérios fuzzy
        """
        criteria = [
            FuzzyCriterion(
                name='clareza',
                universe_range=(0, 10),
                resolution=resolution,
                function_type=function_type,
                terms={'baixa': 'low', 'media': 'medium', 'alta': 'high'},
                weight=1.2,  # Maior peso - critério mais importante
                description='Clareza da explicação e organização das ideias'
            ),
            FuzzyCriterion(
                name='dominio',
                universe_range=(0, 10),
                resolution=resolution,
                function_type=function_type,
                terms={'fraco': 'low', 'medio': 'medium', 'forte': 'high'},
                weight=1.3,  # Maior peso - critério mais importante
                description='Domínio e conhecimento do conteúdo apresentado'
            ),
            FuzzyCriterion(
                name='ritmo',
                universe_range=(0, 10),
                resolution=resolution,
                function_type=function_type,
                terms={'devagar': 'low', 'adequado': 'medium', 'rapido': 'high'},
                weight=0.8,  # Menor peso - menos crítico
                description='Velocidade e fluidez da fala'
            ),
            FuzzyCriterion(
                name='materiais',
                universe_range=(0, 10),
                resolution=resolution,
                function_type=function_type,
                terms={'ruins': 'low', 'aceitaveis': 'medium', 'bons': 'high'},
                weight=0.9,
                description='Qualidade dos slides e recursos visuais'
            ),
            FuzzyCriterion(
                name='engajamento',
                universe_range=(0, 10),
                resolution=resolution,
                function_type=function_type,
                terms={'baixo': 'low', 'medio': 'medium', 'alto': 'high'},
                weight=1.1,
                description='Interação com a plateia e contato visual'
            ),
            FuzzyCriterion(
                name='organizacao',
                universe_range=(0, 10),
                resolution=resolution,
                function_type=function_type,
                terms={'desorganizada': 'low', 'estruturada': 'medium', 'excelente': 'high'},
                weight=1.15,  # Alto peso - critério importante
                description='Estrutura lógica e sequencial da apresentação'
            )
        ]

        return criteria

    @staticmethod
    def create_standard_output(
        resolution: int = 1001,
        function_type: str = 'gaussian'
    ) -> OutputVariable:
        """
        Cria a variável de saída padrão (nota de avaliação)

        Args:
            resolution: Resolução do universo
            function_type: Tipo de função de pertinência

        Returns:
            OutputVariable configurada
        """
        levels = [
            {'name': 'precisa_melhorar', 'center': 0.0, 'position': 'low'},
            {'name': 'aceitavel', 'center': 0.4, 'position': 'low-medium'},
            {'name': 'bom', 'center': 0.65, 'position': 'medium'},
            {'name': 'muito_bom', 'center': 0.82, 'position': 'medium-high'},
            {'name': 'excelente', 'center': 1.0, 'position': 'high'}
        ]

        return OutputVariable(
            name='avaliacao',
            universe_range=(0, 10),
            resolution=resolution,
            function_type=function_type,
            levels=levels
        )
