<div align="center">

⚡ AxionR

Web Security Reconnaissance & Assessment Framework

Reconnaissance · Discovery · Analysis · Evidence · Reporting

<p>
  <img src="https://img.shields.io/badge/AxionR-v2.0.0-06B6D4?style=for-the-badge&labelColor=0B0F14" alt="AxionR v2.0.0">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.x">
  <img src="https://img.shields.io/badge/Kali%20Linux-Ready-111820?style=for-the-badge&logo=kalilinux&logoColor=white" alt="Kali Linux Ready">
  <img src="https://img.shields.io/badge/CLI-Security%20Framework-7C3AED?style=for-the-badge&labelColor=0B0F14" alt="CLI Security Framework">
  <img src="https://img.shields.io/badge/License-Apache--2.0-D22128?style=for-the-badge&labelColor=0B0F14" alt="Apache 2.0 License">
</p>

<p>
  <em>A structured security-assessment workflow for authorized testing, labs, CTFs, and security research.</em>
</p>

</div>

🛰️ Overview

AxionR is a Python-based cybersecurity reconnaissance and web security assessment framework that organizes multiple security tools and assessment stages into a single, repeatable workflow.

AxionR acts as an assessment orchestration layer rather than trying to replace every specialized security utility. It coordinates:

scope validation;

reconnaissance;

asset discovery;

web and service discovery;

URL collection and normalization;

JavaScript and parameter analysis;

content discovery;

security-tool integration;

finding normalization and deduplication;

evidence collection;

structured reporting.

Discover the attack surface → organize evidence → assess security signals → preserve findings → generate a useful report.

🏗️ Assessment Architecture

flowchart TD
    A[Authorized Target] --> B[Scope Validation]
    B --> C[Reconnaissance]

    C --> D[Asset Discovery]
    C --> E[DNS / Host Discovery]
    C --> F[Ports / Services]
    C --> G[Web / Technology Discovery]

    D --> H[URL Discovery]
    E --> H
    F --> H
    G --> H

    H --> I[JavaScript Analysis]
    I --> J[Parameter Discovery]
    J --> K[Content Discovery]
    K --> L[Security Assessment]

    L --> M[Finding Normalization]
    M --> N[Deduplication & Correlation]
    N --> O[Evidence Collection]
    O --> P[Reports]

    P --> P1[HTML]
    P --> P2[JSON]
    P --> P3[TXT]

🎯 Project Goals

AxionR is designed to make authorized security assessments more structured, repeatable, and easier to review.

Primary goals

Centralize reconnaissance workflows.

Reduce repetitive manual command execution.

Maintain a separate workspace for each target.

Validate scope before assessment stages.

Combine passive and active discovery.

Normalize findings from multiple tools.

Preserve scanner evidence and execution metadata.

Distinguish observations/candidates from confirmed vulnerabilities.

Generate machine-readable and human-readable reports.

Provide a professional CLI for labs, demonstrations, and security research.

Non-goals

AxionR is not intended to:

bypass authorization;

provide unauthorized access;

steal credentials;

maintain persistence;

deploy malware;

perform destructive testing;

hide activity from defenders;

automatically exploit arbitrary targets.

✨ Features

🔍 01 — Reconnaissance

AxionR can orchestrate reconnaissance utilities including:

Tool

Purpose

Subfinder

Subdomain discovery

Amass

Asset and subdomain enumeration

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

Typical outputs include domains, subdomains, resolved hosts, historical URLs, live HTTP services, and technology metadata.

🌐 02 — Asset Discovery

The asset-discovery stage can organize:

domains;

subdomains;

IP addresses;

DNS results;

HTTP/HTTPS services;

ports;

service information;

technology metadata;

WAF observations.

Tool

Purpose

Nmap

Port and service enumeration

Naabu

Port discovery

WhatWeb

Technology fingerprinting

Wafw00f

WAF detection

🕷️ 03 — URL Discovery

AxionR can combine URL sources and crawling results from:

GAU;

Waybackurls;

Katana;

Hakrawler;

HTTP probing;

application-discovered URLs.

The processing pipeline is:

URL Sources
    ↓
Normalization
    ↓
Deduplication
    ↓
Scope Filtering
    ↓
In-Scope URL Set

🧩 04 — JavaScript Analysis

AxionR performs lightweight JavaScript analysis for:

JavaScript URL collection;

endpoint candidates;

