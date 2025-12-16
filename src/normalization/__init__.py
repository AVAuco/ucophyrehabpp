# src/normalization/__init__.py
from .zscore import zscore_normalization
# en el futuro: from .minmax import minmax_normalization, etc.

def get_normalization_function(name: str):
    """Devuelve la función (o clase) de normalización según su nombre."""
    name = name.lower()
    if name == "none":
        return None
    if name == "zscore":
        return zscore_normalization        
    # ejemplos futuros
    # elif name == "minmax":
    #     from .minmax import minmax_normalization
    #     return minmax_normalization
    else:
        raise ValueError(f"Normalización desconocida: {name}")
