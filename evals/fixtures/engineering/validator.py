def duplicate(days):
    if not isinstance(days, int) or days < 0:
        raise ValueError('nonnegative integer required')
    return days < 30
