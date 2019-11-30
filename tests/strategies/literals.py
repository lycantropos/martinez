from hypothesis import strategies

floats = strategies.floats(allow_nan=False,
                           allow_infinity=False)
scalars = (strategies.integers() | floats
           | strategies.decimals(allow_nan=False,
                                 allow_infinity=False)
           | strategies.fractions())
