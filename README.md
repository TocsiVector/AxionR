<div align="center">

⚡ AxionR

Web Security Reconnaissance & Assessment Framework

Reconnaissance • Discovery • Analysis • Evidence • Reporting

<p>
  <img src="https://img.shields.io/badge/AxionR-v2.0.0-06B6D4?style=for-the-badge&labelColor=0B0F14" alt="AxionR v2.0.0">
  <img src="https://img.shields.io/badge/Python-3.x-3B82F6?style=for-the-badge&labelColor=0B0F14" alt="Python 3.x">
  <img src="https://img.shields.io/badge/Kali%20Linux-Ready-111820?style=for-the-badge&logo=kalilinux&logoColor=white" alt="Kali Linux Ready">
  <img src="https://img.shields.io/badge/CLI-Security%20Framework-8B5CF6?style=for-the-badge&labelColor=0B0F14" alt="CLI Security Framework">
</p>

<p><em>A structured security-assessment workflow for authorized testing, labs, CTFs, and security research.</em></p>

<!-- Optional hero asset: upload assets/axionr-banner.gif and uncomment. -->

<!-- <img src="assets/axionr-banner.gif" width="100%" alt="AxionR Anime Cybersecurity Banner"> -->

</div>

🛰️ Overview

AxionR is a Python-based cybersecurity reconnaissance and web security assessment framework that organizes multiple security tools and analysis stages into a single, repeatable workflow.

Rather than attempting to replace every specialized security utility, AxionR acts as an assessment orchestration layer: it coordinates discovery, analysis, evidence collection, finding normalization, and reporting around a target-specific workspace.

Discover the attack surface → organize evidence → assess security signals → preserve findings → generate a useful report.

🏗️ Assessment Architecture

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
     ┌─────┼─────┐
     ▼     ▼     ▼
   DNS /  PORTS / TECHNOLOGY
   HOSTS   WEB    DISCOVERY
     │     │     │
     └─────┼─────┘
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
│  CONTENT DISCOVERY  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ SECURITY ASSESSMENT │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│       FINDING ANALYSIS      │
│ Normalize • Deduplicate     │
│ Classify • Correlate        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      EVIDENCE + REPORTS     │
└─────────────────────────────┘

🎯 Project Goals

AxionR is designed to make authorized security assessments more structured, repeatable, and easier to review.

Primary goals

Centralize reconnaissance workflows.

Reduce repetitive manual command execution.

Maintain a separate workspace for each target.

Validate scope before assessment stages.

Combine passive and active discovery.

Normalize findings from different tools.

Preserve scanner evidence and execution metadata.

Distinguish observations and candidates from confirmed vulnerabilities.

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

Typical outputs include:

domains;

subdomains;

resolved hosts;

historical URLs;

live HTTP services;

technology metadata.

🌐 02 — Asset Discovery

The asset-discovery stage can organize:

domains;

subdomains;

IP addresses;

DNS results;

HTTP/HTTPS services;

ports;

service banners;

technology metadata;

WAF observations.

Supporting tools include:

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

historical archives;

passive URL collection;

HTTP probing;

web crawling;

application-discovered URLs.

Discovered URLs are filtered against the assessment scope before being used in later stages.

🧩 04 — JavaScript Analysis

AxionR performs lightweight JavaScript analysis for:

JavaScript URL collection;

endpoint candidates;

API-like paths;

suspicious configuration patterns;

token/secret-like strings requiring manual validation.

Important: A string matching a secret-like pattern is a candidate, not proof that a valid secret exists or is exploitable.

🔎 05 — Parameter Discovery

AxionR can identify URLs containing parameters and integrate parameter-discovery tooling where available.

Example:

https://example.com/search?q=test
                         └── parameter

Parameter information can help prioritize later authorized security review.

📂 06 — Content Discovery

AxionR can integrate FFUF and available wordlists for authorized path discovery.

Common HTTP result categories include:

Code

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

Discovery results are preserved for analysis and are not automatically treated as vulnerabilities.

🛡️ 07 — Security Assessment

AxionR supports security-assessment integrations including:

Nuclei;

Dalfox;

SQLMap integration/detection foundation;

AxionR custom low-impact checks.

Scanner-output philosophy

Scanner output
      │
      ▼
AxionR finding
      │
      ▼
Evidence preserved
      │
      ▼
Manual validation
      │
      ▼
Confirmed finding

AxionR does not automatically treat every scanner result as a confirmed vulnerability.

🧠 Finding Intelligence

