<div align="center">

<a href="https://github.com/TocsiVector/AxionR">
  <img src="https://img.shields.io/badge/⚡_AXIONR-v2.0.0-00D9FF?style=for-the-badge&labelColor=070B12" alt="AxionR v2.0.0">
</a>

<h1>AXIONR</h1>

<h3>Web Security Reconnaissance & Assessment Framework</h3>

<p>
  <strong>Reconnaissance · Discovery · Analysis · Evidence · Reporting</strong>
</p>

<p>
  <a href="https://github.com/TocsiVector/AxionR/stargazers">
    <img src="https://img.shields.io/github/stars/TocsiVector/AxionR?style=flat-square&logo=github&label=Stars" alt="GitHub stars">
  </a>
  <a href="https://github.com/TocsiVector/AxionR/network/members">
    <img src="https://img.shields.io/github/forks/TocsiVector/AxionR?style=flat-square&logo=github&label=Forks" alt="GitHub forks">
  </a>
  <a href="https://github.com/TocsiVector/AxionR/issues">
    <img src="https://img.shields.io/github/issues/TocsiVector/AxionR?style=flat-square&logo=github&label=Issues" alt="GitHub issues">
  </a>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.x">
  <img src="https://img.shields.io/badge/Kali%20Linux-Ready-111820?style=flat-square&logo=kalilinux&logoColor=white" alt="Kali Linux">
  <img src="https://img.shields.io/badge/License-Apache--2.0-D22128?style=flat-square" alt="Apache 2.0">
</p>

<p>
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=18&duration=2600&pause=900&color=00D9FF&center=true&vCenter=true&width=800&lines=Recon+%E2%86%92+Discovery+%E2%86%92+Analysis+%E2%86%92+Evidence+%E2%86%92+Reporting;Authorized+Security+Testing+%7C+Labs+%7C+CTFs+%7C+Security+Research;One+Workflow+%7C+Multiple+Security+Tools+%7C+Structured+Findings" alt="AxionR animated typing banner">
</p>

<p>
  <em>A structured assessment orchestration layer for authorized security testing, labs, CTFs, and security research.</em>
</p>

</div>

Visual identity: AxionR uses a dark SOC/cyberpunk + anime-inspired presentation. Optional local image/GIF assets can be added under assets/ without changing the core framework.

🧭 Quick Navigation

Overview

Why AxionR

Architecture

Workflow

Features

Operating Modes

Tool Stack

Finding Intelligence

Workspace

Reports

Installation

Quick Start

Visual / Animation Assets

Security & Responsible Use

Roadmap

Contributing

🛰️ Overview

AxionR is a Python-based cybersecurity reconnaissance and web security assessment framework that organizes multiple security utilities and assessment stages into a single, repeatable workflow.

Instead of replacing specialized security tools, AxionR acts as an assessment orchestration layer that coordinates:

Scope
  ↓
Reconnaissance
  ↓
Asset Discovery
  ↓
Web / Service Discovery
  ↓
URL Collection & Normalization
  ↓
JavaScript / Parameter / Content Analysis
  ↓
Security Assessment
  ↓
Finding Normalization
  ↓
Evidence Collection
  ↓
Structured Reporting

Core principle

Discover the attack surface → organize evidence → assess security signals → preserve findings → generate a useful report.

💡 Why AxionR

Security testing often involves many independent commands, tools, output formats, and temporary files.

AxionR brings those stages into one target-specific workflow.

Without orchestration

With AxionR

Many terminal commands

One structured workflow

Scattered output

Target-specific workspace

Different output formats

Normalized findings

Repeated manual steps

Reusable assessment modes

Harder result tracking

Checkpoint/resume

Raw scanner output

Finding + evidence model

Manual report preparation

HTML / JSON / TXT reports

AxionR is therefore best understood as an orchestration and evidence layer, not as a replacement for every specialized security utility.

