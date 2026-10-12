"""Edition-aware UI entry (Streamlit / FastAPI placeholder)."""
def launch(config: dict):
    edition = config.get("edition", "operator")
    show_grafana = config.get("ui", {}).get("show_grafana_link", False)
    print(f"Launching {edition} UI (Grafana link: {show_grafana})")
    # TODO: Streamlit or FastAPI + frontend
    # if show_grafana:
    #     print("Grafana button enabled")