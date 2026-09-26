#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AxionR v2.0.0
Professional Web Security Reconnaissance & Assessment Framework

Single-file, Kali-friendly framework.

Authorized-use notice:
    Run AxionR only against systems you own or are explicitly authorized
    to assess. This framework is designed for defensive security testing,
    labs, CTFs and authorized penetration testing.

Examples:
    python3 axionr.py
    python3 axionr.py example.com --mode full
    python3 axionr.py example.com --mode recon
    python3 axionr.py --setup
    python3 axionr.py --status
    python3 axionr.py example.com --mode quick --no-install

The framework uses external security tools when available. Missing tools
are detected and can be installed through apt/pip/go after confirmation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

APP_NAME = "AxionR"
VERSION = "2.0.0"
TAGLINE = "Web Security Reconnaissance & Assessment Framework"

ROOT = Path(__file__).resolve().parent
WORKSPACE_ROOT = ROOT / "workspace"
WORDLIST_ROOT = ROOT / "wordlists"
CONFIG_ROOT = ROOT / "config"
CONFIG_FILE = CONFIG_ROOT / "config.json"
LOG_ROOT = ROOT / "logs"

PYTHON_PACKAGES = {
    "requests": "requests",
    "rich": "rich",
}

APT_PACKAGES = [
    "git",
    "curl",
    "nmap",
    "whatweb",
    "wafw00f",
    "sqlmap",
]

TOOLS: Dict[str, Dict[str, Any]] = {
    "subfinder": {"group": "Recon", "install": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder", "purpose": "Subdomain discovery"},
    "amass": {"group": "Recon", "install": "github.com/owasp-amass/amass/v4/cmd/amass", "purpose": "Asset and subdomain enumeration"},
    "gau": {"group": "Recon", "install": "github.com/lc/gau/v2/cmd/gau", "purpose": "Passive URL discovery"},
    "waybackurls": {"group": "Recon", "install": "github.com/tomnomnom/waybackurls", "purpose": "Wayback URL discovery"},
    "dnsx": {"group": "Recon", "install": "github.com/projectdiscovery/dnsx/cmd/dnsx", "purpose": "DNS probing"},
    "httpx": {"group": "Recon", "install": "github.com/projectdiscovery/httpx/cmd/httpx", "purpose": "HTTP probing and metadata"},
    "katana": {"group": "Recon", "install": "github.com/projectdiscovery/katana/cmd/katana", "purpose": "Web crawling"},
    "hakrawler": {"group": "Recon", "install": "github.com/hakluke/hakrawler", "purpose": "Web crawling"},
    "nmap": {"group": "Network", "install": None, "purpose": "Port and service enumeration"},
    "naabu": {"group": "Network", "install": "github.com/projectdiscovery/naabu/v2/cmd/naabu", "purpose": "Port discovery"},
    "whatweb": {"group": "Network", "install": None, "purpose": "Technology fingerprinting"},
    "wafw00f": {"group": "Network", "install": None, "purpose": "WAF detection"},
    "ffuf": {"group": "Web", "install": "github.com/ffuf/ffuf/v2", "purpose": "Content discovery"},
    "arjun": {"group": "Web", "install": None, "purpose": "Parameter discovery"},
    "nuclei": {"group": "Assessment", "install": "github.com/projectdiscovery/nuclei/v3/cmd/nuclei", "purpose": "Template-based security checks"},
    "dalfox": {"group": "Assessment", "install": "github.com/hahwul/dalfox/v2", "purpose": "XSS assessment"},
    "sqlmap": {"group": "Assessment", "install": None, "purpose": "SQL injection assessment"},
    "curl": {"group": "Utility", "install": None, "purpose": "HTTP utility"},
    "git": {"group": "Utility", "install": None, "purpose": "Repository utility"},
}

PHASES = [
    ("setup", "SETUP", "Environment and dependency readiness"),
    ("scope", "SCOPE", "Authorized target scope validation"),
    ("recon", "RECONNAISSANCE", "Passive and active asset discovery"),
    ("asset_discovery", "ASSET DISCOVERY", "DNS, hosts, ports and technologies"),
    ("url_discovery", "URL DISCOVERY", "URLs, crawling and historical endpoints"),
    ("javascript_analysis", "JAVASCRIPT ANALYSIS", "JavaScript endpoint and secret candidate review"),
    ("parameter_discovery", "PARAMETER DISCOVERY", "Web parameter discovery"),
    ("content_discovery", "CONTENT DISCOVERY", "Authorized content/path discovery"),
    ("security_assessment", "SECURITY ASSESSMENT", "Low-impact vulnerability assessment"),
    ("finding_analysis", "FINDING ANALYSIS", "Normalize, deduplicate and classify findings"),
    ("evidence", "EVIDENCE", "Evidence and execution metadata"),
    ("reporting", "REPORTING", "HTML, JSON and summary report generation"),
]

MODE_DESCRIPTIONS = {
    "full": "Complete authorized assessment pipeline",
    "recon": "Asset and attack-surface discovery",
    "bugbounty": "Authorized web application assessment",
    "ctf": "CTF/lab-oriented enumeration workflow",
    "ejpt": "Pentesting and lab enumeration workflow",
    "oscp": "OSCP-style authorized lab enumeration",
    "audit": "Web/security configuration assessment",
    "quick": "Fast initial triage",
    "custom": "User-selected workflow foundation",
}

MODE_PHASES = {
    "full": [p[0] for p in PHASES],
    "recon": ["setup", "scope", "recon", "asset_discovery", "url_discovery", "finding_analysis", "reporting"],
    "bugbounty": [p[0] for p in PHASES],
    "ctf": ["setup", "scope", "asset_discovery", "url_discovery", "content_discovery", "security_assessment", "finding_analysis", "reporting"],
    "ejpt": ["setup", "scope", "asset_discovery", "url_discovery", "content_discovery", "security_assessment", "finding_analysis", "reporting"],
    "oscp": ["setup", "scope", "asset_discovery", "url_discovery", "content_discovery", "security_assessment", "finding_analysis", "reporting"],
    "audit": ["setup", "scope", "asset_discovery", "security_assessment", "finding_analysis", "reporting"],
    "quick": ["setup", "scope", "asset_discovery", "security_assessment", "reporting"],
    "custom": [p[0] for p in PHASES],
}

DEFAULT_CONFIG = {
    "version": VERSION,
    "timeouts": {
        "command": 300,
        "http": 15,
    },
    "concurrency": 4,
    "rate_limit_seconds": 0.2,
    "max_urls_for_active_checks": 100,
    "user_agent": "AxionR/2.0.0 Authorized-Security-Assessment",
    "install_missing_tools": True,
    "report": {
        "html": True,
        "json": True,
    },
}


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "_", value.strip())
    return value.strip("._-") or "target"


def terminal_width(default: int = 92) -> int:
    try:
        return max(70, min(shutil.get_terminal_size().columns, 130))
    except Exception:
        return default