🏗️ Architecture

                         ┌──────────────────────┐
                         │   AUTHORIZED TARGET  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   SCOPE VALIDATION   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   RECONNAISSANCE     │
                         └──────────┬───────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  ▼                 ▼                 ▼
             DNS / HOSTS      PORTS / SERVICES   WEB / TECH
                  │                 │                 │
                  └─────────────────┼─────────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │   ASSET INVENTORY    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    URL DISCOVERY     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ JS / PARAM / CONTENT │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ SECURITY ASSESSMENT  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ NORMALIZE + DEDUPE   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ EVIDENCE + ANALYSIS  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
                  HTML            JSON             TXT

🔄 Assessment Workflow

01  Setup
      ↓
02  Scope
      ↓
03  Recon
      ↓
04  Asset Discovery
      ↓
05  URL Discovery
      ↓
06  JavaScript Analysis
      ↓
07  Parameter Discovery
      ↓
08  Content Discovery
      ↓
09  Security Assessment
      ↓
10  Finding Normalization
      ↓
11  Correlation / Deduplication
      ↓
12  Evidence Collection
      ↓
13  Report Generation

Assessment lifecycle

INPUT
  │
  ├── Target
  ├── Scope
  ├── Mode
  └── Configuration
  │
  ▼
DISCOVERY
  │
  ├── Domains
  ├── Hosts
  ├── DNS
  ├── Ports
  ├── Services
  ├── URLs
  ├── JavaScript
  └── Parameters
  │
  ▼
ASSESSMENT
  │
  ├── Security headers
  ├── WAF observations
  ├── Scanner integrations
  └── Low-impact custom checks
  │
  ▼
INTELLIGENCE
  │
  ├── Normalize
  ├── Deduplicate
  ├── Correlate
  ├── Classify
  └── Preserve evidence
  │
  ▼
OUTPUT
  ├── HTML
  ├── JSON
  └── TXT

✨ Features

🔍 01 — Reconnaissance

Subdomain discovery

Passive URL collection

Historical URL discovery

DNS probing

HTTP probing

Web crawling

Technology detection

🌐 02 — Attack-Surface Mapping

Domain inventory

Subdomain inventory

Host discovery

IP resolution

Port/service discovery

HTTP/HTTPS mapping

Technology observations

WAF observations

🔗 03 — URL Intelligence

GAU
Waybackurls
Katana
Hakrawler
HTTPX
      ↓
Normalization
      ↓
Deduplication
      ↓
Scope Filtering
      ↓
In-Scope URL Set

🧩 04 — JavaScript Analysis

JavaScript URL collection

Endpoint candidates

API-like paths

Configuration patterns

Secret-like strings requiring validation

A secret-like string is a candidate, not automatically a credential or confirmed security issue.

🔎 05 — Parameter Discovery

Observed query parameters

Parameter candidates

Parameter URLs

Arjun integration

📂 06 — Content Discovery

FFUF integration

Path discovery

Interesting-path collection

Status-code analysis

Wordlist support

🛡️ 07 — Security Assessment

Nuclei integration

Dalfox integration

SQLMap integration/detection foundation

AxionR custom low-impact checks

Finding normalization

Evidence preservation

🎮 Operating Modes

Mode

Purpose

FULL

Complete authorized assessment workflow

RECON

Reconnaissance and attack-surface discovery

BUG BOUNTY

Authorized web application assessment

CTF

CTF/lab enumeration

eJPT

Pentesting/lab practice workflow

OSCP

Authorized lab enumeration

AUDIT

Security/configuration assessment

QUICK

Fast initial triage

CUSTOM

User-selected workflow

Mode matrix

Capability

FULL

RECON

QUICK

CTF

AUDIT

Scope

✓

✓

✓

✓

✓

Recon

✓

✓

✓

✓

✓

Assets

✓

✓

✓

✓

✓

URLs

✓

✓

—

✓

Optional

JS

✓

✓

—

Optional

Optional

Parameters

✓

Optional

—

Optional

Optional

Content

✓

Optional

—

✓

Optional

Security checks

✓

Optional

✓

✓

✓

Reports

✓

✓

✓

