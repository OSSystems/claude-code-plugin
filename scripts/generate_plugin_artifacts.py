#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
PLUGINS_DIR = ROOT / "plugins"


def load_json(path: Path):
    return json.loads(path.read_text())


def dump_json(data) -> str:
    return json.dumps(data, indent=2, ensure_ascii=True) + "\n"


def skill_markdown(skill: dict, source_body: str) -> str:
    return (
        "---\n"
        f"name: {skill['name']}\n"
        f"description: {skill['description']}\n"
        "---\n\n"
        f"# {skill['title']}\n\n"
        f"{source_body.strip()}\n"
    )


def claude_plugin_manifest(plugin: dict) -> dict:
    return {
        "name": plugin["name"],
        "description": plugin["description"],
        "version": plugin["version"],
        "author": plugin["author"],
        "repository": plugin["repository"],
        "homepage": plugin["homepage"],
        "license": plugin["license"],
        "keywords": plugin["keywords"],
    }


def codex_plugin_manifest(plugin: dict) -> dict:
    return {
        "name": plugin["name"],
        "version": plugin["version"],
        "description": plugin["description"],
        "author": plugin["author"],
        "homepage": plugin["homepage"],
        "repository": plugin["repository"],
        "license": plugin["license"],
        "keywords": plugin["keywords"],
        "skills": "./skills/",
        "interface": {
            "displayName": plugin["codexInterface"]["displayName"],
            "shortDescription": plugin["codexInterface"]["shortDescription"],
            "longDescription": plugin["codexInterface"]["longDescription"],
            "developerName": plugin["codexInterface"]["developerName"],
            "category": plugin["category"],
            "capabilities": plugin["codexInterface"]["capabilities"],
            "websiteURL": plugin["homepage"],
            "defaultPrompt": plugin["codexInterface"]["defaultPrompt"],
        },
    }


def build_claude_marketplace(catalog: dict, plugins: list[dict]) -> dict:
    entries = []
    for plugin in plugins:
        if not plugin["publishTo"]["claude"]:
            continue
        entries.append(
            {
                "name": plugin["name"],
                "source": f"./plugins/{plugin['name']}",
                "description": plugin["description"],
                "category": plugin["category"].lower(),
            }
        )
    return {
        "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
        "name": catalog["name"],
        "version": catalog["version"],
        "description": catalog["description"],
        "owner": catalog["owner"],
        "metadata": {"description": "OS Systems company-wide development tools and standards"},
        "plugins": entries,
    }


def build_codex_marketplace(catalog: dict, plugins: list[dict]) -> dict:
    entries = []
    for plugin in plugins:
        if not plugin["publishTo"]["codex"]:
            continue
        entries.append(
            {
                "name": plugin["name"],
                "source": {
                    "source": "local",
                    "path": f"./plugins/{plugin['name']}",
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": plugin["category"],
            }
        )
    return {
        "name": catalog["name"],
        "interface": catalog["interface"],
        "plugins": entries,
    }


def write_if_changed(path: Path, content: str, check: bool) -> bool:
    current = path.read_text() if path.exists() else None
    if current == content:
        return False
    if check:
        print(f"stale generated file: {path.relative_to(ROOT)}", file=sys.stderr)
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    catalog = load_json(SOURCES / "catalog.json")
    plugins = [load_json(SOURCES / "plugins" / f"{name}.json") for name in catalog["plugins"]]

    stale = False

    for plugin in plugins:
        plugin_root = PLUGINS_DIR / plugin["name"]
        for skill in plugin["skills"]:
            body = (SOURCES / "skills" / skill["source"]).read_text()
            markdown = skill_markdown(skill, body)
            stale |= write_if_changed(
                plugin_root / "skills" / skill["name"] / "SKILL.md", markdown, args.check
            )

        stale |= write_if_changed(
            plugin_root / ".claude-plugin" / "plugin.json",
            dump_json(claude_plugin_manifest(plugin)),
            args.check,
        )

        stale |= write_if_changed(
            plugin_root / ".codex-plugin" / "plugin.json",
            dump_json(codex_plugin_manifest(plugin)),
            args.check,
        )

    stale |= write_if_changed(
        ROOT / ".claude-plugin" / "marketplace.json",
        dump_json(build_claude_marketplace(catalog, plugins)),
        args.check,
    )

    stale |= write_if_changed(
        ROOT / ".agents" / "plugins" / "marketplace.json",
        dump_json(build_codex_marketplace(catalog, plugins)),
        args.check,
    )

    return 1 if stale and args.check else 0


if __name__ == "__main__":
    raise SystemExit(main())
