# AI Orchestrator (workspace)

This repo coordinates multiple AIs:
• Reader (e.g., Claude) summarizes large codebases into a RepoSnapshot
• Planner (GPT-5 Thinking) outputs a ChangePlan + PatchSpecs
• Coder (Copilot Chat or GPT-4/5) returns unified diffs (patches) only

This scaffold focuses on config, validation, and run wiring. Model calls are stubbed so you can plug your providers later.

## How to use in VS Code
1. Open this folder in VS Code.
2. When prompted, create a Python virtual environment and install requirements from `requirements.txt`.
3. Edit `orchestrator.yml` (set `target_repo`, paths, and the `job` section).
4. Run → “Python: Orchestrator” to validate and perform a dry-run. Artifacts land in `./artifacts/<timestamp>/`.