✓

✓

Optional and — indicate workflow intent rather than a guarantee that every third-party tool is available.

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

Discovery

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

AxionR custom checks

Low-impact framework checks

Third-party tools are independently maintained projects with their own licenses, versions, command-line behavior, and usage requirements.

🧠 Finding Intelligence

AxionR separates signals, candidates, observations, and validated findings.

Finding pipeline

Raw Observation
      ↓
Candidate
      ↓
Normalized Finding
      ↓
Deduplication
      ↓
Evidence
      ↓
Manual Validation
      ↓
Confirmed / Reported Finding

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

Example

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

Important: Scanner output, endpoint candidates, secret-like strings, SSRF/IDOR candidates, and other observations are not automatically confirmed vulnerabilities.

📦 Workspace Output

Every target receives an isolated workspace.

workspace/
└── example.com/
    ├── scope.txt
    ├── status.json
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

Workspace responsibilities

Directory

Purpose

recon/

Reconnaissance output

assets/

Domains, hosts, IPs, technologies

dns/

DNS records and resolution

ports/

Ports and services

web/

HTTP probing and WAF observations

urls/

Collected and normalized URLs

javascript/

JavaScript analysis

parameters/

Parameter discovery

content/

Content/path discovery

scans/

Security-tool output

findings/

Structured findings

evidence/

Supporting evidence

logs/

Execution logs

reports/

Final reports

<details>
<summary><strong>📂 Expand complete example workspace</strong></summary>

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

</details>

Workspace data flow

Target
  ↓
Scope Validation
  ↓
Recon
  ↓
Assets
  ↓
URLs
  ↓
JavaScript / Parameters / Content
  ↓
Security Assessment
  ↓
Normalize
  ↓
Deduplicate / Correlate
  ↓
Evidence
  ↓
Reports
  ├── HTML
  ├── JSON
  └── TXT

📊 Reporting

AxionR supports structured outputs:

Format

Output

Use

HTML

axionr_report.html

Browser review

JSON

axionr_report.json

Automation / parsing

TXT

summary.txt

Terminal summary

Example:

╔══════════════════════════════════════════╗
║          AXIONR ASSESSMENT               ║
╠══════════════════════════════════════════╣
║ Target : example.com                     ║
║ Mode   : FULL                            ║
╠══════════════════════════════════════════╣
║ Assets : 42                              ║
║ URLs   : 1,248                           ║
║ Findings: 37                             ║
╚══════════════════════════════════════════╝

Example values are illustrative only.

🔬 Evidence & Audit Trail

AxionR can preserve:

command execution metadata;

scanner output;

HTTP observations;

DNS results;

port/service information;

discovered URLs;

technology observations;

environment information.

Example:

logs/
├── commands.jsonl
├── execution.log
├── errors.log
└── timestamps.log

The objective is reproducibility and reviewability, not concealment.

🧪 Validation Philosophy

AxionR follows a conservative interpretation model:

Discovery
   ↓
Observation
   ↓
Candidate
   ↓
Evidence
   ↓
Validation
   ↓
Finding

This is especially important for:

scanner findings;

missing security headers;

JavaScript secret-like strings;

open redirect candidates;

SSRF candidates;

IDOR candidates;

technology disclosures.

🧭 Assessment Coverage

AxionR organizes the assessment surface across multiple layers:

Layer

Coverage

Scope

Target and authorization boundary

Recon

Passive and active discovery workflow

DNS

Resolution and DNS observations

Assets

Hosts, subdomains, IPs, technologies

Network

Ports and services

Web

HTTP/HTTPS and application metadata

URLs

Historical, crawled, and discovered URLs

JavaScript

Endpoint and secret-like candidates

Parameters

Observed and discovered parameters

Content

Authorized path/content discovery

Security

Scanner integrations and custom checks

Findings

Normalization, severity, confidence, status

Evidence

Supporting assessment information

Reporting

HTML, JSON, TXT

🔐 Scope-First Design

AxionR is designed around a scope-first assessment model.

