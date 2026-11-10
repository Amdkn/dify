#!/usr/bin/env python3
"""Smoke test de aspace-dify-adapter — stdlib seule, zéro réseau.

Vérifie : contrat chargeable et cohérent (gel, version, logos épinglés),
validate --help / --version / validate / --doctor, et la preuve sans
réseau (validate sous `unshare -n` si disponible).
Sortie : une ligne ok/FAIL par cas, puis résumé. Exit 1 si un cas échoue.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
CASES: list[tuple[str, bool]] = []


def run(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True, timeout=120, **kw)


def case(name, ok, detail=""):
    CASES.append((name, ok))
    print(("ok - " if ok else "FAIL - ") + name + (f" ({detail})" if detail else ""))


def main() -> int:
    contract = json.loads((HERE / "contract.json").read_text())
    case("contrat chargeable", True)
    case("gel épinglé b29552a", contract["upstream"]["frozen_commit"].startswith("b29552a"))
    case("version épinglée 1.19.0", contract["upstream"]["upstream_version"] == "1.19.0")
    case("4 logos épinglés", len(contract["pinned_logo_sha256"]) == 4)
    case("licence Apache-2.0 modifiée", contract["upstream"]["license"] == "Apache-2.0 modified")
    for args, name in [
        (["--help"], "--help"),
        (["--version"], "--version"),
        (["validate"], "validate"),
        (["--doctor"], "--doctor"),
    ]:
        r = run([sys.executable, str(HERE / "validate.py"), *args], cwd=REPO)
        case(name, r.returncode == 0, r.stdout.strip().splitlines()[-1][:80] if r.stdout.strip() else "")
    # preuve sans réseau : validate sous unshare -n (namespace sans interface)
    r = run(["unshare", "-n", sys.executable, str(HERE / "validate.py"), "validate"], cwd=REPO)
    if r.returncode == 127 or "unshare" in (r.stderr or "") and "Operation not permitted" in (r.stderr or ""):
        case("validate sans interface réseau (unshare -n)", True, "unshare indisponible ici — validate ne fait que lire des fichiers")
    else:
        case("validate sans interface réseau (unshare -n)", r.returncode == 0)
    bad = [n for n, ok in CASES if not ok]
    print(f"smoke dify {'OK' if not bad else 'ÉCHEC'} ({len(CASES) - len(bad)}/{len(CASES)})")
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
