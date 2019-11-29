from hypothesis import strategies

coordinates = strategies.floats(allow_nan=True,
                                allow_infinity=True)