Authorization
     ↓
Defined Scope
     ↓
Scope Validation
     ↓
Discovery
     ↓
Assessment
     ↓
Evidence
     ↓
Reporting

The intended workflow is to establish the authorization boundary before active assessment begins.

Example:

# Authorized Scope

example.com
*.example.com

The target-specific scope is stored in:

workspace/<target>/scope.txt

🧩 Assessment Modules

01 — Reconnaissance

Purpose:

Discover the external attack surface

Typical outputs:

subdomains;

domains;

historical URLs;

DNS observations;

HTTP services;

discovered hosts.

02 — Asset Discovery

Purpose:

Build a consolidated target inventory

Typical assets:

domains;

subdomains;

hosts;

IP addresses;

live services;

technologies.

03 — Network Enumeration

Purpose:

Identify exposed ports and services

Typical information:

open ports;

protocols;

services;

service versions;

network exposure.

04 — Web Discovery

Purpose:

Understand the observable web surface

Typical information:

HTTP status;

page titles;

technologies;

redirects;

web servers;

HTTPS;

WAF observations.

05 — URL Intelligence

Purpose:

Build a clean, deduplicated URL dataset

Pipeline:

Collection
   ↓
Normalization
   ↓
Deduplication
   ↓
Scope Filtering
   ↓
In-Scope URLs

06 — JavaScript Intelligence

Purpose:

Extract useful application-side discovery signals

Possible observations:

JavaScript resources;

endpoint candidates;

API-like paths;

configuration patterns;

secret-like strings.

07 — Parameter Intelligence

Purpose:

Identify application input surfaces

Possible sources:

observed URLs;

crawlers;

Arjun;

application-discovered parameters.

08 — Content Discovery

Purpose:

Identify accessible or interesting application paths

Possible observations:

directories;

files;

administrative paths;

API paths;

backup-like paths;

authentication endpoints.

A discovered path remains an observation until its security significance is established.

09 — Security Assessment

Purpose:

Evaluate security signals discovered during the workflow

Integrations can include:

Nuclei;

Dalfox;

SQLMap;

AxionR custom checks.

10 — Finding Intelligence

Purpose:

Convert raw observations into structured security findings

Pipeline:

Raw Output
   ↓
Parser
   ↓
Normalization
   ↓
Deduplication
   ↓
Correlation
   ↓
Evidence
   ↓
Validation
   ↓
Report

📐 Data Processing Model

AxionR follows a structured data path:

RAW DATA
   │
   ├── Tool Output
   ├── Discovery Results
   ├── HTTP Metadata
   └── Assessment Signals
   │
   ▼
NORMALIZATION
   │
   ▼
DEDUPLICATION
   │
   ▼
CORRELATION
   │
   ▼
FINDING MODEL
   │
   ├── Type
   ├── Severity
   ├── Confidence
   ├── Status
   ├── Target
   ├── Source
   └── Evidence
   │
   ▼
REPORTING

This structure makes output easier to inspect, process, compare, and report.

🧠 Finding Model

A structured finding can contain:

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
Description

Example:

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

🔗 Finding Correlation

Multiple tools can produce overlapping results.

AxionR can conceptually correlate:

Finding A ─────┐
Finding B ─────┼──→ Normalization
Finding C ─────┘
                    ↓
               Deduplication
                    ↓
                 Correlation
                    ↓
                  Evidence
                    ↓
                Validation

The purpose is to reduce duplicate reporting while retaining useful source information.

🧪 Validation Levels

AxionR intentionally separates levels of certainty.

Level

Meaning

OBSERVED

Something was observed during assessment

CANDIDATE

A potential security issue requires validation

REPORTED

Included in assessment reporting

CONFIRMED

Independently validated

INFORMATIONAL

Useful security information without a vulnerability claim

This prevents raw tool output from being presented as automatically confirmed.

📊 Severity Model

AxionR can organize findings using:

CRITICAL
HIGH
MEDIUM
LOW
INFO

Severity and confidence are separate properties.

For example:

