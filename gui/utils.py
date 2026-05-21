def calc_pct(atual: int, maximo: int) -> float:
    """Return the ratio atual/maximo clamped to [0, 1]."""
    return min(atual / maximo, 1.0) if maximo > 0 else 0.0
