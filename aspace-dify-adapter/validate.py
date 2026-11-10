#!/usr/bin/env python3
"""aspace-dify-adapter — validation hors-ligne du dépôt dify au gel.

Surface de l'adapter (contrat seul, D-N048 §1.5) :
  validate [--repo <chemin>]  — structure, LICENSE (deux conditions
    additionnelles : mono-tenant uniquement, LOGO/copyright web/ intacts),
    logos web/ intacts (sha256 épinglés dans contract.json), version 1.19.0.
  --version                   — version amont épinglée + gel.
  --doctor                    — posture télémétrie par défaut (informative).

L'adapter ne démarre jamais api/ ni web/, ne touche jamais à web/,
n'appelle jamais le réseau, ne lit aucun secret. Stdlib seule.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_DEFAULT = HERE.parent
FROZEN_COMMIT = "b29552aae0acb1801eeb2870a552cd939fe36a20"
PINNED_VERSION = "1.19.0"

REQUIRED_PATHS = ["api", "web", "LICENSE", "docker", "api/pyproject.toml", "web/package.json"]
LICENSE_MARKERS = [
    "Multi-tenant service: Unless explicitly authorized by Dify in writing, you may not use the Dify source code to operate a multi-tenant environment.",
    "LOGO and copyright information: In the process of using Dify's frontend, you may not remove or modify the LOGO or copyright information",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition: bool, label: str, failures: list[str]) -> bool:
    print(("ok - " if condition else "FAIL - ") + label)
    if not condition:
        failures.append(label)
    return condition


def cmd_validate(repo: Path) -> int:
    failures: list[str] = []
    contract = json.loads((HERE / "contract.json").read_text())
    check((repo / ".git").exists(), "dépôt git présent", failures)
    for p in REQUIRED_PATHS:
        check((repo / p).exists(), f"présent : {p}", failures)
    license_text = (repo / "LICENSE").read_text()
    for m in LICENSE_MARKERS:
        check(m in license_text, "LICENSE : condition additionnelle présente", failures)
    check("Apache License 2.0" in license_text, "LICENSE : base Apache 2.0", failures)
    for rel, pinned in contract["pinned_logo_sha256"].items():
        f = repo / rel
        check(f.exists() and sha256(f) == pinned, f"logo intact : {rel}", failures)
    # version lue depuis web/package.json (source JSON fiable)
    web_version = json.loads((repo / "web/package.json").read_text()).get("version")
    check(web_version == PINNED_VERSION, f"version amont {web_version} == {PINNED_VERSION}", failures)
    check(contract["upstream"]["frozen_commit"] == FROZEN_COMMIT, f"gel épinglé {FROZEN_COMMIT[:7]}", failures)
    if failures:
        print(f"validate dify ÉCHEC ({len(failures)} échec(s))")
        return 1
    print("validate dify OK (structure, LICENSE, logos, version)")
    return 0


def cmd_version() -> int:
    print(f"dify 1.19.0 (gel b29552a, fork Amdkn/dify, adapter 0.1.0)")
    return 0


def cmd_doctor() -> int:
    print("posture télémétrie par défaut (amont, lue au code — aucun envoi par cet outil) :")
    print("  - télémétrie communautaire api/ : DÉFAUT ON (DISABLE_TELEMETRY=false, DO_NOT_TRACK=false,")
    print("    endpoints https://otel.dify.ai/v1/events + fallback https://otel.dify.cn/v1/events,")
    print("    événements install (1×) + heartbeat (≤1/jour), charge anonyme ; porte : édition COMMUNITY)")
    print("  - coupure par contrat : DISABLE_TELEMETRY=true + DO_NOT_TRACK=true + CI=true")
    print("  - Sentry api/web : OFF sans DSN (SENTRY_DSN unset par défaut)")
    print("  - OpenTelemetry api : OFF par défaut (ENABLE_OTEL=false)")
    print("  - Amplitude web : OFF sans clé (NEXT_PUBLIC_AMPLITUDE_API_KEY vide par défaut, opt-out par défaut)")
    print("  - OTel entreprise : OFF par défaut (ENTERPRISE_TELEMETRY_ENABLED=false, édition ENTERPRISE seule)")
    print("  - PostHog : dépendance transitive inutilisée de chromadb (jamais importé par api/)")
    print("  - l'adapter ne démarre aucun serveur et n'émet rien ; la coupure s'applique au déploiement")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="validate.py", description="aspace-dify-adapter — validation hors-ligne")
    ap.add_argument("command", nargs="?", default="validate", choices=["validate"])
    ap.add_argument("--version", action="store_true")
    ap.add_argument("--doctor", action="store_true")
    ap.add_argument("--repo", default=str(REPO_DEFAULT))
    args = ap.parse_args()
    if args.version:
        return cmd_version()
    if args.doctor:
        return cmd_doctor()
    return cmd_validate(Path(args.repo))


if __name__ == "__main__":
    raise SystemExit(main())
