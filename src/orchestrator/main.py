from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import yaml
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from rich.console import Console
from rich.table import Table

from .schemas import CONFIG_SCHEMA

console = Console()
log = logging.getLogger("orchestrator")


def load_config(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


def validate_config(cfg: Dict[str, Any]) -> None:
    try:
        validate(instance=cfg, schema=CONFIG_SCHEMA)
    except ValidationError as e:
        raise SystemExit(f"Config validation error: {e.message} at {list(e.absolute_path)}")


def summarize(cfg: Dict[str, Any]) -> None:
    table = Table(title="Orchestrator Plan (dry-run)", show_lines=True)
    table.add_column("Section")
    table.add_column("Details")
    table.add_row("Target Repo", f"{cfg.get('target_repo')} @ {cfg.get('commit','HEAD')}")
    table.add_row("Include", ", ".join(cfg["paths"]["include"]))
    table.add_row("Exclude", ", ".join(cfg["paths"]["exclude"]))
    job = cfg["job"]
    table.add_row("Job", f"{job['id']} — {job['goal']}")
    scope = job.get("scope", {})
    table.add_row("Scope.allow", ", ".join(scope.get("allow", [])))
    table.add_row("Scope.deny", ", ".join(scope.get("deny", [])))
    table.add_row("Agents", f"reader={cfg['agents']['reader']}, planner={cfg['agents']['planner']}, coder={cfg['agents']['coder']}")
    table.add_row("Mode", job["mode"])
    console.print(table)


def write_artifacts(cfg: Dict[str, Any], artifacts_dir: Path) -> None:
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    (artifacts_dir / "orchestrator.config.json").write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    (artifacts_dir / "README.txt").write_text(
        "Artifacts placeholder. This is where RepoSnapshot.json, ChangePlan.json, and PatchSet diffs will be saved.\n",
        encoding="utf-8",
    )


def run(cfg_path: Path, dry_run: bool) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    cfg = load_config(cfg_path)
    validate_config(cfg)
    summarize(cfg)

    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    art = Path("artifacts") / ts
    write_artifacts(cfg, art)
    log.info("Artifacts directory: %s", art)

    if dry_run or cfg["job"]["mode"] == "analyze_only":
        console.print("[bold green]Dry-run complete.[/bold green] You can now edit orchestrator.yml and rerun.")
        return

    # Stubs for Reader → Planner → Coder. Replace with real API calls later.
    console.print("[yellow]Reader[/yellow]: would produce RepoSnapshot.json")
    console.print("[yellow]Planner[/yellow]: would produce ChangePlan.json")
    console.print("[yellow]Coder[/yellow]: would produce PatchSet diffs and open a PR")
    console.print("[bold green]Done.[/bold green]")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AI Orchestrator driver")
    p.add_argument("--config", default="orchestrator.yml", help="Path to single-file orchestrator config")
    p.add_argument("--dry-run", action="store_true", help="Validate and summarize without calling agents")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(Path(args.config), dry_run=args.dry_run)
