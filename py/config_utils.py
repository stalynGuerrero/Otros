from pathlib import Path
import yaml
from yaml.loader import SafeLoader

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_FILE = DATA_DIR / "config.yaml"

def guardar_config(config_obj):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        yaml.dump(
            config_obj,
            f,
            default_flow_style=False,
            allow_unicode=True
        )


def cargar_config():
    if not CONFIG_FILE.exists():
        base = {
            "credentials": {"usernames": {}},
            "cookie": {
                "name": "reemplazos_cookie",
                "key": "clave_segura",
                "expiry_days": 30
            },
            "preauthorized": {"emails": []}
        }
        guardar_config(base)
        return base

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = yaml.load(f, Loader=SafeLoader) or {}

    cfg.setdefault("credentials", {}).setdefault("usernames", {})
    cfg.setdefault("cookie", {})
    cfg.setdefault("preauthorized", {}).setdefault("emails", [])

    return cfg