AxionR uses a structured finding model to keep results consistent across tools.

Example

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

This distinction matters:

Observation          ≠ Vulnerability
Candidate            ≠ Confirmed
Scanner output       ≠ Independent validation

🎮 Operating Modes

AxionR provides nine assessment modes:

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

Third-party tools are independently maintained projects. Their installation requirements, CLI behavior, versions, output formats, and licenses may vary.

🖥️ CLI Experience

AxionR uses a consistent dark technical terminal identity.

Example:

                         AxionR

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

completion dashboard;

warnings and errors;

report paths.

The visual direction is intended to remain clean and professional, rather than relying on excessive hacker-style effects.

🌌 Anime / Cybersecurity Visual Identity

AxionR can use an anime-inspired cybersecurity visual system for GitHub documentation and project presentation.

Visual direction

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

Recommended assets

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

After uploading the asset:

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

Runtime data

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

OS       : Kali Linux / Debian-based Linux
Python   : Python 3.x
Git      : Git
Optional : Go

Some assessment modules require additional external tools.

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/AxionR.git
cd AxionR

Replace YOUR_USERNAME with your GitHub username.

2. Check Python

python3 --version

3. Run setup

sudo python3 axionr.py --setup

AxionR checks for missing dependencies and can optionally install supported packages/tools.

4. Check tool status

python3 axionr.py --status

⚡ Quick Start

Interactive mode

python3 axionr.py

FULL assessment

python3 axionr.py example.com --mode full

Reconnaissance

python3 axionr.py example.com --mode recon

Quick triage

python3 axionr.py example.com --mode quick

CTF / lab

python3 axionr.py example.com --mode ctf

eJPT-style lab

python3 axionr.py example.com --mode ejpt

OSCP-style authorized lab

python3 axionr.py example.com --mode oscp

Audit

python3 axionr.py example.com --mode audit

Custom workflow

python3 axionr.py example.com --mode custom

Disable automatic installation

python3 axionr.py example.com --mode recon --no-install

Start a new scan

python3 axionr.py example.com --mode full --new

🛡️ Scope Management

AxionR creates a target-specific scope file:

workspace/<target>/scope.txt

Example:

# AxionR authorized scope

example.com

Before active testing:

Verify that you have permission.

Review the scope.

Confirm allowed domains/IPs.

Confirm permitted testing methods.

Confirm rate limits and program rules.

Start the assessment only after authorization is established.

Scope filtering is also applied when processing discovered URLs.

🔄 Checkpoint & Resume

AxionR stores workflow state in:

workspace/<target>/status.json

Completed phases can be preserved so a later run can continue without unnecessarily repeating completed workflow stages.

Start completely fresh

python3 axionr.py example.com --mode full --new

Disable resume behavior

python3 axionr.py example.com --mode full --no-resume

📦 Workspace Output

AxionR maintains a separate workspace for every target so that reconnaissance data, discovered assets, scan results, evidence, logs, findings, and reports remain organized throughout the assessment.

For example, when the authorized target is:

example.com

AxionR creates a target-specific workspace:

workspace/
└── example.com/
    │
    ├── 📄 scope.txt
    ├── 📄 status.json
    │
    ├── 🔎 recon/
    │   ├── subfinder.txt
    │   ├── amass.txt
    │   ├── gau.txt
    │   ├── waybackurls.txt
    │   └── recon_summary.txt
    │
    ├── 🌐 assets/
    │   ├── subdomains.txt
    │   ├── all_hosts.txt
    │   ├── live_hosts.txt
    │   ├── resolved_ips.txt
    │   └── technologies.txt
    │
    ├── 🧬 dns/
    │   ├── dns_records.txt
    │   ├── resolved_ips.txt
    │   ├── live_hosts.txt
    │   └── dnsx_results.txt
    │
    ├── 🔌 ports/
    │   ├── nmap.txt
    │   ├── naabu.txt
    │   ├── open_ports.txt
    │   ├── services.txt
    │   └── port_summary.txt
    │
    ├── 🖥️ web/
    │   ├── httpx_raw.txt
    │   ├── live_urls.txt
    │   ├── http_status.txt
    │   ├── technologies.txt
    │   ├── waf_detection.txt
    │   └── web_summary.txt
    │
    ├── 🔗 urls/
    │   ├── gau.txt
    │   ├── waybackurls.txt
    │   ├── katana.txt
    │   ├── hakrawler.txt
    │   ├── all_urls.txt
    │   └── in_scope_urls.txt
    │
    ├── 🧩 javascript/
    │   ├── javascript_urls.txt
    │   ├── endpoints.txt
    │   ├── api_candidates.txt
    │   ├── secret_candidates.txt
    │   └── javascript_analysis.txt
    │
    ├── 🔎 parameters/
    │   ├── observed_parameters.txt
    │   ├── arjun_results.txt
    │   ├── parameter_urls.txt
    │   └── parameter_analysis.txt
    │
    ├── 📂 content/
    │   ├── ffuf_results.txt
    │   ├── discovered_paths.txt
    │   ├── interesting_paths.txt
    │   └── content_summary.txt
    │
    ├── 🛡️ scans/
    │   ├── nuclei.jsonl
    │   ├── nuclei.txt
    │   ├── dalfox.txt
    │   ├── sqlmap_notice.txt
    │   └── scanner_summary.txt
    │
    ├── 🧠 findings/
    │   ├── findings.json
    │   ├── findings_normalized.json
    │   ├── findings_deduplicated.json
    │   └── raw_count.txt
    │
    ├── 🔬 evidence/
    │   ├── environment.json
    │   ├── headers/
    │   ├── requests/
    │   ├── responses/
    │   └── screenshots/
    │
    ├── 📝 logs/
    │   ├── commands.jsonl
    │   ├── execution.log
    │   ├── errors.log
    │   └── timestamps.log
    │
    └── 📊 reports/
        ├── axionr_report.html
        ├── axionr_report.json
        └── summary.txt

📁 Directory Responsibilities

Each directory represents a stage or output category in the AxionR assessment pipeline.

📄 Root Files

scope.txt
status.json

scope.txt

Contains the authorized assessment scope.

Example:

# AxionR Authorized Scope

example.com
*.example.com

The scope file helps keep assessment activity aligned with the intended authorization boundary.

status.json

Stores workflow state used by checkpoint and resume functionality.

Typical state can include:

Target
Mode
Completed phases
Current phase
Scan status
Start time
Last update

🔎 recon/

Stores raw and processed reconnaissance results.

Typical sources include:

Subfinder
Amass
GAU
Waybackurls

Example:

recon/
├── subfinder.txt
├── amass.txt
├── gau.txt
├── waybackurls.txt
└── recon_summary.txt

Purpose:

Passive Discovery
       ↓
Initial Attack-Surface Mapping

🌐 assets/

Contains the consolidated asset inventory.

Example:

assets/
├── subdomains.txt
├── all_hosts.txt
├── live_hosts.txt
├── resolved_ips.txt
└── technologies.txt

Typical information:

Domains
Subdomains
Hosts
IP addresses
Live services
Technologies

This inventory becomes the foundation for later assessment stages.

🧬 dns/

Stores DNS discovery and resolution results.

Example:

dns/
├── dns_records.txt
├── resolved_ips.txt
├── live_hosts.txt
└── dnsx_results.txt

Possible data includes:

A
AAAA
CNAME
MX
NS
TXT
Resolved IP addresses
DNS probing results

🔌 ports/

Stores network and service enumeration results.

Example:

ports/
├── nmap.txt
├── naabu.txt
├── open_ports.txt
├── services.txt
└── port_summary.txt

Typical information:

Open ports
Services
Service versions
Protocols
Network exposure

Example:

22    SSH
80    HTTP
443   HTTPS
8080  HTTP

🖥️ web/

Contains HTTP/HTTPS probing and web-service analysis.

Example:

web/
├── httpx_raw.txt
├── live_urls.txt
├── http_status.txt
├── technologies.txt
├── waf_detection.txt
└── web_summary.txt

Typical information:

HTTP status
Page title
Web server
Technologies
Redirects
HTTPS availability
WAF observations

🔗 urls/

Central URL-discovery workspace.

AxionR can combine URL sources such as:

GAU
Waybackurls
Katana
Hakrawler
HTTP probing

Example:

urls/
├── gau.txt
├── waybackurls.txt
├── katana.txt
├── hakrawler.txt
├── all_urls.txt
└── in_scope_urls.txt

The URL pipeline is:

Multiple URL Sources
        ↓
Normalization
        ↓
Deduplication
        ↓
Scope Filtering
        ↓
in_scope_urls.txt

🧩 javascript/

Stores JavaScript resources and analysis results.

Example:

javascript/
├── javascript_urls.txt
├── endpoints.txt
├── api_candidates.txt
├── secret_candidates.txt
└── javascript_analysis.txt

Possible analysis includes:

JavaScript files
Endpoint candidates
API-like paths
Configuration patterns
Secret-like strings

Secret-like strings and endpoint patterns are treated as candidates requiring validation, not automatically as confirmed vulnerabilities or valid credentials.

🔎 parameters/

Stores discovered URL parameters and parameter-analysis results.

Example:

parameters/
├── observed_parameters.txt
├── arjun_results.txt
├── parameter_urls.txt
└── parameter_analysis.txt

Example:

https://example.com/search?q=test
                              └── q

Parameter information can help prioritize later authorized security testing.

📂 content/

Stores web-content discovery results.

Example:

content/
├── ffuf_results.txt
├── discovered_paths.txt
├── interesting_paths.txt
└── content_summary.txt

Possible discoveries:

/admin
/login
/api
/backup
/assets
/config

A discovered path is not automatically a vulnerability.

🛡️ scans/

Contains security-tool output.

Example:

scans/
├── nuclei.jsonl
├── nuclei.txt
├── dalfox.txt
├── sqlmap_notice.txt
└── scanner_summary.txt

Integrated assessment tooling can include:

Nuclei
Dalfox
SQLMap
AxionR custom checks

Scanner pipeline:

Security Scanner
       ↓
Raw Output
       ↓
AxionR Parser
       ↓
Normalized Finding
       ↓
Evidence
       ↓
Manual Validation

Scanner output should not automatically be interpreted as a confirmed vulnerability.

🧠 findings/

Contains structured security findings generated by AxionR.

Example:

findings/
├── findings.json
├── findings_normalized.json
├── findings_deduplicated.json
└── raw_count.txt

A finding can contain:

Finding ID
Finding Type
Target
URL
Severity
Confidence
Status
Source
Evidence
Timestamp

Example:

{
  "id": "a1b2c3d4",
  "type": "Missing HSTS",
  "severity": "LOW",
  "confidence": "MEDIUM",
  "status": "CANDIDATE",
  "target": "example.com",
  "source": "AxionR-Headers"
}

Finding lifecycle:

Observation
    ↓
Candidate
    ↓
Normalized
    ↓
Deduplicated
    ↓
Validated
    ↓
Reported

🔬 evidence/

Stores supporting assessment evidence.

Example:

evidence/
├── environment.json
├── headers/
├── requests/
├── responses/
└── screenshots/

Evidence may include:

HTTP headers
Tool output
Request/response information
Environment metadata
Screenshots
Scanner evidence

The purpose is to make findings easier to review and reproduce.

📝 logs/

Stores execution and diagnostic information.

Example:

logs/
├── commands.jsonl
├── execution.log
├── errors.log
└── timestamps.log

Typical information:

Executed command
Module
Timestamp
Exit status
Execution result
Error information

This helps diagnose failed tools and reconstruct the assessment timeline.

📊 reports/

Contains the final assessment outputs.

reports/
├── axionr_report.html
├── axionr_report.json
└── summary.txt

HTML Report

axionr_report.html

Designed for:

browser viewing;

demonstrations;

project presentations;

assessment review.

JSON Report

axionr_report.json

Designed for:

automation;

integrations;

parsing;

future dashboards;

data processing.

Text Summary

summary.txt

Designed for:

terminal review;

quick assessment summaries;

compact result sharing.

🔄 Complete Workspace Data Flow

                    TARGET
                       │
                       ▼
                SCOPE VALIDATION
                       │
                       ▼
                 RECONNAISSANCE
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
        DNS          HOSTS         WEB
          │            │            │
          └────────────┼────────────┘
                       ▼
                 ASSET INVENTORY
                       │
                       ▼
                  URL DISCOVERY
                       │
                       ▼
              SCOPE + DEDUPLICATION
                       │
                       ▼
             JAVASCRIPT ANALYSIS
                       │
                       ▼
             PARAMETER DISCOVERY
                       │
                       ▼
              CONTENT DISCOVERY
                       │
                       ▼
             SECURITY ASSESSMENT
                       │
                       ▼
               RAW SCANNER DATA
                       │
                       ▼
             FINDING NORMALIZATION
                       │
                       ▼
                DEDUPLICATION
                       │
                       ▼
             EVIDENCE COLLECTION
                       │
                       ▼
               FINDING ANALYSIS
                       │
                       ▼
                  REPORTING
              ┌────────┼────────┐
              ▼        ▼        ▼
            HTML      JSON      TXT

🗂️ Target Isolation

Every target receives its own workspace:

workspace/
├── example.com/
├── test.lab/
└── lab.local/

Each target maintains its own:

Scope
Recon
Assets
DNS
Ports
Web data
URLs
JavaScript
Parameters
Content
Scans
Findings
Evidence
Logs
Reports

This keeps assessment data from different targets isolated at the workspace level.

🔐 Workspace Security

Workspace data may contain sensitive assessment information.

Do not commit the following to a public GitHub repository:

workspace/
private scan results
credentials
API keys
tokens
private target information
client data
personal information
confidential evidence

Recommended .gitignore entries:

# AxionR runtime data
workspace/
logs/

# Local configuration
config/config.json

# Sensitive files
*.key
*.pem
*.secret
.env
.env.*

# Python
__pycache__/
*.pyc

# Local virtual environment
.venv/
venv/

📌 Workspace Notes

The exact files produced can vary depending on:

selected AxionR mode;

installed third-party tools;

target scope;

tool availability;

successful execution of individual phases;

assessment configuration.

Therefore, the structure above describes the logical AxionR workspace architecture. Individual files or directories may not be created during every run.

📊 Reporting

AxionR produces multiple report formats.

Format

File

Purpose

HTML

reports/axionr_report.html

Browser viewing, demonstrations, assessment review

JSON

reports/axionr_report.json

Automation, parsing, integrations

TXT

reports/summary.txt

Quick terminal review

Example report summary

AxionR Security Assessment

Target:  example.com
Mode:    FULL

Assets:  42
URLs:    1,248
Findings: 37

Critical:       0
High:           3
Medium:        11
Low:           12
Informational: 11

Example numbers are illustrative. Actual results depend on the authorized target, scope, and installed tools.

🔬 Evidence Collection

AxionR preserves evidence generated during the workflow.

Examples include:

tool output;

HTTP headers;

scanner JSON;

discovered URLs;

DNS results;

port/service output;

technology observations;

execution metadata.

Command execution metadata is stored in:

logs/commands.jsonl

This helps make assessments more reproducible and reviewable.

🧠 Finding Correlation & Deduplication

Multiple tools can report related observations.

AxionR attempts to normalize and deduplicate findings using structured attributes such as:

Finding type
URL
Source
Severity
Evidence

The goal is to reduce duplicate entries while preserving the original evidence source.

⚠️ Finding Validation Philosophy

AxionR deliberately separates potential signals from validated findings:

Potential signal
      ↓
Candidate
      ↓
Scanner-reported observation
      ↓
Manual validation
      ↓
Confirmed vulnerability

A candidate should not automatically be presented as an exploitable vulnerability.

This is particularly important for:

redirect observations;

missing security headers;

JavaScript secret-like strings;

scanner output;

technology disclosures;

SSRF/IDOR-style candidates.

🧪 Testing Philosophy

When developing or extending AxionR:

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

Better attack-surface relationship visualization

🎬 GitHub Demo

A concise professional demo should show:

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

Recommended demo asset:

assets/terminal-demo.gif

A short terminal GIF can be placed near the top of the README after the final UI is recorded.

🖼️ Screenshot Gallery

After capturing the final interface, add:

Startup

![AxionR Startup](assets/screenshots/startup.png)

Recon

![AxionR Recon](assets/screenshots/recon.png)

Security Assessment

![AxionR Scan](assets/screenshots/scan.png)

Report

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

bug bounty programs where testing is explicitly allowed;

security research with permission;

defensive assessment.

Do not run AxionR against systems you do not own or have explicit permission to assess.

Users are responsible for complying with applicable laws, contracts, program rules, and authorization boundaries.

⚖️ Legal & Safety Notice

AxionR is a security-assessment framework.

The project itself does not grant permission to test any target.

Third-party security tools integrated by AxionR have their own licenses, terms, and usage requirements. Review those requirements before using them.

The authors and contributors are not responsible for unauthorized, illegal, destructive, or abusive use of the software.

Always establish authorization and scope before running active assessment modules.

📜 License

Add an appropriate open-source license to the repository before publishing it as an open-source project.

For example:

LICENSE

If the project is released under MIT, add the official MIT license text to LICENSE and update this section accordingly.

👨‍💻 Project

<div align="center">

⚡ AxionR

Web Security Reconnaissance & Assessment Framework

Built as a cybersecurity learning, research, and authorized-assessment project.

<br>

Recon • Discover • Analyze • Validate • Report

<br>

v2.0.0

<sub>Built for authorized security testing.</sub>

</div>
