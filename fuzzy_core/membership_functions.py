"""
Strategy Pattern para Funções de Pertinência
Permite configurar diferentes tipos de curvas fuzzy de forma modular
"""

from abc import ABC, abstractmethod
import numpy as np
import skfuzzy as fuzz
from typing import Dict, Tuple


class MembershipFunctionStrategy(ABC):
    """Classe abstrata para estratégias de funções de pertinência"""

    @abstractmethod
    def create_function(self, universe: np.ndarray, params: Dict) -> np.ndarray:
        """
        Cria uma função de pertinência

        Args:
            universe: Array com o universo de discurso
            params: Dicionário com parâmetros específicos da função

        Returns:
            Array com os valores de pertinência
        """
        pass

    @abstractmethod
    def get_default_params(self, position: str, universe_range: Tuple[float, float]) -> Dict:
        """
        Retorna parâmetros padrão para uma posição (baixo/medio/alto)

        Args:
            position: 'low', 'medium', 'high'
            universe_range: Tupla (min, max) do universo

        Returns:
            Dicionário com parâmetros padrão
        """
        pass


class TriangularMF(MembershipFunctionStrategy):
    """Funções de pertinência triangulares"""

    def create_function(self, universe: np.ndarray, params: Dict) -> np.ndarray:
        """
        Cria função triangular

        Params esperados:
            - a: ponto inicial
            - b: pico
            - c: ponto final
        """
        return fuzz.trimf(universe, [params['a'], params['b'], params['c']])

    def get_default_params(self, position: str, universe_range: Tuple[float, float]) -> Dict:
        min_val, max_val = universe_range
        range_size = max_val - min_val

        if position == 'low':
            return {'a': min_val, 'b': min_val, 'c': min_val + range_size * 0.4}
        elif position == 'medium':
            return {'a': min_val + range_size * 0.2, 'b': min_val + range_size * 0.5,
                    'c': min_val + range_size * 0.8}
        elif position == 'high':
            return {'a': min_val + range_size * 0.6, 'b': max_val, 'c': max_val}
        else:
            raise ValueError(f"Position '{position}' não reconhecida")


class TrapezoidalMF(MembershipFunctionStrategy):
    """Funções de pertinência trapezoidais"""

    def create_function(self, universe: np.ndarray, params: Dict) -> np.ndarray:
        """
        Cria função trapezoidal

        Params esperados:
            - a: ponto inicial
            - b: início do plateau
            - c: fim do plateau
            - d: ponto final
        """
        return fuzz.trapmf(universe, [params['a'], params['b'], params['c'], params['d']])

    def get_default_params(self, position: str, universe_range: Tuple[float, float]) -> Dict:
        min_val, max_val = universe_range
        range_size = max_val - min_val

        if position == 'low':
            return {'a': min_val, 'b': min_val,
                    'c': min_val + range_size * 0.3, 'd': min_val + range_size * 0.4}
        elif position == 'medium':
            return {'a': min_val + range_size * 0.3, 'b': min_val + range_size * 0.4,
                    'c': min_val + range_size * 0.6, 'd': min_val + range_size * 0.7}
        elif position == 'high':
            return {'a': min_val + range_size * 0.6, 'b': min_val + range_size * 0.7,
                    'c': max_val, 'd': max_val}
        else:
            raise ValueError(f"Position '{position}' não reconhecida")


class GaussianMF(MembershipFunctionStrategy):
    """Funções de pertinência gaussianas (curvas suaves)"""

    def create_function(self, universe: np.ndarray, params: Dict) -> np.ndarray:
        """
        Cria função gaussiana

        Params esperados:
            - mean: centro da gaussiana
            - sigma: desvio padrão (largura)
        """
        return fuzz.gaussmf(universe, params['mean'], params['sigma'])

    def get_default_params(self, position: str, universe_range: Tuple[float, float]) -> Dict:
        min_val, max_val = universe_range
        range_size = max_val - min_val

        # Sigma adaptativo baseado no tamanho do universo
        sigma_low = range_size * 0.15
        sigma_medium = range_size * 0.15
        sigma_high = range_size * 0.10

        if position == 'low':
            return {'mean': min_val, 'sigma': sigma_low}
        elif position == 'medium':
            return {'mean': min_val + range_size * 0.5, 'sigma': sigma_medium}
        elif position == 'high':
            return {'mean': max_val, 'sigma': sigma_high}
        else:
            raise ValueError(f"Position '{position}' não reconhecida")


class GeneralizedBellMF(MembershipFunctionStrategy):
    """Funções de pertinência em sino generalizado"""

    def create_function(self, universe: np.ndarray, params: Dict) -> np.ndarray:
        """
        Cria função sino generalizado

        Params esperados:
            - a: largura
            - b: inclinação das bordas
            - c: centro
        """
        return fuzz.gbellmf(universe, params['a'], params['b'], params['c'])

    def get_default_params(self, position: str, universe_range: Tuple[float, float]) -> Dict:
        min_val, max_val = universe_range
        range_size = max_val - min_val

        width = range_size * 0.2
        slope = 2.0

        if position == 'low':
            return {'a': width, 'b': slope, 'c': min_val}
        elif position == 'medium':
            return {'a': width, 'b': slope, 'c': min_val + range_size * 0.5}
        elif position == 'high':
            return {'a': width * 0.8, 'b': slope, 'c': max_val}
        else:
            raise ValueError(f"Position '{position}' não reconhecida")


class SigmoidalMF(MembershipFunctionStrategy):
    """Funções de pertinência sigmoidais"""

    def create_function(self, universe: np.ndarray, params: Dict) -> np.ndarray:
        """
        Cria função sigmoidal

        Params esperados:
            - a: inclinação
            - c: ponto de inflexão
        """
        return fuzz.sigmf(universe, params['c'], params['a'])

    def get_default_params(self, position: str, universe_range: Tuple[float, float]) -> Dict:
        min_val, max_val = universe_range
        range_size = max_val - min_val

        # Inclinação adaptativa
        slope = 1.0 / (range_size * 0.1)

        if position == 'low':
            # Sigmoide descendente
            return {'a': -slope, 'c': min_val + range_size * 0.3}
        elif position == 'medium':
            # Combinação de duas sigmoides (aproxima trapezoidal)
            # Para medium, retorna gaussiana como fallback
            return GaussianMF().get_default_params('medium', universe_range)
        elif position == 'high':
            # Sigmoide ascendente
            return {'a': slope, 'c': min_val + range_size * 0.7}
        else:
            raise ValueError(f"Position '{position}' não reconhecida")


# Factory para criar estratégias
class MembershipFunctionFactory:
    """Factory para criar estratégias de funções de pertinência"""

    _strategies = {
        'triangular': TriangularMF,
        'trapezoidal': TrapezoidalMF,
        'gaussian': GaussianMF,
        'bell': GeneralizedBellMF,
        'sigmoidal': SigmoidalMF
    }

    @classmethod
    def create(cls, function_type: str) -> MembershipFunctionStrategy:
        """
        Cria uma estratégia de função de pertinência

        Args:
            function_type: Tipo da função ('triangular', 'gaussian', etc.)

        Returns:
            Instância da estratégia
        """
        strategy_class = cls._strategies.get(function_type.lower())
        if strategy_class is None:
            available = ', '.join(cls._strategies.keys())
            raise ValueError(f"Tipo '{function_type}' inválido. Disponíveis: {available}")
        return strategy_class()

    @classmethod
    def available_types(cls) -> list:
        """Retorna lista de tipos disponíveis"""
        return list(cls._strategies.keys())