class UI:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"

    @classmethod
    def enabled(cls) -> bool:
        return sys.stdout.isatty() and os.environ.get("AXIONR_NO_COLOR") != "1"

    @classmethod
    def c(cls, text: str, color: str) -> str:
        return f"{color}{text}{cls.RESET}" if cls.enabled() else text

    @classmethod
    def clear(cls) -> None:
        if cls.enabled():
            print("\033[2J\033[H", end="")

    @classmethod
    def banner(cls, compact: bool = False) -> None:
        if compact:
            line = f"AxionR v{VERSION}  |  {TAGLINE}"
            print(cls.c(line, cls.BOLD + cls.CYAN).center(terminal_width()))
            return

        # Explicit AXIONR logo; no figlet/toilet dependency required.
        logo = [
            " █████╗  ██╗  ██╗ ██╗  ██████╗  ███╗   ██╗ ██████╗  ██████╗ ",
            "██╔══██╗ ╚██╗██╔╝ ██║ ██╔═══██╗ ████╗  ██║ ██╔══██╗ ██╔══██╗",
            "███████║  ╚███╔╝  ██║ ██║   ██║ ██╔██╗ ██║ ██████╔╝ ██████╔╝",
            "██╔══██║  ██╔██╗  ██║ ██║   ██║ ██║╚██╗██║ ██╔══██╗ ██╔══██╗",
            "██║  ██║ ██╔╝ ██╗ ██║ ╚██████╔╝ ██║ ╚████║ ██████╔╝ ██║  ██║",
            "╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═╝  ╚═════╝  ╚═╝  ╚═══╝ ╚═════╝  ╚═╝  ╚═╝",
        ]

        width = terminal_width()
        for line in logo:
            print(cls.c(line.center(width), cls.CYAN + cls.BOLD))

        print()
        print(cls.c("AxionR".center(width), cls.CYAN + cls.BOLD))
        print(cls.c(
            "WEB SECURITY RECONNAISSANCE & ASSESSMENT FRAMEWORK".center(width),
            cls.WHITE + cls.BOLD,
        ))
        print(cls.c(
            "Recon • Discovery • Analysis • Evidence • Reporting".center(width),
            cls.GRAY,
        ))
        print()
        print(cls.c(
            f"AxionR v{VERSION}  •  Authorized Security Testing  •  Kali Linux Ready".center(width),
            cls.BLUE + cls.BOLD,
        ))
        print()

    @classmethod
    def intro(cls) -> None:
        """Professional pre-input introduction for the interactive CLI."""
        print(cls.c("  SECURITY ASSESSMENT CONSOLE", cls.BOLD + cls.WHITE))
        print(cls.c("  ─────────────────────────────────────────────────────────────", cls.BLUE))
        print(cls.c("  Enter an authorized target to initialize the assessment.", cls.GRAY))
        print()

    @classmethod
    def startup(cls, no_animation: bool = False) -> None:
        if no_animation or not cls.enabled():
            return
        frames = [
            "INITIALIZING SECURITY ENGINE",
            "LOADING RECON MODULES",
            "LOADING ASSESSMENT MODULES",
            "INITIALIZING REPORT ENGINE",
            "ENGINE READY",
        ]
        for item in frames:
            print(cls.c(f"  ◈ {item} ...", cls.CYAN), end="\r", flush=True)
            time.sleep(0.12)
        print(" " * (terminal_width() - 2), end="\r")

    @classmethod
    def section(cls, number: str, title: str, subtitle: str = "") -> None:
        line = "─" * min(terminal_width() - 2, 108)
        print()
        print(cls.c(line, cls.BLUE))
        print(cls.c(f"  {number}  {title}", cls.CYAN + cls.BOLD))
        if subtitle:
            print(cls.c(f"      {subtitle}", cls.GRAY))
        print(cls.c(line, cls.BLUE))

    @classmethod
    def status(cls, label: str, value: str, color: Optional[str] = None) -> None:
        color = color or cls.WHITE
        print(f"  {cls.c(label.ljust(18), cls.GRAY)} {cls.c(value, color)}")

    @classmethod
    def success(cls, message: str) -> None:
        print(cls.c(f"  ✓ {message}", cls.GREEN))

    @classmethod
    def warning(cls, message: str) -> None:
        print(cls.c(f"  ⚠ {message}", cls.YELLOW))

    @classmethod
    def error(cls, message: str) -> None:
        print(cls.c(f"  ✕ {message}", cls.RED))

    @classmethod
    def info(cls, message: str) -> None:
        print(cls.c(f"  • {message}", cls.CYAN))

    @classmethod
    def progress(cls, label: str, current: int, total: int) -> None:
        total = max(total, 1)
        pct = min(100, int((current / total) * 100))
        width = 34
        filled = int(width * pct / 100)
        bar = "█" * filled + "░" * (width - filled)
        print(f"\r  {label:<24} [{bar}] {pct:>3}%", end="", flush=True)
        if current >= total:
            print()

    @classmethod
    def menu(cls) -> None:
        print(cls.c("  SELECT ASSESSMENT MODE", cls.BOLD + cls.WHITE))
        print()
        modes = [
            ("1", "FULL", "Complete authorized assessment"),
            ("2", "RECON", "Discover domains, hosts, DNS, URLs and attack surface"),
            ("3", "BUG BOUNTY", "Authorized web application assessment"),
            ("4", "CTF", "CTF/lab enumeration workflow"),
            ("5", "eJPT", "Pentesting practice workflow"),
            ("6", "OSCP", "OSCP-style authorized lab workflow"),
            ("7", "AUDIT", "Security configuration assessment"),
            ("8", "QUICK", "Fast initial triage"),
            ("9", "CUSTOM", "Choose individual phases"),
            ("0", "EXIT", "Close AxionR"),
        ]
        for key, name, desc in modes:
            print(f"    {cls.c(key, cls.CYAN + cls.BOLD)}  {cls.c(name.ljust(12), cls.WHITE + cls.BOLD)} {cls.c(desc, cls.GRAY)}")
        print()


    @classmethod
    def final_dashboard(cls, stats: Dict[str, Any], report_dir: Path) -> None:
        print()
        print(cls.c("  ╔════════════════════════════════════════════════════════════╗", cls.CYAN))
        print(cls.c("  ║                 SCAN COMPLETED                           ║", cls.CYAN + cls.BOLD))
        print(cls.c("  ╚════════════════════════════════════════════════════════════╝", cls.CYAN))
        print()
        cls.status("Target", stats.get("target", "-"), cls.WHITE)
        cls.status("Mode", stats.get("mode", "-").upper(), cls.BLUE)
        cls.status("Assets", str(stats.get("assets", 0)), cls.CYAN)
        cls.status("URLs", str(stats.get("urls", 0)), cls.CYAN)
        cls.status("Findings", str(stats.get("findings", 0)), cls.YELLOW)
        cls.status("Critical", str(stats.get("critical", 0)), cls.RED)
        cls.status("High", str(stats.get("high", 0)), cls.RED)
        cls.status("Medium", str(stats.get("medium", 0)), cls.YELLOW)
        cls.status("Low", str(stats.get("low", 0)), cls.GREEN)
        cls.status("Informational", str(stats.get("info", 0)), cls.GRAY)
        print()
        cls.status("Reports", str(report_dir), cls.GREEN)


def import_optional_packages() -> Tuple[Any, Any]:
    requests_mod = None
    rich_mod = None
    try:
        import requests as requests_mod
    except Exception:
        pass
    try:
        import rich as rich_mod
    except Exception:
        pass
    return requests_mod, rich_mod


def ensure_dirs() -> None:
    for p in (WORKSPACE_ROOT, WORDLIST_ROOT, CONFIG_ROOT, LOG_ROOT):
        p.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, indent=2), encoding="utf-8")


def load_config() -> Dict[str, Any]:
    ensure_dirs()
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        merged = json.loads(json.dumps(DEFAULT_CONFIG))
        for key, value in data.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key].update(value)
            else:
                merged[key] = value
        return merged
    except Exception:
        CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, indent=2), encoding="utf-8")
        return json.loads(json.dumps(DEFAULT_CONFIG))