Severity   : HIGH
Confidence : LOW
Status     : CANDIDATE

This communicates that an observation may be important but still requires validation.

🔬 Evidence Model

Evidence is associated with assessment observations where available.

Examples:

HTTP Headers
Tool Output
DNS Results
Port Information
URLs
Technology Metadata
Scanner Output
Environment Metadata
Execution Metadata

Evidence supports review and reproducibility.

🔄 Reproducibility

AxionR aims to make an assessment easier to reconstruct by preserving:

Target
Scope
Mode
Workflow State
Commands
Tool Output
Findings
Evidence
Reports

This is especially useful for:

learning;

lab exercises;

debugging;

repeat assessments;

project demonstrations;

security documentation.

📁 Target Isolation

Each target receives its own workspace:

workspace/
├── example.com/
├── test.lab/
└── lab.local/

This prevents different assessment datasets from being mixed together at the workspace level.

🧹 Data Hygiene

AxionR separates:

PUBLIC PROJECT CODE
        │
        ├── axionr.py
        ├── README.md
        ├── LICENSE
        └── docs/assets
        │
        ▼
PRIVATE RUNTIME DATA
        │
        ├── workspace/
        ├── logs/
        ├── credentials
        ├── tokens
        └── private evidence

Public repositories should contain project code and documentation, not private assessment results.

⚙️ Dependency Model

AxionR can work as an orchestration layer around external security utilities.

Conceptually:

AxionR
  │
  ├── Python Runtime
  │
  ├── Recon Tools
  │
  ├── Network Tools
  │
  ├── Web Discovery Tools
  │
  ├── Security Scanners
  │
  └── Reporting / Analysis

Availability of individual integrations depends on the local environment and installed tools.

🧱 Design Principles

AxionR follows these project principles:

Scope First

Authorization and scope should be established before active testing.

Modular Workflow

Assessment stages are separated into logical phases.

Evidence Driven

Important observations should retain supporting evidence where available.

Conservative Interpretation

Potential signals are not automatically treated as confirmed vulnerabilities.

Repeatability

Target workspaces and checkpoints make repeated assessment easier.

Separation of Data

Runtime assessment data should remain separate from public project source code.

Tool Orchestration

Specialized security utilities remain specialized; AxionR coordinates their workflow and output.

🎓 Learning Value

AxionR provides hands-on exposure to several cybersecurity domains:

Python Automation
       ↓
Linux / Kali
       ↓
Reconnaissance
       ↓
Networking
       ↓
Web Security
       ↓
Security Tooling
       ↓
Data Normalization
       ↓
Evidence Handling
       ↓
Security Reporting

The project is therefore useful as a practical cybersecurity engineering and assessment-learning project.

🧪 Example Assessment Lifecycle

For an authorized target:

example.com
     │
     ▼
Scope Confirmation
     │
     ▼
Subdomain Discovery
     │
     ▼
DNS / Host Resolution
     │
     ▼
Port / Service Discovery
     │
     ▼
HTTP / Technology Detection
     │
     ▼
URL Collection
     │
     ▼
JavaScript / Parameter Discovery
     │
     ▼
Content Discovery
     │
     ▼
Security Assessment
     │
     ▼
Finding Normalization
     │
     ▼
Evidence Collection
     │
     ▼
HTML / JSON / TXT Reports

📋 Assessment Output Summary

A completed assessment can be summarized across:

Target Information
        ↓
Scope Information
        ↓
Asset Inventory
        ↓
Service Inventory
        ↓
Web Inventory
        ↓
URL Inventory
        ↓
Security Signals
        ↓
Structured Findings
        ↓
Evidence
        ↓
Final Reports

🎨 Anime + Cyber Visual System

AxionR's visual identity is built around:

                 AXIONR
                   │
        ┌──────────┴──────────┐
        │                     │
   Cybersecurity          Anime / SOC
        │                     │
   Recon Dashboard       Futuristic Analyst
        │                     │
   Network Graphs         Neon UI Elements
        └──────────┬──────────┘
                   │
             Dark Terminal

