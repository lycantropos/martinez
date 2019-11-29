from hypothesis import strategies

floats = strategies.floats(allow_nan=False,
                           allow_infinity=True)
scalars = (strategies.integers() | floats
           | strategies.decimals(allow_nan=False)
           | strategies.fractions())