API-like paths;

configuration patterns;

token/secret-like strings requiring validation.

Important: A secret-like string or endpoint pattern is a candidate, not proof of a valid credential, vulnerability, or exploitability.

🔎 05 — Parameter Discovery

AxionR can identify URLs containing parameters and integrate parameter-discovery tooling where available.

Example:

https://example.com/search?q=test
                         └── q

Parameter information can be used to prioritize later authorized security review.

📂 06 — Content Discovery

AxionR can integrate FFUF and available wordlists for authorized path discovery.

Status

Meaning

200

Accessible resource

301

Redirect

302

Redirect

401

Authentication required

403

Forbidden

404

Not found

A discovered path is an observation. It is not automatically a vulnerability.

🛡️ 07 — Security Assessment

AxionR supports security-assessment integrations including:

Nuclei

Dalfox

SQLMap integration/detection foundation

AxionR custom low-impact checks

Validation model

Scanner Output
      ↓
AxionR Parser
      ↓
Structured Finding
      ↓
Evidence
      ↓
Manual Validation
      ↓
Confirmed Finding

Scanner output is preserved as evidence and should not automatically be treated as a confirmed vulnerability.

🧠 Finding Intelligence

AxionR uses a structured finding model so results from different sources can be normalized and reviewed consistently.

Example finding

