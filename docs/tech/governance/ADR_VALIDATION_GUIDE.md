# author: "DNK-e.com Maksym"
# ADR Validation Guide

## Overview
All Architecture Decision Records (ADR) must pass validation before being merged into `main`.

## Required Sections
- **Status**: Proposed, Accepted, Deprecated, Superseded, or Rejected
- **Context**: Problem description and background
- **Decision**: Selected architectural option
- **Alternatives Considered**: Numbered list of options evaluated (at least 1)
- **Consequences**: Positive outcomes (`### Positive` or `✅`) and negative trade-offs (`### Negative` or `⚠️`/`❌`)
- **Dependencies**: Related system components or services
- **Date**: Date in `YYYY-MM-DD` format
- **Owner**: Assigned engineer or domain owner

## Usage
```bash
# Validate all ADRs
python scripts/validate_adr.py

# Validate single ADR
python scripts/validate_adr.py docs/tech/adr/ADR-001_vllm-paged-attention.md
```

## CI/CD
ADR validation runs automatically on PRs and pushes to `main`.
