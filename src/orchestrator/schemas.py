from __future__ import annotations

CONFIG_SCHEMA = {
    "type": "object",
    "required": [
        "version",
        "target_repo",
        "paths",
        "policy",
        "ci_checks",
        "agents",
        "job",
    ],
    "properties": {
        "version": {"type": "integer"},
        "target_repo": {"type": "string", "minLength": 1},
        "commit": {"type": "string"},
        "language": {"type": "string"},
        "paths": {
            "type": "object",
            "required": ["include", "exclude"],
            "properties": {
                "include": {"type": "array", "items": {"type": "string"}},
                "exclude": {"type": "array", "items": {"type": "string"}},
            },
        },
        "policy": {
            "type": "object",
            "properties": {
                "require_tests_on_src_change": {"type": "boolean"},
                "protected_paths": {"type": "array", "items": {"type": "string"}},
            },
        },
        "scrub": {
            "type": "object",
            "properties": {"ignore_globs": {"type": "array", "items": {"type": "string"}}},
        },
        "ci_checks": {"type": "array", "items": {"type": "string"}},
        "agents": {
            "type": "object",
            "required": ["reader", "planner", "coder"],
            "properties": {
                "reader": {"type": "string"},
                "planner": {"type": "string"},
                "coder": {"type": "string"},
            },
        },
        "job": {
            "type": "object",
            "required": ["id", "goal", "scope", "patch_policy", "mode"],
            "properties": {
                "id": {"type": "string"},
                "goal": {"type": "string"},
                "scope": {
                    "type": "object",
                    "properties": {
                        "allow": {"type": "array", "items": {"type": "string"}},
                        "deny": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "tests": {
                    "type": "object",
                    "properties": {
                        "touched_required": {"type": "boolean"},
                        "add": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "acceptance": {"type": "array", "items": {"type": "string"}},
                "patch_policy": {
                    "type": "object",
                    "required": ["require_unified_diff"],
                    "properties": {
                        "require_unified_diff": {"type": "boolean"},
                        "max_files": {"type": "integer"},
                        "max_lines": {"type": "integer"},
                        "fail_if_anchors_missing": {"type": "boolean"},
                    },
                },
                "branching": {
                    "type": "object",
                    "properties": {
                        "prefix": {"type": "string"},
                        "reviewers": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "mode": {"enum": ["analyze_only", "plan_only", "plan_and_pr"]},
            },
        },
    },
}
