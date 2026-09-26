<div align="center">

⚡ AxionR

Web Security Reconnaissance & Assessment Framework

<p>
  <strong>Reconnaissance • Discovery • Analysis • Evidence • Reporting</strong>
</p>

<!--
  Optional animated hero asset.
  After uploading the asset to your repository, uncomment:
  <img src="assets/axionr-banner.gif" width="100%" alt="AxionR Anime Cybersecurity Banner">
-->

<p>
  <img src="https://img.shields.io/badge/AxionR-v2.0.0-06B6D4?style=for-the-badge&labelColor=0B0F14" alt="AxionR Version">
  <img src="https://img.shields.io/badge/Python-3.x-3B82F6?style=for-the-badge&labelColor=0B0F14" alt="Python">
  <img src="https://img.shields.io/badge/Kali%20Linux-Ready-111820?style=for-the-badge&logo=kalilinux&logoColor=white" alt="Kali Linux">
  <img src="https://img.shields.io/badge/CLI-Security%20Framework-8B5CF6?style=for-the-badge&labelColor=0B0F14" alt="CLI">
</p>

<p>
  <em>A structured security-assessment workflow for authorized testing, labs, CTFs and security research.</em>
</p>

</div>

🛰️ About AxionR

AxionR is a Python-based cybersecurity reconnaissance and web security assessment framework that organizes multiple security tools and analysis stages into a single, repeatable workflow.

The goal is not to replace every specialized security tool. Instead, AxionR acts as an assessment orchestration layer:

                    ┌─────────────────────┐
                    │       TARGET        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   SCOPE VALIDATION  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   RECONNAISSANCE    │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
          DNS / HOSTS       PORTS / WEB      TECHNOLOGIES
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │   URL DISCOVERY     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ JAVASCRIPT ANALYSIS │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ PARAMETER DISCOVERY │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ CONTENT DISCOVERY   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ SECURITY ASSESSMENT │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ FINDING ANALYSIS    │
                    │ Normalize / Dedup    │
                    │ Classify / Correlate │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ EVIDENCE + REPORTS  │
                    └─────────────────────┘

AxionR is designed around a simple principle:

Discover the attack surface → organize evidence → assess security signals → preserve findings → generate a useful report.

🎯 Project Goals

AxionR is designed to make authorized security assessments more structured and repeatable.

Primary goals

Centralize reconnaissance workflows.

Reduce repetitive manual command execution.

Keep each target in a separate workspace.

Validate target scope before assessment stages.

Combine passive and active discovery.

Normalize findings from different tools.

Preserve scanner evidence and execution metadata.

Distinguish observations/candidates from confirmed vulnerabilities.

Generate machine-readable and human-readable reports.

Provide a professional CLI suitable for labs, demonstrations and security research.

Non-goals

AxionR is not intended to:

bypass authorization,

provide unauthorized access,

steal credentials,

maintain persistence,

deploy malware,

perform destructive testing,

hide activity from defenders,

automatically exploit arbitrary targets.

✨ Key Features

🔍 01 — Reconnaissance

AxionR can orchestrate reconnaissance utilities such as:

Subfinder

Amass

GAU

Waybackurls

DNSX

HTTPX

Katana

Hakrawler

Typical output includes:

Domains
Subdomains
Resolved hosts
Historical URLs
Live HTTP services
Technology metadata

🌐 02 — Asset Discovery

The asset-discovery stage helps organize:

domains,

subdomains,

IP addresses,

DNS results,

HTTP/HTTPS services,

ports,

service banners,

technology metadata,

WAF observations.

Network/service tooling may include:

Nmap

Naabu

WhatWeb

Wafw00f

🕷️ 03 — URL Discovery

AxionR can combine URL sources and crawling results.

Sources may include:

Historical archives
Passive URL collection
HTTP probing
Web crawling
Application-discovered URLs

The framework then applies in-scope filtering before using discovered URLs in later stages.

🧩 04 — JavaScript Analysis

AxionR identifies JavaScript resources and performs lightweight analysis for:

JavaScript URL collection,

endpoint candidates,