Recommended asset structure

assets/
├── axionr-banner.gif
├── axionr-anime.png
├── axionr-logo.png
├── architecture.png
├── workflow.png
├── terminal-demo.gif
└── screenshots/
    ├── startup.png
    ├── recon.png
    ├── scan.png
    └── report.png

Optional animated banner

GitHub README can display an actual GIF once the file is uploaded:

<p align="center">
  <img
    src="assets/axionr-banner.gif"
    width="100%"
    alt="AxionR animated cybersecurity banner"
  >
</p>

Optional anime character panel

<p align="center">
  <img
    src="assets/axionr-anime.png"
    width="700"
    alt="AxionR anime cybersecurity analyst"
  >
</p>

Do not enable these image tags until the actual files exist in the repository. This prevents broken-image icons.

Animation-safe GitHub elements

The README also uses lightweight animated external SVGs such as the typing banner. No JavaScript, custom CSS, or browser-side code is required.

🖥️ CLI Identity

Example conceptual startup:

                 █████╗ ██╗  ██╗██╗ ██████╗ ███╗   ██╗██████╗
                ██╔══██╗╚██╗██╔╝██║██╔═══██╗████╗  ██║██╔══██╗
                ███████║ ╚███╔╝ ██║██║   ██║██╔██╗ ██║██████╔╝
                ██╔══██║ ██╔██╗ ██║██║   ██║██║╚██╗██║██╔══██╗
                ██║  ██║██╔╝ ██╗██║╚██████╔╝██║ ╚████║██████╔╝
                ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝

                 WEB SECURITY RECONNAISSANCE
                    & ASSESSMENT FRAMEWORK

             Recon • Discovery • Analysis • Evidence • Reporting

📁 Repository Structure

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
│   ├── axionr-logo.png
│   ├── architecture.png
│   ├── workflow.png
│   ├── terminal-demo.gif
│   └── screenshots/
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

Keep these local:

workspace/
logs/
private scan results
credentials
API keys
tokens
private target data
confidential evidence

🚀 Installation

Requirements

OS       : Kali Linux / Debian-based Linux
Python   : Python 3.x
Git      : Git
Optional : Go

Clone

git clone https://github.com/TocsiVector/AxionR.git
cd AxionR

Check Python

python3 --version

Setup

sudo python3 axionr.py --setup

Check tools

python3 axionr.py --status

⚡ Quick Start

Interactive

python3 axionr.py

FULL

python3 axionr.py example.com --mode full

RECON

python3 axionr.py example.com --mode recon

QUICK

python3 axionr.py example.com --mode quick

CTF

python3 axionr.py example.com --mode ctf

eJPT

python3 axionr.py example.com --mode ejpt

OSCP-style lab

python3 axionr.py example.com --mode oscp

AUDIT

python3 axionr.py example.com --mode audit

CUSTOM

python3 axionr.py example.com --mode custom

Fresh assessment

python3 axionr.py example.com --mode full --new

Disable automatic installation

python3 axionr.py example.com --mode recon --no-install

Exact CLI flags should match the current axionr.py implementation. If a flag is not supported by your current build, use the interactive mode or update the command documentation with the implemented interface.

🛡️ Scope Management

Before active testing:

1. Confirm authorization
2. Define target scope
3. Review allowed methods
4. Confirm rate limits
5. Confirm exclusions
6. Start assessment

Example:

# Authorized Scope

example.com
*.example.com

AxionR stores target scope under:

workspace/<target>/scope.txt

🔄 Checkpoint & Resume

Assessment state is stored under:

workspace/<target>/status.json

The purpose is to preserve workflow state and support continuation after interruptions.

Assessment
    ↓
Completed Phase
    ↓
Checkpoint
    ↓
Resume
    ↓
Next Phase

🔐 Workspace Security

Never publish runtime assessment data publicly.

Recommended .gitignore:

# AxionR runtime
workspace/
logs/

# Local configuration
config/config.json