def command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def run_command(
    args: Sequence[str],
    timeout: int = 300,
    cwd: Optional[Path] = None,
    stdin_text: Optional[str] = None,
) -> Tuple[int, str, str]:
    try:
        proc = subprocess.run(
            list(args),
            cwd=str(cwd) if cwd else None,
            input=stdin_text,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ""
        err = exc.stderr or "Command timed out"
        if isinstance(out, bytes):
            out = out.decode(errors="replace")
        if isinstance(err, bytes):
            err = err.decode(errors="replace")
        return 124, out, err
    except FileNotFoundError:
        return 127, "", f"Command not found: {args[0]}"
    except Exception as exc:
        return 1, "", str(exc)


def is_root() -> bool:
    return hasattr(os, "geteuid") and os.geteuid() == 0


def apt_install(packages: Sequence[str]) -> bool:
    if not packages:
        return True
    if not command_exists("apt-get"):
        UI.warning("apt-get is unavailable; skipping apt installation.")
        return False
    if not is_root():
        UI.warning("Root privileges are required for apt installation.")
        UI.info("Run: sudo python3 axionr.py --setup")
        return False
    UI.info("Installing missing apt packages...")
    rc, out, err = run_command(["apt-get", "update"], timeout=600)
    if rc != 0:
        UI.error("apt-get update failed.")
        if err:
            print(err[-1000:])
        return False
    rc, out, err = run_command(["apt-get", "install", "-y", *packages], timeout=900)
    if rc != 0:
        UI.error("apt package installation failed.")
        if err:
            print(err[-1000:])
        return False
    return True


def pip_install(packages: Sequence[str]) -> bool:
    if not packages:
        return True
    UI.info("Installing Python packages...")
    cmd = [sys.executable, "-m", "pip", "install", *packages]
    rc, out, err = run_command(cmd, timeout=600)
    if rc == 0:
        return True
    UI.warning("Standard pip installation failed.")
    # Kali/Debian often blocks system pip through PEP 668.
    rc, out, err = run_command([sys.executable, "-m", "pip", "install", "--user", *packages], timeout=600)
    if rc == 0:
        return True
    UI.warning("Python package installation was not completed.")
    if err:
        print(err[-1200:])
    return False


def go_install(packages: Sequence[str]) -> bool:
    if not packages:
        return True
    if not command_exists("go"):
        UI.warning("Go is not installed. ProjectDiscovery/Go tools cannot be installed automatically.")
        UI.info("Install Go first, then rerun: python3 axionr.py --setup")
        return False
    ok = True
    for pkg in packages:
        UI.info(f"Installing Go tool: {pkg}")
        rc, out, err = run_command(["go", "install", f"{pkg}@latest"], timeout=900)
        if rc != 0:
            ok = False
            UI.warning(f"Failed to install {pkg}")
            if err:
                print(err[-800:])
    return ok


def tool_available(name: str) -> bool:
    return command_exists(name)


def collect_tool_status() -> Dict[str, bool]:
    return {name: tool_available(name) for name in TOOLS}


def show_tool_status() -> None:
    UI.section("00", "TOOL STATUS", "Dependency readiness")
    groups: Dict[str, List[str]] = {}
    for name, meta in TOOLS.items():
        groups.setdefault(meta["group"], []).append(name)
    status = collect_tool_status()
    for group, names in groups.items():
        print(UI.c(f"\n  [{group}]", UI.BOLD + UI.WHITE))
        for name in names:
            mark = UI.c("READY", UI.GREEN) if status[name] else UI.c("MISSING", UI.RED)
            print(f"    {name:<16} {mark:<20} {TOOLS[name]['purpose']}")


def setup_dependencies(allow_install: bool = True) -> None:
    UI.section("01", "ENVIRONMENT SETUP", "Checking runtime and external security tooling")

    if os.name != "posix":
        UI.warning("AxionR is optimized for Kali/Linux. Some installers are Linux-specific.")

    missing_apt = [p for p in APT_PACKAGES if not command_exists(p)]
    missing_py = []
    for module, package in PYTHON_PACKAGES.items():
        try:
            __import__(module)
        except Exception:
            missing_py.append(package)

    missing_go = [
        meta["install"]
        for name, meta in TOOLS.items()
        if not command_exists(name) and meta.get("install")
    ]

    UI.status("Python", sys.version.split()[0], UI.GREEN)
    UI.status("Platform", sys.platform, UI.WHITE)
    UI.status("APT missing", str(len(missing_apt)), UI.YELLOW if missing_apt else UI.GREEN)
    UI.status("Python missing", str(len(missing_py)), UI.YELLOW if missing_py else UI.GREEN)
    UI.status("Go tools missing", str(len(missing_go)), UI.YELLOW if missing_go else UI.GREEN)

    if not allow_install:
        return

    if missing_py:
        pip_install(missing_py)

    # Ask only if packages are actually missing.
    if missing_apt:
        UI.warning("Missing apt packages: " + ", ".join(missing_apt))
        answer = input("  Install missing apt packages? [y/N]: ").strip().lower()
        if answer == "y":
            apt_install(missing_apt)

    if missing_go:
        unique_go = list(dict.fromkeys(missing_go))
        UI.warning(f"{len(unique_go)} Go-based security tools are missing.")
        answer = input("  Install missing Go tools? [y/N]: ").strip().lower()
        if answer == "y":
            go_install(unique_go)

    UI.success("Dependency check completed.")


def normalize_target(raw: str) -> str:
    raw = raw.strip()
    if not raw:
        raise ValueError("Target cannot be empty.")
    if "://" in raw:
        parsed = urllib.parse.urlparse(raw)
        host = parsed.hostname
        if not host:
            raise ValueError("Invalid URL target.")
        return host.lower().rstrip(".")
    # Remove accidental path.
    raw = raw.split("/")[0]
    return raw.lower().rstrip(".")


def validate_target(target: str) -> bool:
    if not target:
        return False
    if len(target) > 253:
        return False
    if re.fullmatch(r"[A-Za-z0-9._:-]+", target) is None:
        return False
    return True


def create_workspace(target: str) -> Path:
    target_dir = WORKSPACE_ROOT / slugify(target)
    folders = [
        "recon", "assets", "dns", "ports", "web", "urls", "javascript",
        "parameters", "content", "scans", "findings", "evidence", "logs",
        "reports",
    ]
    target_dir.mkdir(parents=True, exist_ok=True)
    for folder in folders:
        (target_dir / folder).mkdir(parents=True, exist_ok=True)
    return target_dir


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", errors="replace")


def read_lines(path: Path) -> List[str]:
    if not path.exists():
        return []
    try:
        return [x.strip() for x in path.read_text(encoding="utf-8", errors="replace").splitlines() if x.strip()]
    except Exception:
        return []


def unique_lines(values: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for value in values:
        value = value.strip()
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def write_lines(path: Path, values: Iterable[str]) -> int:
    values = unique_lines(values)
    write_text(path, "\n".join(values) + ("\n" if values else ""))
    return len(values)


def ensure_scope(workspace: Path, target: str) -> Path:
    scope_file = workspace / "scope.txt"
    if not scope_file.exists():
        write_text(
            scope_file,
            f"# AxionR authorized scope\n"
            f"# Review this file before active testing.\n"
            f"{target}\n",
        )
        UI.warning(f"Created scope file: {scope_file}")
    return scope_file


def host_in_scope(host: str, target: str) -> bool:
    host = host.lower().strip(".")
    target = target.lower().strip(".")
    return host == target or host.endswith("." + target)


def url_in_scope(url: str, target: str) -> bool:
    try:
        host = urllib.parse.urlparse(url).hostname
        return bool(host and host_in_scope(host, target))
    except Exception:
        return False


def filter_scoped_urls(urls: Iterable[str], target: str) -> List[str]:
    return unique_lines([u for u in urls if url_in_scope(u, target)])


def resolve_host(target: str) -> List[str]:
    ips = []
    try:
        _, _, addresses = socket.gethostbyname_ex(target)
        ips.extend(addresses)
    except Exception:
        pass
    return unique_lines(ips)


def safe_tool_output(
    workspace: Path,
    phase: str,
    filename: str,
    args: Sequence[str],
    timeout: int,
    stdin_text: Optional[str] = None,
) -> Tuple[int, str, str, Path]:
    out_path = workspace / phase / filename
    rc, out, err = run_command(args, timeout=timeout, cwd=workspace, stdin_text=stdin_text)
    write_text(out_path, out)
    write_text(out_path.with_suffix(out_path.suffix + ".stderr"), err)
    return rc, out, err, out_path


def record_command(log_path: Path, args: Sequence[str], rc: int, started: str, ended: str) -> None:
    entry = {
        "started": started,
        "ended": ended,
        "return_code": rc,
        "command": list(args),
    }
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def execute_tool(
    workspace: Path,
    phase: str,
    filename: str,
    args: Sequence[str],
    timeout: int,
) -> Tuple[int, str, str, Path]:
    log_path = workspace / "logs" / "commands.jsonl"
    started = now_iso()
    rc, out, err, path = safe_tool_output(workspace, phase, filename, args, timeout)
    ended = now_iso()
    record_command(log_path, args, rc, started, ended)
    return rc, out, err, path


def passive_basic_recon(target: str, workspace: Path) -> Dict[str, Any]:
    data: Dict[str, Any] = {"target": target, "ips": resolve_host(target)}
    write_lines(workspace / "dns" / "resolved_ips.txt", data["ips"])

    try:
        rdns = socket.gethostbyname_ex(target)
        aliases = unique_lines(rdns[1])
        write_lines(workspace / "dns" / "aliases.txt", aliases)
        data["aliases"] = aliases
    except Exception:
        data["aliases"] = []

    return data


def run_recon(target: str, workspace: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    UI.section("03", "RECONNAISSANCE", "Passive and active attack-surface discovery")
    assets: List[str] = [target]
    details: Dict[str, Any] = {}

    if command_exists("subfinder"):
        UI.info("Running subfinder...")
        rc, out, err, _ = execute_tool(
            workspace, "recon", "subfinder.txt",
            ["subfinder", "-d", target, "-silent"],
            config["timeouts"]["command"],
        )
        subs = [x.strip() for x in out.splitlines() if host_in_scope(x.strip(), target)]
        write_lines(workspace / "assets" / "subdomains.txt", subs)
        assets.extend(subs)
        details["subfinder"] = {"return_code": rc, "count": len(subs)}
    else:
        UI.warning("subfinder unavailable; using local DNS resolution only.")

    if command_exists("amass"):
        UI.info("Running amass passive enumeration...")
        rc, out, err, _ = execute_tool(
            workspace, "recon", "amass.txt",
            ["amass", "enum", "-passive", "-d", target],
            config["timeouts"]["command"],
        )
        subs = [x.strip() for x in out.splitlines() if host_in_scope(x.strip(), target)]
        existing = read_lines(workspace / "assets" / "subdomains.txt")
        write_lines(workspace / "assets" / "subdomains.txt", existing + subs)
        assets.extend(subs)
        details["amass"] = {"return_code": rc, "count": len(subs)}

    basic = passive_basic_recon(target, workspace)
    assets.extend(read_lines(workspace / "assets" / "subdomains.txt"))
    assets = unique_lines(assets)
    write_lines(workspace / "assets" / "all_hosts.txt", assets)

    details["resolved_ips"] = basic.get("ips", [])
    details["asset_count"] = len(assets)
    UI.success(f"Reconnaissance complete: {len(assets)} in-scope host entries.")
    return {"assets": assets, "details": details}


def run_asset_discovery(target: str, workspace: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    UI.section("04", "ASSET DISCOVERY", "DNS, ports, HTTP services and technology fingerprinting")
    hosts = read_lines(workspace / "assets" / "all_hosts.txt") or [target]
    ports: List[str] = []
    web_urls: List[str] = []
    tech: List[str] = []

    if command_exists("dnsx"):
        source = workspace / "assets" / "all_hosts.txt"
        rc, out, err, _ = execute_tool(
            workspace, "dns", "dnsx.txt",
            ["dnsx", "-l", str(source), "-silent"],
            config["timeouts"]["command"],
        )
        dns_hosts = [x.strip() for x in out.splitlines() if host_in_scope(x.strip(), target)]
        write_lines(workspace / "dns" / "live_hosts.txt", dns_hosts)
        if dns_hosts:
            hosts = unique_lines(hosts + dns_hosts)

    if command_exists("httpx"):
        source = workspace / "assets" / "all_hosts.txt"
        rc, out, err, _ = execute_tool(
            workspace, "web", "httpx.txt",
            ["httpx", "-l", str(source), "-silent", "-title", "-tech-detect", "-status-code"],
            config["timeouts"]["command"],
        )
        write_text(workspace / "web" / "httpx_raw.txt", out)
        for line in out.splitlines():
            m = re.match(r"^\s*(https?://\S+)", line)
            if m and url_in_scope(m.group(1), target):
                web_urls.append(m.group(1))
        write_lines(workspace / "web" / "live_urls.txt", web_urls)

    if command_exists("nmap"):
        UI.info("Running conservative service discovery on the target host...")
        rc, out, err, _ = execute_tool(
            workspace, "ports", "nmap.txt",
            ["nmap", "-Pn", "-sV", "--top-ports", "100", target],
            config["timeouts"]["command"],
        )
        for line in out.splitlines():
            if "/tcp" in line and "open" in line:
                ports.append(line.strip())
        write_lines(workspace / "ports" / "open_services.txt", ports)

    if command_exists("naabu"):
        rc, out, err, _ = execute_tool(
            workspace, "ports", "naabu.txt",
            ["naabu", "-host", target, "-top-ports", "100", "-silent"],
            config["timeouts"]["command"],
        )
        write_lines(workspace / "ports" / "naabu.txt", out.splitlines())

    if command_exists("whatweb"):
        rc, out, err, _ = execute_tool(
            workspace, "web", "whatweb.txt",
            ["whatweb", "--no-errors", target],
            config["timeouts"]["command"],
        )
        tech.extend([x.strip() for x in out.splitlines() if x.strip()])

    if command_exists("wafw00f"):
        rc, out, err, _ = execute_tool(
            workspace, "web", "wafw00f.txt",
            ["wafw00f", target],
            config["timeouts"]["command"],
        )
        write_text(workspace / "web" / "waf_detection.txt", out)

    UI.success(f"Asset discovery complete: {len(web_urls)} web endpoints identified.")
    return {
        "hosts": hosts,
        "web_urls": unique_lines(web_urls),
        "ports": unique_lines(ports),
        "technologies": unique_lines(tech),
    }


def run_url_discovery(target: str, workspace: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    UI.section("05", "URL DISCOVERY", "Historical URLs, crawling and endpoint discovery")
    urls: List[str] = read_lines(workspace / "web" / "live_urls.txt")

    if command_exists("gau"):
        rc, out, err, _ = execute_tool(
            workspace, "urls", "gau.txt",
            ["gau", target],
            config["timeouts"]["command"],
        )
        urls.extend(filter_scoped_urls(out.splitlines(), target))

    if command_exists("waybackurls"):
        rc, out, err, _ = execute_tool(
            workspace, "urls", "waybackurls.txt",
            ["waybackurls", target],
            config["timeouts"]["command"],
        )
        urls.extend(filter_scoped_urls(out.splitlines(), target))

    seed = urls[:100]
    if command_exists("katana") and seed:
        seed_file = workspace / "urls" / "seed.txt"
        write_lines(seed_file, seed)
        rc, out, err, _ = execute_tool(
            workspace, "urls", "katana.txt",
            ["katana", "-list", str(seed_file), "-silent", "-depth", "2"],
            config["timeouts"]["command"],
        )
        urls.extend(filter_scoped_urls(out.splitlines(), target))

    if command_exists("hakrawler") and seed:
        for url in seed[:20]:
            rc, out, err = run_command(["hakrawler", "-url", url], timeout=120)
            urls.extend(filter_scoped_urls(out.splitlines(), target))

    urls = unique_lines(urls)
    write_lines(workspace / "urls" / "all_urls.txt", urls)
    UI.success(f"URL discovery complete: {len(urls)} unique in-scope URLs.")
    return {"urls": urls}


def extract_js_urls(urls: Iterable[str], target: str) -> List[str]:
    result = []
    for url in urls:
        low = url.lower().split("?", 1)[0]
        if low.endswith(".js") and url_in_scope(url, target):
            result.append(url)
    return unique_lines(result)


def run_javascript_analysis(target: str, workspace: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    UI.section("06", "JAVASCRIPT ANALYSIS", "Endpoint and secret candidate review")
    urls = extract_js_urls(read_lines(workspace / "urls" / "all_urls.txt"), target)
    write_lines(workspace / "javascript" / "javascript_urls.txt", urls)

    candidates: List[str] = []
    secret_patterns = [
        r"(?i)(?:api[_-]?key|secret|token|access[_-]?token)\s*[:=]\s*['\"][^'\"]{8,}['\"]",
        r"(?i)(?:aws_access_key_id|client_secret)\s*[:=]\s*['\"][^'\"]+['\"]",
        r"(?i)https?://[A-Za-z0-9._/-]+/api/[A-Za-z0-9._?=&/-]+",
    ]

    requests_mod, _ = import_optional_packages()
    if requests_mod and urls:
        session = requests_mod.Session()
        session.headers.update({"User-Agent": config["user_agent"]})
        for idx, url in enumerate(urls[:100], 1):
            try:
                r = session.get(url, timeout=config["timeouts"]["http"], allow_redirects=True)
                text = r.text[:1_000_000]
                for pattern in secret_patterns:
                    if re.search(pattern, text):
                        candidates.append(f"{url} :: pattern={pattern}")
                # Lightweight endpoint extraction.
                for match in re.findall(r"""["'](\/[A-Za-z0-9_./-]{2,100}(?:\?[A-Za-z0-9_=&.-]+)?)["']""", text):
                    absolute = urllib.parse.urljoin(url, match)
                    if url_in_scope(absolute, target):
                        candidates.append(f"{url} :: endpoint={absolute}")
                if idx % 10 == 0:
                    UI.progress("JavaScript review", idx, min(len(urls), 100))
            except Exception:
                continue

    write_lines(workspace / "javascript" / "candidates.txt", candidates)
    UI.success(f"JavaScript analysis complete: {len(urls)} JS URLs reviewed.")
    return {"js_urls": urls, "candidates": candidates}


def run_parameter_discovery(target: str, workspace: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    UI.section("07", "PARAMETER DISCOVERY", "Identifying application parameters")
    urls = read_lines(workspace / "urls" / "all_urls.txt")
    parameter_urls = [u for u in urls if "?" in u][:200]

    if command_exists("arjun") and parameter_urls:
        seed_file = workspace / "parameters" / "seed.txt"
        write_lines(seed_file, parameter_urls[:30])
        # Arjun CLI differs between releases; use URL-by-URL invocation conservatively.
        raw = []
        for url in parameter_urls[:20]:
            rc, out, err = run_command(["arjun", "-u", url, "--quiet"], timeout=120)
            raw.extend(out.splitlines())
        write_lines(workspace / "parameters" / "arjun.txt", raw)
    else:
        write_lines(
            workspace / "parameters" / "observed_parameters.txt",
            parameter_urls,
        )

    UI.success(f"Parameter discovery complete: {len(parameter_urls)} parameterized URLs observed.")
    return {"parameterized_urls": parameter_urls}


def run_content_discovery(target: str, workspace: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    UI.section("08", "CONTENT DISCOVERY", "Authorized path/content discovery")
    findings = []
    base_urls = read_lines(workspace / "web" / "live_urls.txt") or [f"https://{target}"]

    wordlist_candidates = [
        WORDLIST_ROOT / "common.txt",
        Path("/usr/share/seclists/Discovery/Web-Content/common.txt"),
        Path("/usr/share/wordlists/dirb/common.txt"),
    ]
    wordlist = next((p for p in wordlist_candidates if p.exists()), None)

    if command_exists("ffuf") and wordlist and base_urls:
        for base in base_urls[:5]:
            if not url_in_scope(base, target):
                continue
            url = base.rstrip("/") + "/FUZZ"
            rc, out, err = run_command(
                [
                    "ffuf", "-u", url, "-w", str(wordlist),
                    "-mc", "200,204,301,302,307,308,401,403",
                    "-s", "-t", "5",
                ],
                timeout=300,
            )
            findings.extend(out.splitlines())

    write_lines(workspace / "content" / "ffuf_results.txt", findings)
    UI.success(f"Content discovery complete: {len(findings)} result lines.")
    return {"content_results": findings}


def make_finding(
    finding_type: str,
    severity: str,
    confidence: str,
    target: str,
    url: str = "",
    source: str = "AxionR",
    status: str = "candidate",
    evidence: str = "",
    description: str = "",
) -> Dict[str, Any]:
    key = f"{finding_type}|{severity}|{target}|{url}|{source}|{evidence}"
    fid = hashlib.sha256(key.encode()).hexdigest()[:12]
    return {
        "id": fid,
        "type": finding_type,
        "severity": severity.upper(),
        "confidence": confidence.upper(),
        "status": status.upper(),
        "target": target,
        "url": url,
        "source": source,
        "evidence": evidence[:4000],
        "description": description,
        "timestamp": now_iso(),
    }


def parse_nuclei_findings(raw: str, target: str) -> List[Dict[str, Any]]:
    results = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            info = obj.get("info", {})
            sev = str(info.get("severity", "info")).lower()
            if sev not in {"critical", "high", "medium", "low", "info", "informational"}:
                sev = "info"
            matched = obj.get("matched-at") or obj.get("host") or ""
            if matched and not url_in_scope(matched, target):
                continue
            results.append(
                make_finding(
                    finding_type=info.get("name", obj.get("template-id", "Nuclei finding")),
                    severity="informational" if sev == "informational" else sev,
                    confidence="high",
                    target=target,
                    url=matched,
                    source="nuclei",
                    status="reported",
                    evidence=json.dumps(obj, ensure_ascii=False)[:4000],
                    description=str(info.get("description", "")),
                )
            )
        except Exception:
            # Keep raw lines as evidence rather than inventing structured severity.
            results.append(
                make_finding(
                    "Nuclei raw result",
                    "info",
                    "low",
                    target,
                    source="nuclei",
                    status="reported",
                    evidence=line,
                )
            )
    return results


def passive_custom_checks(target: str, workspace: Path, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    urls = read_lines(workspace / "urls" / "all_urls.txt")
    requests_mod, _ = import_optional_packages()
    if not requests_mod:
        return findings

    # Low-impact checks: headers and obvious configuration signals only.
    session = requests_mod.Session()
    session.headers.update({"User-Agent": config["user_agent"]})

    checked = 0
    for url in urls[: config["max_urls_for_active_checks"]]:
        if not url_in_scope(url, target):
            continue
        try:
            r = session.get(url, timeout=config["timeouts"]["http"], allow_redirects=False)
            checked += 1
            h = {k.lower(): v for k, v in r.headers.items()}

            if urllib.parse.urlparse(url).scheme == "https" and "strict-transport-security" not in h:
                findings.append(
                    make_finding(
                        "Missing HSTS",
                        "low",
                        "medium",
                        target,
                        url,
                        "AxionR-Headers",
                        "candidate",
                        "Strict-Transport-Security header not observed.",
                        "The endpoint did not return an HSTS header in this response.",
                    )
                )

            if "content-security-policy" not in h:
                findings.append(
                    make_finding(
                        "Missing Content-Security-Policy",
                        "low",
                        "medium",
                        target,
                        url,
                        "AxionR-Headers",
                        "candidate",
                        "Content-Security-Policy header not observed.",
                        "CSP was not observed in this response; absence alone does not prove exploitability.",
                    )
                )

            if "x-content-type-options" not in h:
                findings.append(
                    make_finding(
                        "Missing X-Content-Type-Options",
                        "info",
                        "medium",
                        target,
                        url,
                        "AxionR-Headers",
                        "candidate",
                        "X-Content-Type-Options header not observed.",
                        "The response did not expose this common browser hardening header.",
                    )
                )

            server = h.get("server")
            if server:
                findings.append(
                    make_finding(
                        "Server Header Disclosure",
                        "info",
                        "high",
                        target,
                        url,
                        "AxionR-Headers",
                        "observed",
                        f"Server: {server}",
                        "The response discloses a server banner.",
                    )
                )

            # Safe redirect observation. Do not label as open redirect unless the
            # redirect target is attacker-controlled and actually verified.
            loc = h.get("location")
            if loc:
                absolute = urllib.parse.urljoin(url, loc)
                if urllib.parse.urlparse(absolute).hostname and not url_in_scope(absolute, target):
                    findings.append(
                        make_finding(
                            "External Redirect Observation",
                            "info",
                            "high",
                            target,
                            url,
                            "AxionR-Redirect",
                            "observed",
                            f"Location: {absolute}",
                            "An external redirect was observed from the endpoint. This is not automatically an open redirect.",
                        )
                    )

        except Exception:
            continue

    write_text(workspace / "findings" / "header_check_count.txt", str(checked))
    return findings


def run_security_assessment(target: str, workspace: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    UI.section("09", "SECURITY ASSESSMENT", "Low-impact authorized assessment and scanner correlation")
    findings: List[Dict[str, Any]] = []
    urls = read_lines(workspace / "urls" / "all_urls.txt")
    live_urls = read_lines(workspace / "web" / "live_urls.txt") or [f"https://{target}"]

    # Nuclei: use discovered in-scope URLs only.
    if command_exists("nuclei") and urls:
        target_file = workspace / "scans" / "nuclei_targets.txt"
        write_lines(target_file, urls[:500])
        rc, out, err, _ = execute_tool(
            workspace, "scans", "nuclei.jsonl",
            [
                "nuclei", "-l", str(target_file),
                "-jsonl", "-silent",
                "-severity", "info,low,medium,high,critical",
                "-rate-limit", "5",
                "-bulk-size", "5",
                "-concurrency", "5",
            ],
            max(600, config["timeouts"]["command"]),
        )
        findings.extend(parse_nuclei_findings(out, target))

    # Dalfox: only against URLs already discovered and in scope.
    if command_exists("dalfox") and urls:
        target_file = workspace / "scans" / "dalfox_targets.txt"
        write_lines(target_file, [u for u in urls if "?" in u][:100])
        if read_lines(target_file):
            rc, out, err, _ = execute_tool(
                workspace, "scans", "dalfox.txt",
                ["dalfox", "file", str(target_file), "--silence"],
                max(600, config["timeouts"]["command"]),
            )
            # Preserve output as evidence; don't invent severity from text.
            for line in out.splitlines():
                if line.strip():
                    findings.append(
                        make_finding(
                            "Dalfox reported result",
                            "medium",
                            "low",
                            target,
                            source="dalfox",
                            status="reported",
                            evidence=line,
                            description="Preserved scanner output requiring manual validation.",
                        )
                    )

    # SQLMap is intentionally not auto-run against arbitrary discovered URLs.
    # It is high-impact compared with passive checks and should be explicitly
    # invoked by the tester after scope review.
    write_text(
        workspace / "scans" / "sqlmap_notice.txt",
        "SQLMap is detected by AxionR but is not automatically launched. "
        "Review scope and manually select a test URL/parameter before using SQLMap.\n",
    )

    findings.extend(passive_custom_checks(target, workspace, config))
    write_text(workspace / "findings" / "raw_count.txt", str(len(findings)))

    UI.success(f"Security assessment complete: {len(findings)} observations/findings collected.")
    return {"findings": findings}


def deduplicate_findings(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    result = []
    severity_rank = {"CRITICAL": 5, "HIGH": 4, "MEDIUM": 3, "LOW": 2, "INFO": 1, "INFORMATIONAL": 1}
    for f in findings:
        key = (
            f.get("type", "").lower(),
            f.get("url", "").lower(),
            f.get("source", "").lower(),
        )
        if key in seen:
            continue
        seen.add(key)
        result.append(f)

    result.sort(
        key=lambda x: severity_rank.get(str(x.get("severity", "")).upper(), 0),
        reverse=True,
    )
    return result


def run_finding_analysis(target: str, workspace: Path, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    UI.section("10", "FINDING ANALYSIS", "Normalize • deduplicate • classify • preserve confidence")
    normalized = deduplicate_findings(findings)

    for f in normalized:
        if f.get("status") == "CONFIRMED":
            continue
        # Scanner output is not independently confirmed by AxionR.
        if f.get("source") in {"nuclei", "dalfox"} and f.get("status") == "REPORTED":
            f["confidence"] = "REQUIRES VALIDATION"

    write_text(
        workspace / "findings" / "findings.json",
        json.dumps(normalized, indent=2, ensure_ascii=False),
    )
    return normalized


def severity_counts(findings: List[Dict[str, Any]]) -> Dict[str, int]:
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        sev = str(f.get("severity", "info")).lower()
        if sev == "informational":
            sev = "info"
        counts[sev if sev in counts else "info"] += 1
    return counts


def generate_html_report(
    target: str,
    mode: str,
    workspace: Path,
    findings: List[Dict[str, Any]],
    stats: Dict[str, Any],
) -> Path:
    report = workspace / "reports" / "axionr_report.html"
    rows = []
    for f in findings:
        rows.append(
            "<tr>"
            f"<td><code>{html.escape(str(f.get('id','')))}</code></td>"
            f"<td>{html.escape(str(f.get('severity','')))}</td>"
            f"<td>{html.escape(str(f.get('type','')))}</td>"
            f"<td>{html.escape(str(f.get('confidence','')))}</td>"
            f"<td>{html.escape(str(f.get('status','')))}</td>"
            f"<td>{html.escape(str(f.get('url','')))}</td>"
            f"<td>{html.escape(str(f.get('source','')))}</td>"
            "</tr>"
        )

    generated = now_iso()
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AxionR Security Assessment - {html.escape(target)}</title>
<style>
:root {{
 --bg:#0b0f14; --surface:#111820; --surface2:#16202b; --primary:#3b82f6;
 --cyan:#06b6d4; --text:#e5e7eb; --muted:#94a3b8; --danger:#ef4444;
 --warning:#f59e0b; --success:#22c55e; --border:#243244;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);font:14px/1.55 Inter,system-ui,Segoe UI,Arial,sans-serif}}
.container{{max-width:1250px;margin:auto;padding:32px}}
.hero{{background:linear-gradient(135deg,#101722,#0d151e);border:1px solid var(--border);
 border-radius:18px;padding:30px;position:relative;overflow:hidden}}
.hero:after{{content:"";position:absolute;inset:auto -10% -70% 30%;height:240px;
 background:radial-gradient(circle,rgba(59,130,246,.20),transparent 60%)}}
.logo{{font-weight:800;letter-spacing:4px;color:var(--cyan);font-size:30px}}
.tag{{color:var(--muted);margin-top:5px}}
.meta{{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}}
.badge{{padding:7px 11px;border:1px solid var(--border);border-radius:999px;background:var(--surface2);color:var(--muted)}}
.grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:18px 0}}
.card{{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:18px}}
.card .n{{font-size:27px;font-weight:800;color:var(--text)}}
.card .l{{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:1px}}
section{{margin-top:24px;background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:22px}}
h2{{font-size:16px;letter-spacing:1px}}
table{{width:100%;border-collapse:collapse}}
th,td{{padding:11px 10px;border-bottom:1px solid var(--border);text-align:left;vertical-align:top}}
th{{color:var(--muted);font-size:12px;text-transform:uppercase}}
code{{color:var(--cyan);word-break:break-all}}
.footer{{color:var(--muted);margin-top:24px;font-size:12px}}
@media(max-width:900px){{.grid{{grid-template-columns:repeat(2,1fr)}}.container{{padding:16px}}}}
</style>
</head>
<body>
<div class="container">
<div class="hero">
<div class="logo">AXIONR</div>
<div class="tag">Web Security Reconnaissance &amp; Assessment Framework</div>
<div class="meta">
<div class="badge">Target: {html.escape(target)}</div>
<div class="badge">Mode: {html.escape(mode.upper())}</div>
<div class="badge">Generated: {html.escape(generated)}</div>
<div class="badge">Authorized testing only</div>
</div>
</div>

<div class="grid">
<div class="card"><div class="n">{stats['assets']}</div><div class="l">Assets</div></div>
<div class="card"><div class="n">{stats['urls']}</div><div class="l">URLs</div></div>
<div class="card"><div class="n">{stats['findings']}</div><div class="l">Findings</div></div>
<div class="card"><div class="n">{stats['critical']}</div><div class="l">Critical</div></div>
<div class="card"><div class="n">{stats['high']}</div><div class="l">High</div></div>
</div>

<section>
<h2>SECURITY FINDINGS</h2>
<table>
<thead><tr><th>ID</th><th>Severity</th><th>Type</th><th>Confidence</th><th>Status</th><th>URL</th><th>Source</th></tr></thead>
<tbody>
{''.join(rows) if rows else '<tr><td colspan="7">No structured findings were collected.</td></tr>'}
</tbody>
</table>
</section>

<section>
<h2>ASSESSMENT NOTES</h2>
<p>Scanner-reported observations may require manual validation. Candidate observations are not equivalent to confirmed vulnerabilities.</p>
<p>Review the generated evidence and tool output before making remediation decisions.</p>
</section>

<div class="footer">Generated by AxionR v{VERSION}. Run only against authorized targets.</div>
</div>
</body>
</html>"""
    write_text(report, page)
    return report


def generate_reports(
    target: str,
    mode: str,
    workspace: Path,
    findings: List[Dict[str, Any]],
    state: Dict[str, Any],
) -> Dict[str, Any]:
    UI.section("12", "REPORTING", "Security assessment report generation")
    counts = severity_counts(findings)
    stats = {
        "target": target,
        "mode": mode,
        "assets": len(read_lines(workspace / "assets" / "all_hosts.txt")),
        "urls": len(read_lines(workspace / "urls" / "all_urls.txt")),
        "findings": len(findings),
        **counts,
    }

    summary = {
        "axionr_version": VERSION,
        "generated_at": now_iso(),
        "target": target,
        "mode": mode,
        "stats": stats,
        "workspace": str(workspace),
        "findings": findings,
        "state": state,
    }

    json_path = workspace / "reports" / "axionr_report.json"
    write_text(json_path, json.dumps(summary, indent=2, ensure_ascii=False))
    html_path = generate_html_report(target, mode, workspace, findings, stats)

    # Lightweight text summary for terminal/report portability.
    txt_path = workspace / "reports" / "summary.txt"
    text = (
        f"AxionR Security Assessment\n"
        f"Target: {target}\n"
        f"Mode: {mode.upper()}\n"
        f"Generated: {summary['generated_at']}\n\n"
        f"Assets: {stats['assets']}\n"
        f"URLs: {stats['urls']}\n"
        f"Findings: {stats['findings']}\n"
        f"Critical: {stats['critical']}\n"
        f"High: {stats['high']}\n"
        f"Medium: {stats['medium']}\n"
        f"Low: {stats['low']}\n"
        f"Informational: {stats['info']}\n"
    )
    write_text(txt_path, text)

    UI.success("HTML report generated.")
    UI.success("JSON report generated.")
    UI.success("Text summary generated.")
    return {"stats": stats, "html": html_path, "json": json_path, "text": txt_path}


def choose_mode() -> str:
    UI.menu()
    while True:
        choice = input("\n  Select mode [0-9]: ").strip().lower()
        mapping = {
            "1": "full", "2": "recon", "3": "bugbounty", "4": "ctf",
            "5": "ejpt", "6": "oscp", "7": "audit", "8": "quick",
            "9": "custom", "0": "exit",
        }
        if choice in mapping:
            return mapping[choice]
        print("  Invalid selection.")


def choose_custom_phases() -> List[str]:
    UI.info("Available phases:")
    for idx, (key, title, desc) in enumerate(PHASES, 1):
        print(f"    {idx:02d}. {title:<22} {desc}")
    raw = input("  Enter phase numbers separated by commas (blank = all): ").strip()
    if not raw:
        return [p[0] for p in PHASES]
    selected = []
    for item in raw.split(","):
        try:
            idx = int(item.strip()) - 1
            if 0 <= idx < len(PHASES):
                selected.append(PHASES[idx][0])
        except ValueError:
            pass
    return selected or [p[0] for p in PHASES]


def save_state(workspace: Path, state: Dict[str, Any]) -> None:
    write_text(workspace / "status.json", json.dumps(state, indent=2, ensure_ascii=False))


def load_state(workspace: Path) -> Dict[str, Any]:
    path = workspace / "status.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def run_assessment(
    target: str,
    mode: str,
    no_install: bool = False,
    no_animation: bool = False,
    resume: bool = True,
    custom_phases: Optional[List[str]] = None,
) -> int:
    ensure_dirs()
    config = load_config()

    workspace = create_workspace(target)
    scope_file = ensure_scope(workspace, target)
    state = load_state(workspace)

    UI.warning("AUTHORIZED USE ONLY: verify scope before active testing.")
    UI.status("Target", target, UI.WHITE)
    UI.status("Mode", mode.upper(), UI.BLUE)
    UI.status("Workspace", str(workspace), UI.GREEN)
    UI.status("Scope file", str(scope_file), UI.YELLOW)

    if not no_install:
        setup_dependencies(allow_install=True)
    else:
        UI.info("Automatic dependency installation disabled.")

    phases = custom_phases if custom_phases is not None else MODE_PHASES.get(mode, MODE_PHASES["full"])
    phase_results: Dict[str, Any] = state.get("phase_results", {})
    findings: List[Dict[str, Any]] = state.get("findings", [])

    # Scope checkpoint.
    if "scope" in phases:
        UI.section("02", "SCOPE", "Confirming target and scope file")
        scope_entries = read_lines(scope_file)
        allowed = any(
            entry.lstrip("#").strip() and (
                entry.strip() == target or
                host_in_scope(entry.strip(), target)
            )
            for entry in scope_entries
        )
        if not allowed:
            UI.error("Target is not present in scope.txt.")
            UI.info(f"Open: {scope_file}")
            UI.info(f"Add the authorized target: {target}")
            UI.info("Then run AxionR again.")
            return 2
        UI.success("Target is present in scope.txt.")

    print()
    UI.section("START", "ASSESSMENT ENGINE", f"{len(phases)} phases selected • target: {target}")
    print()
    for idx, phase_key in enumerate(phases, 1):
        if phase_key == "setup":
            phase_results["setup"] = {"completed": True, "timestamp": now_iso()}
            continue
        if phase_key == "scope":
            phase_results["scope"] = {"completed": True, "timestamp": now_iso()}
            continue

        # Resume: skip completed phases except reporting/finding analysis.
        if resume and phase_results.get(phase_key, {}).get("completed"):
            UI.info(f"Skipping completed phase: {phase_key}")
            continue

        try:
            if phase_key == "recon":
                result = run_recon(target, workspace, config)
            elif phase_key == "asset_discovery":
                result = run_asset_discovery(target, workspace, config)
            elif phase_key == "url_discovery":
                result = run_url_discovery(target, workspace, config)
            elif phase_key == "javascript_analysis":
                result = run_javascript_analysis(target, workspace, config)
            elif phase_key == "parameter_discovery":
                result = run_parameter_discovery(target, workspace, config)
            elif phase_key == "content_discovery":
                result = run_content_discovery(target, workspace, config)
            elif phase_key == "security_assessment":
                result = run_security_assessment(target, workspace, config)
                findings.extend(result.get("findings", []))
            elif phase_key == "finding_analysis":
                findings = run_finding_analysis(target, workspace, findings)
                result = {"finding_count": len(findings)}
            elif phase_key == "evidence":
                evidence = {
                    "generated_at": now_iso(),
                    "target": target,
                    "mode": mode,
                    "scope_file": str(scope_file),
                    "python": sys.version,
                    "platform": sys.platform,
                    "tools": collect_tool_status(),
                }
                write_text(workspace / "evidence" / "environment.json", json.dumps(evidence, indent=2))
                result = evidence
            elif phase_key == "reporting":
                reports = generate_reports(target, mode, workspace, findings, state)
                result = {
                    "html": str(reports["html"]),
                    "json": str(reports["json"]),
                    "text": str(reports["text"]),
                }
            else:
                result = {"completed": True}

            phase_results[phase_key] = {
                "completed": True,
                "timestamp": now_iso(),
                "result": result,
            }
            state["phase_results"] = phase_results
            state["findings"] = findings
            save_state(workspace, state)

        except KeyboardInterrupt:
            UI.warning("Interrupted by user. Current checkpoint has been saved.")
            state["phase_results"] = phase_results
            state["findings"] = findings
            save_state(workspace, state)
            return 130
        except Exception as exc:
            UI.error(f"Phase failed: {phase_key}: {exc}")
            phase_results[phase_key] = {
                "completed": False,
                "timestamp": now_iso(),
                "error": str(exc),
            }
            state["phase_results"] = phase_results
            state["findings"] = findings
            save_state(workspace, state)
            return 1

    # Always ensure analysis/reporting exist if selected.
    if "finding_analysis" in phases and findings:
        findings = run_finding_analysis(target, workspace, findings)

    if "reporting" in phases:
        reports = generate_reports(target, mode, workspace, findings, state)
        final_stats = reports["stats"]
    else:
        counts = severity_counts(findings)
        final_stats = {
            "target": target,
            "mode": mode,
            "assets": len(read_lines(workspace / "assets" / "all_hosts.txt")),
            "urls": len(read_lines(workspace / "urls" / "all_urls.txt")),
            "findings": len(findings),
            **counts,
        }

    state["completed_at"] = now_iso()
    state["findings"] = findings
    save_state(workspace, state)

    UI.final_dashboard(final_stats, workspace / "reports")
    return 0


def list_workspaces() -> None:
    ensure_dirs()
    entries = [p for p in WORKSPACE_ROOT.iterdir() if p.is_dir()]
    if not entries:
        print("No workspaces found.")
        return
    print("AxionR Workspaces:")
    for p in sorted(entries):
        state = load_state(p)
        print(f"  • {p.name:<35} {state.get('completed_at', 'in progress / not started')}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} {VERSION} - {TAGLINE}"
    )
    parser.add_argument("target", nargs="?", help="Authorized domain, host or URL")
    parser.add_argument(
        "--mode",
        choices=list(MODE_DESCRIPTIONS.keys()),
        default=None,
        help="Assessment mode",
    )
    parser.add_argument("--setup", action="store_true", help="Check/install dependencies")
    parser.add_argument("--status", action="store_true", help="Show tool status")
    parser.add_argument("--list", action="store_true", help="List target workspaces")
    parser.add_argument("--new", action="store_true", help="Start a new scan by ignoring saved checkpoints")
    parser.add_argument("--no-install", action="store_true", help="Do not install missing dependencies")
    parser.add_argument("--no-animation", action="store_true", help="Disable startup animation")
    parser.add_argument("--no-resume", action="store_true", help="Do not resume completed phases")
    args = parser.parse_args()

    ensure_dirs()

    if args.setup:
        UI.banner(compact=True)
        setup_dependencies(allow_install=True)
        show_tool_status()
        return 0

    if args.status:
        UI.banner(compact=True)
        show_tool_status()
        return 0

    if args.list:
        list_workspaces()
        return 0

    UI.clear()
    UI.banner()
    UI.startup(args.no_animation)
    UI.intro()

    # Easy interactive flow: MODE -> TARGET -> SCOPE -> SCAN.
    mode = args.mode
    if not mode:
        mode = choose_mode()
    if mode == "exit":
        print()
        UI.info("AxionR closed.")
        return 0

    print()
    print(UI.c(f"  Selected mode: {mode.upper()}", UI.BLUE + UI.BOLD))
    print(UI.c(f"  {MODE_DESCRIPTIONS[mode]}", UI.GRAY))
    print()

    target = args.target
    if not target:
        prompt = "Target  > "
        target = input(UI.c(prompt.center(min(shutil.get_terminal_size().columns, 90)), UI.GREEN)).strip()

    try:
        target = normalize_target(target)
    except ValueError as exc:
        UI.error(str(exc))
        return 2

    if not validate_target(target):
        UI.error("Invalid target format.")
        return 2

    print()
    UI.status("Target", target, UI.WHITE)
    UI.status("Mode", mode.upper(), UI.BLUE)
    UI.info("A target workspace and scope.txt will be created automatically.")
    print()

    custom_phases = None
    if mode == "custom":
        custom_phases = choose_custom_phases()

    if args.new:
        workspace = create_workspace(target)
        status_file = workspace / "status.json"
        if status_file.exists():
            status_file.unlink()

    return run_assessment(
        target=target,
        mode=mode,
        no_install=args.no_install,
        no_animation=args.no_animation,
        resume=not (args.new or args.no_resume),
        custom_phases=custom_phases,
    )


if __name__ == "__main__":
    raise SystemExit(main())