API-like paths,

suspicious configuration patterns,

token/secret-like strings requiring manual validation.

Important:

A string matching a secret-like pattern is a candidate, not proof that a valid secret exists or is exploitable.

🔎 05 — Parameter Discovery

AxionR can identify URLs containing parameters and integrate parameter-discovery tooling where available.

Example:

https://example.com/search?q=test
                         └── parameter

This information can be used to prioritize later authorized security review.

📂 06 — Content Discovery

AxionR can integrate FFUF and available wordlists for authorized path discovery.

Possible result categories:

200  → accessible resource
301  → redirect
302  → redirect
401  → authentication required
403  → forbidden
404  → not found

Results are preserved for later analysis rather than automatically treated as vulnerabilities.

🛡️ 07 — Security Assessment

AxionR supports integration with security assessment tools including:

Nuclei

Dalfox

SQLMap detection/integration foundation

AxionR custom low-impact checks

Important scanner behavior

Scanner output is preserved as evidence and may require manual validation.

For example:

Scanner output
      ↓
AxionR finding
      ↓
Evidence preserved
      ↓
Manual validation
      ↓
Confirmed finding

AxionR does not automatically treat every scanner result as a confirmed vulnerability.

🧠 Finding Intelligence

AxionR uses a structured finding model.

Example:

{
  "id": "a1b2c3d4e5f6",
  "type": "Missing HSTS",
  "severity": "LOW",
  "confidence": "MEDIUM",
  "status": "CANDIDATE",
  "target": "example.com",
  "url": "https://example.com",
  "source": "AxionR-Headers",
  "evidence": "Strict-Transport-Security header not observed.",
  "timestamp": "2026-01-01T12:00:00+05:30"
}

Severity

CRITICAL
HIGH
MEDIUM
LOW
INFO

Confidence

HIGH
MEDIUM
LOW
REQUIRES VALIDATION

Status

CANDIDATE
OBSERVED
REPORTED
CONFIRMED
INFORMATIONAL

This distinction is important because:

Observation ≠ Vulnerability
Candidate ≠ Confirmed
Scanner output ≠ Independent validation

🎮 Operating Modes

AxionR provides multiple workflows.

Mode

Purpose

FULL

Complete authorized assessment

RECON

Reconnaissance and attack-surface discovery

BUG BOUNTY

Authorized web application assessment

CTF

CTF/lab enumeration

eJPT

Pentesting/lab workflow

OSCP

Authorized lab enumeration

AUDIT

Security/configuration assessment

QUICK

Fast initial triage

CUSTOM

User-selected phase workflow

🧭 Mode Workflows

FULL

Setup
 ↓
Scope
 ↓
Recon
 ↓
Asset Discovery
 ↓
URL Discovery
 ↓
JavaScript Analysis
 ↓
Parameter Discovery
 ↓
Content Discovery
 ↓
Security Assessment
 ↓
Finding Analysis
 ↓
Evidence
 ↓
Reporting

RECON

Setup
 ↓
Scope
 ↓
Recon
 ↓
Asset Discovery
 ↓
URL Discovery
 ↓
Finding Analysis
 ↓
Reporting

QUICK

Setup
 ↓
Scope
 ↓
Asset Discovery
 ↓
Security Assessment
 ↓
Reporting

CUSTOM

The user selects the desired assessment phases.

🧩 Integrated Tool Stack

Recon

Tool

Role

Subfinder

Subdomain discovery

Amass

Asset/subdomain enumeration

GAU

Passive URL discovery

Waybackurls

Historical URL discovery

DNSX

DNS probing

HTTPX

HTTP probing and metadata

Katana

Web crawling

Hakrawler

Web crawling

Network / Web

Tool

Role

Nmap

Port/service enumeration

Naabu

Port discovery

WhatWeb

Technology fingerprinting

Wafw00f

WAF detection

Web Discovery

Tool

Role

FFUF

Content discovery

Arjun

Parameter discovery

SecLists

Wordlists

PayloadsAllTheThings

Security-testing reference payloads

Assessment

Tool

Role

Nuclei

