from pathlib import Path
import yaml
from orchestrator.schemas import CONFIG_SCHEMA
from jsonschema import validate

def test_yaml_validates():
    cfg = yaml.safe_load(Path("orchestrator.yml").read_text(encoding="utf-8"))
    validate(instance=cfg, schema=CONFIG_SCHEMA)
