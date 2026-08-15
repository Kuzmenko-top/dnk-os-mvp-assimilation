# author: "DNK-e.com Maksym"
# Architecture Health Score

## Overview
The Architecture Health Score (0-100) measures DNK OS architecture quality dynamically across documentation, testing, debt management, and component compatibility.

## Components
- **ADR Coverage (30%)**: % of patterns with ADR documentation
- **Test Coverage (30%)**: % of patterns with regression tests
- **Tech Debt Ratio (25%)**: % of patterns without open tech debt
- **Compatibility Score (15%)**: % of compatible components

## Thresholds
- **Excellent (90-100)**: Production-ready, best practices
- **Good (75-89)**: Production-ready, minor improvements needed
- **Fair (60-74)**: Needs improvements before production
- **Poor (<60)**: Not production-ready

## Usage
```bash
python scripts/calculate_arch_health.py
```

## CI/CD Gate
- Minimum score for merge: 75
- Minimum score for production: 85