Template-based security checks

Dalfox

XSS assessment

SQLMap

SQL injection assessment

Third-party tools are independently maintained projects. Their availability, CLI behavior and output can vary by installed version.

🖥️ Professional CLI Experience

AxionR uses a consistent dark technical terminal identity.

Example:

                         AxionR

           WEB SECURITY RECONNAISSANCE
              & ASSESSMENT FRAMEWORK

          Recon • Discovery • Analysis
             Evidence • Reporting

      AxionR v2.0.0 • Kali Linux Ready

The interface includes:

centered AxionR branding,

startup animation,

module headers,

status indicators,

progress bars,

scan-state information,

completion dashboard,

warnings and errors,

report paths.

The visual direction is intentionally clean enterprise-security UI, rather than excessive hacker-style effects.

🌌 Anime / Cybersecurity Visual Identity

AxionR can use an anime-inspired cybersecurity visual system for GitHub documentation and project presentation.

Recommended visual language:

Dark SOC Environment
        +
Futuristic Anime Analyst
        +
Cyan / Blue Security UI
        +
Network Nodes
        +
Terminal Data
        +
Subtle Scanning Animation

Suggested assets

assets/
├── axionr-banner.gif
├── axionr-anime.png
├── architecture.png
├── workflow.png
├── terminal-demo.gif
└── screenshots/
    ├── startup.png
    ├── recon.png
    ├── scan.png
    └── report.png

Animated banner

After adding the GIF to the repository:

<p align="center">
  <img
    src="assets/axionr-banner.gif"
    width="100%"
    alt="AxionR Anime Cybersecurity Banner"
  >
</p>

Anime character

<p align="center">
  <img
    src="assets/axionr-anime.png"
    width="700"
    alt="AxionR Anime Cybersecurity Analyst"
  >
</p>

📁 Repository Structure

Recommended GitHub structure:

AxionR/
│
├── axionr.py
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
│
├── assets/
│   ├── axionr-banner.gif
│   ├── axionr-anime.png
│   ├── architecture.png
│   ├── workflow.png
│   ├── terminal-demo.gif
│   └── screenshots/
│       ├── startup.png
│       ├── recon.png
│       ├── scan.png
│       └── report.png
│
├── config/
│   └── config.example.json
│
├── docs/
│   ├── architecture.md
│   └── workflow.md
│
└── wordlists/
    └── README.md

Generated runtime data

The following should generally remain local and should not be committed:

workspace/
logs/
private scan results
credentials
API keys
private target data
temporary files

🚀 Installation

Requirements

Recommended environment:

OS          : Kali Linux / Debian-based Linux
Python      : Python 3.x
Git         : Git
Optional    : Go

Some assessment modules require external tools.

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/AxionR.git
cd AxionR

Replace:

YOUR_USERNAME

with your GitHub username.

2. Check Python

python3 --version

3. Run setup

sudo python3 axionr.py --setup

AxionR checks for missing dependencies and can optionally install supported packages/tools.

4. Check tool status

python3 axionr.py --status

⚡ Quick Start

Interactive mode:

python3 axionr.py

Direct FULL workflow:

python3 axionr.py example.com --mode full

Recon:

python3 axionr.py example.com --mode recon

Quick triage:

python3 axionr.py example.com --mode quick

CTF/lab:

python3 axionr.py example.com --mode ctf

eJPT-style lab:

python3 axionr.py example.com --mode ejpt

OSCP-style authorized lab:

python3 axionr.py example.com --mode oscp

Audit:

python3 axionr.py example.com --mode audit

Custom:

python3 axionr.py example.com --mode custom

Disable automatic installation:

python3 axionr.py example.com --mode recon --no-install

Start a new scan instead of resuming:

python3 axionr.py example.com --mode full --new

🛡️ Scope Management

AxionR creates:

workspace/<target>/scope.txt

Example:

# AxionR authorized scope

example.com

Before active testing:

Verify that you have permission.

Review the scope.

Confirm allowed domains/IPs.

Confirm allowed testing methods.

Confirm rate limits and program rules.

