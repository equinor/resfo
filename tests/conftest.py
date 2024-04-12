from hypothesis import HealthCheck, settings


settings.register_profile(
    "no_timeouts",
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
    print_blob=True,
)
settings.load_profile("no_timeouts")