# Secrets
.env
.env.*
*.key
*.pem
*.secret

# Python
__pycache__/
*.pyc
.venv/
venv/

🗺️ Roadmap

v2.0.0 Foundation

Single-file Python framework

Professional CLI

AxionR branding

Assessment modes

Scope management

Workspace generation

Dependency detection

Recon workflow

Asset discovery

URL discovery

JavaScript analysis foundation

Parameter discovery foundation

Content discovery

Security integrations

Finding normalization

Evidence collection

Checkpoint/resume

HTML / JSON / TXT reporting

Future

Interactive terminal dashboard

Expanded correlation engine

CVSS metadata support

Configurable scan profiles

Plugin architecture

CI/CD integration

Optional web dashboard

Rich evidence attachments

Attack-surface visualization

Additional report templates

Expanded passive-intelligence integrations

🎬 Demo Structure

Recommended GitHub demo:

START
  ↓
AxionR Banner
  ↓
Mode Selection
  ↓
Scope Confirmation
  ↓
Recon
  ↓
Asset Discovery
  ↓
URL Discovery
  ↓
Security Assessment
  ↓
Finding Analysis
  ↓
Report Generation
  ↓
HTML Report

Recommended local assets:

assets/terminal-demo.gif
assets/screenshots/startup.png
assets/screenshots/recon.png
assets/screenshots/scan.png
assets/screenshots/report.png

🧪 Testing Philosophy

Prefer

✓ Authorized targets
✓ Controlled labs
✓ Passive discovery
✓ Low-impact validation
✓ Explicit scope
✓ Rate limiting
✓ Evidence preservation
✓ Manual validation

Avoid

✗ Unauthorized scanning
✗ Credential theft
✗ Persistence
✗ Malware deployment
✗ Destructive testing
✗ Data destruction
✗ Concealment of activity

🤝 Contributing

Contributions are welcome when they improve:

legitimate security testing;

cybersecurity education;

documentation;

defensive analysis;

reproducibility;

evidence quality;

reporting.

Guidelines

Keep changes focused.

Preserve scope validation.

Avoid destructive functionality.

Document new dependencies.

Clearly identify third-party integrations.

Do not represent candidates as confirmed vulnerabilities.

Update README/documentation when behavior changes.

Development

git checkout -b feature/your-feature
git add .
git commit -m "Add: your feature"
git push origin feature/your-feature

Then open a pull request.

🐛 Issue Reporting

Include:

AxionR version
Python version
Operating system
Tool version
Command used
Expected behavior
Actual behavior
Relevant error

Never attach:

API keys
Passwords
Credentials
Private target information
Personal information
Confidential assessment results

🔐 Responsible Use

AxionR is intended for:

authorized penetration testing;

cybersecurity education;

CTFs;

controlled laboratories;

permitted bug bounty programs;

security research with authorization;

defensive assessment.

Do not run AxionR against systems you do not own or have explicit permission to assess.

Users are responsible for complying with applicable laws, contracts, program rules, and authorization boundaries.

⚖️ Legal Notice

AxionR is a security-assessment framework.

The software itself does not grant permission to test any target.

Third-party tools integrated with AxionR have their own licenses, terms, and usage requirements.

The authors and contributors are not responsible for unauthorized, illegal, destructive, or abusive use of the software.

Always establish authorization and scope before running active assessment modules.

📜 License

AxionR is released under the Apache License 2.0.

See LICENSE for the complete license text.

<div align="center">

⚡ AXIONR

Web Security Reconnaissance & Assessment Framework

Recon · Discover · Analyze · Validate · Report

<br>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=15&duration=3000&pause=1000&color=00D9FF&center=true&vCenter=true&width=700&lines=Authorized+Security+Testing;Reconnaissance+%7C+Discovery+%7C+Evidence;Built+for+Labs%2C+CTFs%2C+Research+%26+Authorized+Assessments" alt="AxionR animated footer">

<br><br>

<sub>AxionR v2.0.0 · Built for authorized security testing.</sub>

</div>