Then start the assessment.

Scope filtering is also used when processing discovered URLs.

🔄 Checkpoint & Resume

AxionR stores state in:

workspace/<target>/status.json

Completed phases can be preserved so a later run can continue without unnecessarily repeating completed workflow stages.

Start completely fresh:

python3 axionr.py example.com --mode full --new

Disable resume behavior:

python3 axionr.py example.com --mode full --no-resume

📦 Workspace Output

For:

example.com

AxionR can create:

workspace/
└── example.com/
    │
    ├── scope.txt
    ├── status.json
    │
    ├── recon/
    │   ├── subfinder.txt
    │   └── amass.txt
    │
    ├── assets/
    │   ├── subdomains.txt
    │   └── all_hosts.txt
    │
    ├── dns/
    │   ├── live_hosts.txt
    │   └── resolved_ips.txt
    │
    ├── ports/
    │   ├── nmap.txt
    │   └── open_services.txt
    │
    ├── web/
    │   ├── httpx_raw.txt
    │   ├── live_urls.txt
    │   └── waf_detection.txt
    │
    ├── urls/
    │   ├── gau.txt
    │   ├── waybackurls.txt
    │   └── all_urls.txt
    │
    ├── javascript/
    │   ├── javascript_urls.txt
    │   └── candidates.txt
    │
    ├── parameters/
    │   └── observed_parameters.txt
    │
    ├── content/
    │   └── ffuf_results.txt
    │
    ├── scans/
    │   ├── nuclei.jsonl
    │   ├── dalfox.txt
    │   └── sqlmap_notice.txt
    │
    ├── findings/
    │   ├── findings.json
    │   └── raw_count.txt
    │
    ├── evidence/
    │   └── environment.json
    │
    ├── logs/
    │   └── commands.jsonl
    │
    └── reports/
        ├── axionr_report.html
        ├── axionr_report.json
        └── summary.txt

📊 Reporting

AxionR produces multiple report formats.

HTML

reports/axionr_report.html

Designed for:

browser viewing,

demonstrations,

project presentations,

assessment review.

JSON

reports/axionr_report.json

Designed for:

automation,

future integrations,

parsing,

data pipelines.

Text

reports/summary.txt

Designed for quick terminal review.

📋 Example Report Summary

AxionR Security Assessment

Target: example.com
Mode: FULL

Assets:       42
URLs:         1,248
Findings:     37

Critical:      0
High:          3
Medium:       11
Low:          12
Informational:11

The actual numbers depend on the authorized target and tools available.

🔬 Assessment Evidence

AxionR preserves evidence from the workflow.

Examples include:

Tool output
HTTP headers
Scanner JSON
Discovered URLs
DNS results
Port/service output
Technology observations
Execution metadata

Command execution metadata is stored in:

logs/commands.jsonl

This helps make the assessment more reproducible.

🧠 Finding Correlation

Multiple tools can report related observations.

AxionR attempts to normalize and deduplicate findings using structured attributes such as:

Finding type
URL
Source
Severity
Evidence

The purpose is to reduce duplicate entries while preserving the original evidence source.

⚠️ Important Finding Philosophy

AxionR deliberately distinguishes:

Potential signal
      ↓
Candidate
      ↓
Scanner-reported observation
      ↓
Manual validation
      ↓
Confirmed vulnerability

A candidate finding should not automatically be presented as an exploitable vulnerability.

This is especially important for:

redirect observations,

missing security headers,

JavaScript secret-like strings,

scanner output,

technology disclosures,

SSRF/IDOR-style candidates.

🧪 Testing Philosophy

When developing or extending AxionR:

Prefer:
✓ Passive discovery
✓ Low-impact validation
✓ Explicit scope
✓ Rate limiting
✓ Evidence preservation
✓ Manual validation

Avoid:
✗ Destructive testing
✗ Unauthorized scanning
✗ Credential theft
✗ Persistence
✗ Malware deployment
✗ Data destruction

🗺️ Roadmap

v2.0.0 Foundation

Single-file Python framework

AxionR branding

Professional CLI

Startup animation

