"""RetailSense main entry point."""
import os
import yaml
from pathlib import Path

def load_config():
    edition = os.getenv("EDITION", "operator")
    base = Path("configs/base.yaml")
    edition_cfg = Path(f"configs/{edition}.yaml")
    config = {}
    if base.exists():
        with open(base) as f:
            config.update(yaml.safe_load(f) or {})
    if edition_cfg.exists():
        with open(edition_cfg) as f:
            config.update(yaml.safe_load(f) or {})
    config["edition"] = edition
    return config

if __name__ == "__main__":
    config = load_config()
    print(f"Starting RetailSense in {config['edition']} edition")
    # TODO: Initialize sensors, fusion engine, UI, metrics server
    # from app.core.engine import start
    # start(config)