#!/usr/bin/env python3
"""Quality gate: validates n8n export structure and scans tracked project files.

Static tests only. Never connects to n8n or an AI provider.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

AGENT_TYPE = "@n8n/n8n-nodes-langchain.agent"
MODEL_TYPE = "@n8n/n8n-nodes-langchain.lmChatOpenAi"
CALCULATOR_TYPE = "@n8n/n8n-nodes-langchain.toolCalculator"
REQUIRED_STAGES = ("Triagem", "Qualidade", "Analise", "Relatorio", "Auditoria")
ROOT = Path(__file__).resolve().parents[1]
SECRET_RE = [
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{25,})\b"),
    re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{30,}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9_.-]{24,}\b", re.I),
    re.compile(r"(?i)[\"'](?:api_key|client_secret|access_token|refresh_token|password)[\"']\s*:\s*[\"'][^\"']{12,}[\"']"),
]
FORBIDDEN_FILES = (".env", "credentials.json", "n8n.sqlite", "database.sqlite")
SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}


def check(condition, message):
    if not condition:
        raise ValueError(message)


def iter_project_files():
    try:
        names = subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-files"], text=True, stderr=subprocess.DEVNULL
        ).splitlines()
        if names:
            return [ROOT / name for name in names]
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    return [p for p in ROOT.rglob("*") if p.is_file()
            and not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts)]


def scan_secrets():
    files = list(iter_project_files())
    for p in files:
        if not p.exists() or not p.is_file():
            continue
        check(p.name not in FORBIDDEN_FILES, f"Arquivo sensível versionado: {p.relative_to(ROOT)}")
        if p.suffix.lower() not in {".py", ".js", ".mjs", ".json", ".md", ".yml", ".yaml", ".txt", ".ps1"}:
            continue
        data = p.read_text(encoding="utf-8", errors="replace")
        for rule in SECRET_RE:
            check(not rule.search(data), f"Possível segredo em {p.relative_to(ROOT)}")
    print(f"Segredos: varredura de padrões comuns em {len(files)} arquivos (não é auditoria completa).")


def check_agents(d, path):
    nodes = d["nodes"]
    agents = [n for n in nodes if n["type"] == AGENT_TYPE]
    models = [n for n in nodes if n["type"] == MODEL_TYPE]
    tools = [n for n in nodes if n["type"] == CALCULATOR_TYPE]
    check(len(agents) == len(models) == len(tools) == 5,
          f"{path.name}: esperados 5 agentes, modelos e calculadoras")
    names = {n["name"] for n in nodes}
    for stage in REQUIRED_STAGES:
        check(any(stage.lower() in n["name"].lower() for n in agents),
              f"{path.name}: agente ausente {stage}")
    connections = d["connections"]
    for agent in agents:
        inbound_model = any(
            item.get("node") == agent["name"]
            for n in models for group in connections.get(n["name"], {}).get("ai_languageModel", [])
            for item in group
        )
        inbound_tool = any(
            item.get("node") == agent["name"]
            for n in tools for group in connections.get(n["name"], {}).get("ai_tool", [])
            for item in group
        )
        check(inbound_model and inbound_tool,
              f"{path.name}: modelo e ferramenta exigidos em {agent['name']}")
    first = next(n["name"] for n in agents if "Triagem" in n["name"])
    cur = first
    visited = {cur}
    for _ in range(4):
        candidates = [
            edge["node"] for group in connections.get(cur, {}).get("main", [])
            for edge in group if edge["node"] in names
        ]
        check(len(candidates) == 1, f"{path.name}: ligação principal ausente após {cur}")
        cur = candidates[0]
        check(cur not in visited and any(n["name"] == cur for n in agents),
              f"{path.name}: ordem dos cinco agentes interrompida")
        visited.add(cur)
    check(any("Auditoria" in x for x in visited),
          f"{path.name}: cadeia não termina em Auditoria")


def verify_workflow(path):
    d = json.loads(path.read_text(encoding="utf-8"))
    check(isinstance(d, dict), f"{path.name}: JSON raiz inválido")
    check(d.get("active") is False, f"{path.name}: export deve ser desativado")
    check(not d.get("pinData"), f"{path.name}: pinData deve ser vazio")
    nodes = d.get("nodes", [])
    check(isinstance(nodes, list) and bool(nodes), f"{path.name}: sem nós")
    names = [n.get("name") for n in nodes]
    ids = [n.get("id") for n in nodes]
    check(all(names) and len(names) == len(set(names)), f"{path.name}: nomes repetidos")
    check(all(ids) and len(ids) == len(set(ids)), f"{path.name}: IDs repetidos")
    for n in nodes:
        check("credentials" not in n, f"{path.name}: credencial incorporada em {n.get('name')}")
        check(n.get("type") and isinstance(n.get("parameters"), dict),
              f"{path.name}: nó malformado {n.get('name')}")
    nameset = set(names)
    for origin, ports in d.get("connections", {}).items():
        check(origin in nameset, f"{path.name}: origem inexistente {origin}")
        for groups in ports.values():
            for group in groups:
                for edge in group:
                    check(edge.get("node") in nameset,
                          f"{path.name}: destino inexistente {edge.get('node')}")
    if any(n["type"] == AGENT_TYPE for n in nodes):
        check_agents(d, path)
    else:
        check(not any(n["type"] in (MODEL_TYPE, CALCULATOR_TYPE) for n in nodes),
              f"{path.name}: modelos desconectados sem agentes")
    print(f"OK {path.relative_to(ROOT)}: {len(nodes)} nós")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("main", "portfolio"), required=True)
    args = parser.parse_args()
    files = sorted((ROOT / "workflows").glob("*.json"))
    check(bool(files), "Pasta workflows vazia")
    if args.mode == "main":
        numbers = {p.name.split("_", 1)[0] for p in files}
        check(set("01 02 03 04 05 06 07".split()).issubset(numbers),
              "Faltam exports 01–07")
        check(len(files) == 7, "Workflow desconhecido: revisar política antes de incluir")
    else:
        check(len(files) == 1 and files[0].name == "cinco_agentes_demo_sanitizado.json",
              "Portfólio deve conter apenas o fluxo demonstrativo sanitizado")
    for path in files:
        verify_workflow(path)
    scan_secrets()
    print("APROVADO: validação estrutural e verificação básica de segredos")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"FALHA: {exc}", file=sys.stderr)
        sys.exit(1)
