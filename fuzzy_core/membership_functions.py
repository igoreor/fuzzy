from abc import ABC, abstractmethod
import numpy as np
import skfuzzy as fuzz
from typing import Dict, Tuple


class MembershipFunctionStrategy(ABC):

    @abstractmethod
    def create_function(self, universe: np.ndarray, params: Dict) -> np.ndarray:
        """
        pass

    @abstractmethod
    def get_default_params(self, position: str, universe_range: Tuple[float, float]) -> Dict:
        """
        pass


class TriangularMF(MembershipFunctionStrategy):

    def create_function(self, universe: np.ndarray, params: Dict) -> np.ndarray:
        return fuzz.trimf(universe, [params['a'], params['b'], params['c']])

    def get_default_params(self, position: str, universe_range: Tuple[float, float]) -> Dict:
        min_val, max_val = universe_range
        range_size = max_val - min_val

        if position == 'low':
            return {'a': min_val, 'b': min_val, 'c': min_val + range_size * 0.35}
        elif position == 'low-medium':
            return {'a': min_val + range_size * 0.1, 'b': min_val + range_size * 0.25,
                    'c': min_val + range_size * 0.4}
        elif position == 'medium':
            return {'a': min_val + range_size * 0.3, 'b': min_val + range_size * 0.5,
                    'c': min_val + range_size * 0.7}
        elif position == 'medium-high':
            return {'a': min_val + range_size * 0.6, 'b': min_val + range_size * 0.75,
                    'c': min_val + range_size * 0.9}
        elif position == 'high':
            return {'a': min_val + range_size * 0.65, 'b': max_val, 'c': max_val}
        else:
            raise ValueError(f"Position '{position}' não reconhecida. Use: 'low', 'low-medium', 'medium', 'medium-high', 'high'")


class TrapezoidalMF(MembershipFunctionStrategy):

    def create_function(self, universe: np.ndarray, params: Dict) -> np.ndarray:
        return fuzz.trapmf(universe, [params['a'], params['b'], params['c'], params['d']])

    def get_default_params(self, position: str, universe_range: Tuple[float, float]) -> Dict:
        min_val, max_val = universe_range
        range_size = max_val - min_val

        if position == 'low':
            return {'a': min_val, 'b': min_val,
                    'c': min_val + range_size * 0.25, 'd': min_val + range_size * 0.35}
        elif position == 'low-medium':
            return {'a': min_val + range_size * 0.15, 'b': min_val + range_size * 0.2,
                    'c': min_val + range_size * 0.3, 'd': min_val + range_size * 0.4}
        elif position == 'medium':
            return {'a': min_val + range_size * 0.35, 'b': min_val + range_size * 0.45,
                    'c': min_val + range_size * 0.55, 'd': min_val + range_size * 0.65}
        elif position == 'medium-high':
            return {'a': min_val + range_size * 0.6, 'b': min_val + range_size * 0.7,
                    'c': min_val + range_size * 0.8, 'd': min_val + range_size * 0.85}
        elif position == 'high':
            return {'a': min_val + range_size * 0.65, 'b': min_val + range_size * 0.75,
                    'c': max_val, 'd': max_val}
        else:
            raise ValueError(f"Position '{position}' não reconhecida. Use: 'low', 'low-medium', 'medium', 'medium-high', 'high'")


class GaussianMF(MembershipFunctionStrategy):

    def create_function(self, universe: np.ndarray, params: Dict) -> np.ndarray:
        return fuzz.gaussmf(universe, params['mean'], params['sigma'])

    def get_default_params(self, position: str, universe_range: Tuple[float, float]) -> Dict:
        min_val, max_val = universe_range
        range_size = max_val - min_val

        if position == 'low':
            return {'mean': min_val, 'sigma': range_size * 0.12}
        elif position == 'low-medium':
            return {'mean': min_val + range_size * 0.25, 'sigma': range_size * 0.10}
        elif position == 'medium':
            return {'mean': min_val + range_size * 0.5, 'sigma': range_size * 0.12}
        elif position == 'medium-high':
            return {'mean': min_val + range_size * 0.75, 'sigma': range_size * 0.10}
        elif position == 'high':
            return {'mean': max_val, 'sigma': range_size * 0.08}  
        else:
            raise ValueError(f"Position '{position}' não reconhecida. Use: 'low', 'low-medium', 'medium', 'medium-high', 'high'")


class GeneralizedBellMF(MembershipFunctionStrategy):

    def create_function(self, universe: np.ndarray, params: Dict) -> np.ndarray:
        return fuzz.gbellmf(universe, params['a'], params['b'], params['c'])

    def get_default_params(self, position: str, universe_range: Tuple[float, float]) -> Dict:
        min_val, max_val = universe_range
        range_size = max_val - min_val

        width = range_size * 0.15
        slope = 2.5

        if position == 'low':
            return {'a': width, 'b': slope, 'c': min_val}
        elif position == 'low-medium':
            return {'a': width * 0.9, 'b': slope, 'c': min_val + range_size * 0.25}
        elif position == 'medium':
            return {'a': width, 'b': slope, 'c': min_val + range_size * 0.5}
        elif position == 'medium-high':
            return {'a': width * 0.9, 'b': slope, 'c': min_val + range_size * 0.75}
        elif position == 'high':
            return {'a': width * 0.75, 'b': slope, 'c': max_val}
        else:
            raise ValueError(f"Position '{position}' não reconhecida. Use: 'low', 'low-medium', 'medium', 'medium-high', 'high'")


class SigmoidalMF(MembershipFunctionStrategy):

    def create_function(self, universe: np.ndarray, params: Dict) -> np.ndarray:
 
        if 'mean' in params and 'sigma' in params:
            return fuzz.gaussmf(universe, params['mean'], params['sigma'])
 
        return fuzz.sigmf(universe, params['c'], params['a'])

    def get_default_params(self, position: str, universe_range: Tuple[float, float]) -> Dict:
        min_val, max_val = universe_range
        range_size = max_val - min_val

        slope = 1.0 / (range_size * 0.08)

        if position == 'low':
            return {'a': -slope, 'c': min_val + range_size * 0.25}
        elif position == 'low-medium':
            return GaussianMF().get_default_params('low-medium', universe_range)
        elif position == 'medium':
            return GaussianMF().get_default_params('medium', universe_range)
        elif position == 'medium-high':
            return GaussianMF().get_default_params('medium-high', universe_range)
        elif position == 'high':
            return {'a': slope, 'c': min_val + range_size * 0.75}
        else:
            raise ValueError(f"Position '{position}' não reconhecida. Use: 'low', 'low-medium', 'medium', 'medium-high', 'high'")


class MembershipFunctionFactory:

    _strategies = {
        'triangular': TriangularMF,
        'trapezoidal': TrapezoidalMF,
        'gaussian': GaussianMF,
        'bell': GeneralizedBellMF,
        'sigmoidal': SigmoidalMF
    }

    @classmethod
    def create(cls, function_type: str) -> MembershipFunctionStrategy:
        strategy_class = cls._strategies.get(function_type.lower())
        if strategy_class is None:
            available = ', '.join(cls._strategies.keys())
            raise ValueError(f"Tipo '{function_type}' inválido. Disponíveis: {available}")
        return strategy_class()

    @classmethod
    def available_types(cls) -> list:
        return list(cls._strategies.keys())
