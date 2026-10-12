"""Placeholder for core engine startup."""
def start(config: dict):
    print(f"Engine starting with edition: {config.get('edition')}")
    # TODO: Wire sensors → fusion → UI → metrics
    # from app.metrics import start_metrics_server
    # start_metrics_server()