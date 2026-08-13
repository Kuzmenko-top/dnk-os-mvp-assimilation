# --- DNK-MRH-HEADER ---
# mrh_id: "DNK-COMP-013_google-skills-contracts"
# purpose: "Component contracts and schema definitions for Google Skills Standard in DNK OS"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-13"
# --- END DNK-MRH-HEADER ---

# DNK-COMP-013: Google Skills Component Contracts

## 1. Skill Metadata Frontmatter Contract (YAML Schema)
```yaml
name: string             # Required: unique skill identifier
description: string      # Required: concise overview
version: string          # Required: semver (e.g. "1.0.0")
category: string         # Required: taxonomy classification
tags: list[string]       # Optional: tags for indexing
author: string           # Required: author attribution
triggers: list[string]   # Required: intent matching keyphrases
inputs_schema: dict      # Optional: JSON Schema of skill inputs
outputs_schema: dict     # Optional: JSON Schema of skill outputs
```

## 2. Mandatory Markdown Section Contract
```markdown
# Skill Title

## Overview
Brief explanation of what this skill accomplishes.

## Core Specifications
Links to relevant RN-XXX, DNK-ARCH-XXX, and DNK-COMP-XXX specifications.

## Intent & Triggers
List of prompt intent patterns and trigger rules for dynamic selection.

## Input / Output Contracts
Description or JSON Schema for inputs and expected outputs.

## Quick Recipes & Execution Flow
Step-by-step code snippets or actionable procedures.

## Pitfalls & Error Handling
Edge cases, failure modes, and recovery procedures.
```
