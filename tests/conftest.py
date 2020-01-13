import os

from hypothesis import (HealthCheck,
                        settings)

on_azure_pipelines = os.getenv('TF_BUILD', False)
on_travis_ci = os.getenv('CI', False)
settings.register_profile('default',
                          max_examples=(settings.default.max_examples // 5
                                        if on_azure_pipelines or on_travis_ci
                                        else settings.default.max_examples),
                          deadline=None,
                          suppress_health_check=[HealthCheck.data_too_large,
                                                 HealthCheck.filter_too_much,
                                                 HealthCheck.too_slow])
