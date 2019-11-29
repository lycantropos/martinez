from hypothesis import strategies

coordinates = strategies.floats(allow_nan=False,
                                allow_infinity=True)