Operating modes

Scope management

Workspace generation

Dependency detection

Recon workflow

Asset discovery

URL discovery

JavaScript analysis foundation

Parameter discovery foundation

Content discovery

Security-tool integration

Finding normalization

Evidence collection

Checkpoint/resume

HTML reporting

JSON reporting

Text summary

Future

Rich interactive terminal dashboard

Expanded finding correlation

CVSS metadata support

More detailed evidence attachments

Configurable scan profiles

Plugin architecture

CI/CD integration

Optional web dashboard

More report templates

Expanded passive intelligence integrations

Better visualization of attack-surface relationships

🎬 Recommended GitHub Demo

A professional project demo should show:

01. AxionR startup
        ↓
02. Mode selection
        ↓
03. Scope confirmation
        ↓
04. Reconnaissance
        ↓
05. Asset discovery
        ↓
06. URL discovery
        ↓
07. Security assessment
        ↓
08. Finding analysis
        ↓
09. Report generation
        ↓
10. HTML report

For GitHub, a short terminal GIF is usually more useful than a long video.

Recommended asset:

assets/terminal-demo.gif

🖼️ Screenshot Gallery

After recording your final UI, add screenshots here.

Startup

![AxionR Startup](assets/screenshots/startup.png)

Recon

![AxionR Recon](assets/screenshots/recon.png)

Security Assessment

![AxionR Scan](assets/screenshots/scan.png)

Report

![AxionR Report](assets/screenshots/report.png)

🌐 GitHub Topics

Recommended repository topics:

cybersecurity
penetration-testing
web-security
reconnaissance
ethical-hacking
bug-bounty
kali-linux
python
red-team
security-tools
vulnerability-scanner
security-research
osint
ctf

🤝 Contributing

Contributions are welcome when they improve legitimate security testing, education, documentation or defensive analysis.

Development guidelines

Keep changes focused.

Preserve scope validation.

Avoid destructive behavior.

Avoid unauthorized-access functionality.

Document new dependencies.

Preserve evidence and reproducibility.

Keep scanner integrations clearly identified.

Do not represent candidates as confirmed vulnerabilities.

Update documentation when behavior changes.

Suggested workflow

git checkout -b feature/your-feature

Then:

git add .
git commit -m "Add: your feature"
git push origin feature/your-feature

Open a pull request after testing.

🐛 Issues

When reporting an issue, include:

AxionR version
Python version
Operating system
Tool version
Command used
Expected behavior
Actual behavior
Relevant error

Do not upload:

API keys
passwords
credentials
private target data
personal information
confidential assessment results

🔐 Responsible Use

AxionR is intended for:

authorized penetration testing,

cybersecurity education,

CTFs,

controlled laboratories,

bug bounty programs where testing is explicitly allowed,

security research with permission,

defensive assessment.

Do not run AxionR against systems you do not own or have explicit permission to assess.

Users are responsible for complying with applicable laws, contracts, program rules and authorization boundaries.

⚖️ Legal & Safety Notice

AxionR is a security-assessment framework.

The project does not grant permission to test any target.

Third-party security tools integrated by AxionR have their own licenses, terms and usage requirements. Review those requirements before using them.

The authors and contributors are not responsible for unauthorized, illegal, destructive or abusive use of the software.

Always establish authorization and scope before running active assessment modules.

📜 License

Choose and add an appropriate open-source license before publishing the repository.

For example:

LICENSE

If the repository is later released under MIT, replace this section with the official MIT license notice and add the corresponding LICENSE file.

👨‍💻 Author

<div align="center">

AxionR

Web Security Reconnaissance & Assessment Framework

Built as a cybersecurity learning, research and authorized-assessment project.

</div>

⭐ Support

If AxionR is useful for your cybersecurity learning or authorized assessment workflows:

⭐ Star the repository
🐛 Report reproducible bugs
💡 Suggest improvements
🤝 Contribute responsibly
📚 Improve documentation

<div align="center">

⚡ AxionR

Recon • Discover • Analyze • Validate • Report

v2.0.0

Built for authorized security testing.

</div>