{
  "id": "a1b2c3d4",
  "type": "Missing HSTS",
  "severity": "LOW",
  "confidence": "MEDIUM",
  "status": "CANDIDATE",
  "target": "example.com",
  "url": "https://example.com",
  "source": "AxionR-Headers",
  "evidence": "Strict-Transport-Security header not observed."
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

The distinction is intentional:

Observation    ≠ Vulnerability
Candidate      ≠ Confirmed
Scanner output ≠ Independent validation

🎮 Operating Modes

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

User-selected workflow

FULL workflow

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

RECON workflow

Setup → Scope → Recon → Assets → URLs → Analysis → Reporting

QUICK workflow

Setup → Scope → Assets → Security Assessment → Reporting

CUSTOM workflow

Select the assessment phases required for the authorized engagement.

🧩 Integrated Tool Stack

Reconnaissance

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

Network & Web

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

Security Assessment

Tool

Role

Nuclei

Template-based security checks

Dalfox

XSS assessment

SQLMap

SQL injection assessment

Third-party tools are independently maintained projects. Their versions, installation requirements, CLI behavior, output formats, and licenses may vary.

🖥️ CLI Experience

AxionR uses a dark, technical terminal identity designed to remain professional rather than relying on excessive hacker-style effects.

Example:

                         AXIONR

           WEB SECURITY RECONNAISSANCE
              & ASSESSMENT FRAMEWORK

          Recon • Discovery • Analysis
             Evidence • Reporting

      AxionR v2.0.0 • Kali Linux Ready

The interface includes:

centered AxionR branding;

startup animation;

module headers;

status indicators;

progress information;

scan-state information;

completion summary;

warnings and errors;

report paths.

🌌 Anime / Cybersecurity Visual Identity

AxionR uses an anime-inspired cyber-security visual direction for project presentation and GitHub branding.

Visual language

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

Optional assets

If these files are added to the repository, they can be displayed in the README:

assets/
├── axionr-banner.gif
├── axionr-anime.png
├── architecture.png
├── workflow.png
└── terminal-demo.gif

Example:

<p align="center">
  <img src="assets/axionr-banner.gif" width="100%" alt="AxionR Anime Cybersecurity Banner">
</p>

Do not add the image tag until the actual file exists. This prevents broken-image icons on GitHub.

📁 Repository Structure

Keep the repository itself clean and separate from generated assessment data:

AxionR/
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
│   └── terminal-demo.gif
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

workspace/ and private runtime output should remain outside the public repository and be ignored by Git.

🚀 Installation

Requirements

Recommended environment:

OS       : Kali Linux / Debian-based Linux
Python   : Python 3.x
Git      : Git
Optional : Go

Some assessment modules require additional external tools.

1. Clone

git clone https://github.com/TocsiVector/AxionR.git
cd AxionR

2. Check Python

python3 --version

3. Setup

sudo python3 axionr.py --setup

4. Check tool availability

python3 axionr.py --status

⚡ Quick Start

Interactive mode

python3 axionr.py

FULL

python3 axionr.py example.com --mode full

RECON

python3 axionr.py example.com --mode recon

QUICK

python3 axionr.py example.com --mode quick

CTF / lab

python3 axionr.py example.com --mode ctf

eJPT-style lab

python3 axionr.py example.com --mode ejpt

OSCP-style authorized lab

python3 axionr.py example.com --mode oscp

AUDIT

python3 axionr.py example.com --mode audit

CUSTOM

python3 axionr.py example.com --mode custom

Disable automatic installation

python3 axionr.py example.com --mode recon --no-install

Start a fresh assessment

python3 axionr.py example.com --mode full --new

🛡️ Scope Management

AxionR maintains a target-specific scope:

workspace/<target>/scope.txt

Example:

# AxionR Authorized Scope

example.com
*.example.com

Before active assessment:

Verify authorization.

Review the scope.

Confirm allowed domains/IPs.

Confirm permitted testing methods.

Confirm applicable rate limits and program rules.

Start the assessment only after the authorization boundary is clear.

🔄 Checkpoint & Resume

AxionR stores workflow state in:

workspace/<target>/status.json

This allows completed phases to be preserved so a later run can continue without unnecessarily repeating completed workflow stages.

Start fresh

python3 axionr.py example.com --mode full --new

Disable resume

python3 axionr.py example.com --mode full --no-resume

📦 Workspace Output

AxionR maintains a separate workspace for each target.

For:

example.com

the logical workspace is:

workspace/
└── example.com/
    ├── scope.txt
    ├── status.json
    │
    ├── recon/
    ├── assets/
    ├── dns/
    ├── ports/
    ├── web/
    ├── urls/
    ├── javascript/
    ├── parameters/
    ├── content/
    ├── scans/
    ├── findings/
    ├── evidence/
    ├── logs/
    └── reports/

This compact view is intentional: it prevents the README from becoming an extremely wide, difficult-to-read file tree.

Directory responsibilities

Directory

Purpose

recon/

Raw and processed reconnaissance results

assets/

Consolidated hosts, subdomains, IPs, and technologies

dns/

DNS records and resolution results

ports/

Port and service enumeration

web/

HTTP probing, technologies, status, and WAF observations

urls/

Collected, normalized, deduplicated, in-scope URLs

javascript/

JavaScript resources and analysis candidates

parameters/

Observed and discovered parameters

content/

Content/path discovery results

scans/

Security-tool output

findings/

Normalized, deduplicated security findings

evidence/

Supporting evidence and assessment metadata

logs/

Commands, execution history, and errors

reports/

Final HTML, JSON, and text reports

Example detailed workspace

example.com/
├── scope.txt
├── status.json
│
├── recon/
│   ├── subfinder.txt
│   ├── amass.txt
│   ├── gau.txt
│   └── waybackurls.txt
│
├── assets/
│   ├── subdomains.txt
│   ├── all_hosts.txt
│   └── live_hosts.txt
│
├── dns/
│   ├── dns_records.txt
│   └── resolved_ips.txt
│
├── ports/
│   ├── nmap.txt
│   ├── naabu.txt
│   └── open_ports.txt
│
├── web/
│   ├── httpx_raw.txt
│   ├── live_urls.txt
│   └── waf_detection.txt
│
├── urls/
│   ├── all_urls.txt
│   └── in_scope_urls.txt
│
├── javascript/
│   ├── javascript_urls.txt
│   ├── endpoints.txt
│   └── candidates.txt
│
├── parameters/
│   ├── observed_parameters.txt
│   └── arjun_results.txt
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
│   └── findings_deduplicated.json
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

Workspace data flow

flowchart LR
    A[Target] --> B[Scope]
    B --> C[Recon]
    C --> D[Assets]
    D --> E[URLs]
    E --> F[JS / Parameters / Content]
    F --> G[Security Assessment]
    G --> H[Normalize]
    H --> I[Deduplicate]
    I --> J[Evidence]
    J --> K[Reports]

    K --> K1[HTML]
    K --> K2[JSON]
    K --> K3[TXT]

Target isolation

Each target receives its own workspace:

workspace/
├── example.com/
├── test.lab/
└── lab.local/

This keeps data from different assessments separated at the workspace level.

The exact files created can vary depending on the selected mode, installed tools, scope, configuration, and successful execution of individual phases. The structure above describes the logical AxionR workspace architecture.

📊 Reporting

AxionR produces multiple report formats:

Format

File

Purpose

HTML

reports/axionr_report.html

Browser viewing, demonstrations, and assessment review

JSON

reports/axionr_report.json

Automation, parsing, and integrations

TXT

reports/summary.txt

Quick terminal review

Example

AxionR Security Assessment

Target:   example.com
Mode:     FULL

Assets:   42
URLs:     1,248
Findings: 37

Critical:        0
High:            3
Medium:         11
Low:            12
Informational:  11

Example numbers are illustrative. Actual results depend on the authorized target, scope, configuration, and available tools.

🔬 Evidence Collection

AxionR preserves supporting information generated during the workflow.

Examples include:

tool output;

HTTP headers;

scanner output;

discovered URLs;

DNS results;

port/service information;

technology observations;

execution metadata.

Command execution metadata is stored in:

logs/commands.jsonl

This helps make assessment results more reviewable and reproducible.

🧠 Finding Correlation & Deduplication

Multiple tools can report related observations.

AxionR can normalize and deduplicate findings using structured attributes such as:

Finding type
URL
Source
Severity
Evidence

The goal is to reduce duplicate entries while retaining the underlying evidence source.

⚠️ Finding Validation Philosophy

AxionR deliberately separates potential signals from validated findings:

Potential Signal
      ↓
Candidate
      ↓
Scanner Observation
      ↓
Manual Validation
      ↓
Confirmed Finding

This distinction is particularly important for:

redirect observations;

missing security headers;

JavaScript secret-like strings;

scanner output;

technology disclosures;

SSRF/IDOR-style candidates.

🧪 Testing Philosophy

Prefer

✓ Passive discovery
✓ Low-impact validation
✓ Explicit scope
✓ Rate limiting
✓ Evidence preservation
✓ Manual validation

Avoid

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

Future development

Rich interactive terminal dashboard

Expanded finding correlation

CVSS metadata support

More detailed evidence attachments

Configurable scan profiles

Plugin architecture

CI/CD integration

Optional web dashboard

More report templates

Expanded passive-intelligence integrations

Attack-surface relationship visualization

🎬 GitHub Demo

A concise project demo should show:

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

Recommended asset:

assets/terminal-demo.gif

Only reference the GIF after the actual file has been uploaded.

🖼️ Screenshots

Once screenshots are added to the repository:

assets/screenshots/
├── startup.png
├── recon.png
├── scan.png
└── report.png

Use:

![AxionR Startup](assets/screenshots/startup.png)
![AxionR Recon](assets/screenshots/recon.png)
![AxionR Scan](assets/screenshots/scan.png)
![AxionR Report](assets/screenshots/report.png)

🌐 Suggested GitHub Topics

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

Contributions are welcome when they improve legitimate security testing, education, documentation, or defensive analysis.

Guidelines

Keep changes focused.

Preserve scope validation.

Avoid destructive behavior.

Avoid unauthorized-access functionality.

Document new dependencies.

Preserve evidence and reproducibility.

Clearly identify third-party scanner integrations.

Do not represent candidates as confirmed vulnerabilities.

Update documentation when behavior changes.

Development workflow

git checkout -b feature/your-feature
git add .
git commit -m "Add: your feature"
git push origin feature/your-feature

Then open a pull request after testing.

🐛 Reporting Issues

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

authorized penetration testing;

cybersecurity education;

CTFs;

controlled laboratories;

bug bounty programs where testing is explicitly permitted;

security research with permission;

defensive assessment.

Do not run AxionR against systems you do not own or have explicit permission to assess.

Users are responsible for complying with applicable laws, contracts, program rules, and authorization boundaries.

⚖️ Legal & Safety Notice

AxionR is a security-assessment framework.

The project itself does not grant permission to test any target.

Third-party security tools integrated by AxionR have their own licenses, terms, and usage requirements. Review those requirements before use.

The authors and contributors are not responsible for unauthorized, illegal, destructive, or abusive use of the software.

Always establish authorization and scope before running active assessment modules.

📜 License

AxionR is released under the Apache License 2.0.

See the repository's LICENSE file for the complete license text.

👨‍💻 Project

<div align="center">

⚡ AxionR

Web Security Reconnaissance & Assessment Framework

Built as a cybersecurity learning, research, and authorized-assessment project.

<br>

Recon · Discover · Analyze · Validate · Report

<br>

v2.0.0

<sub>Built for authorized security testing.</sub>

</div>
