# GitHub Workflow & Integration Guidelines

**Project:** OmniSight: Multimodal UI Self-Healing & RPA Agent  
**Working Branch:** `feature/Hardev`

---

## 1. Branch Strategy

```
main (Base / Target Branch)
  ^
  | (Pull Request via GitHub API)
  |
feature/Hardev (Active Working Branch)
  ^
  | (Automated Self-Healing PR Branches)
  |
fix/omnisight-healing-<timestamp> (Proposed Branch Naming Convention)
```

- **`main`**: Target integration branch.
- **`feature/Hardev`**: Active working branch preserved for developer workflow.
- **Automated Fix Branches:** Created by the CI/CD Gateway when generating self-healing Pull Requests.

---

## 2. GitHub Integration Flow (Week 3 Requirement)

As specified in the official Week 3 deliverables:

1. **Trigger:** An anomaly is detected by the VLM Engine and a CSS/React fix is applied.
2. **Verification:** Headless Navigator takes a new screenshot and the VLM verifies the repair.
3. **Branching:** CI/CD Gateway creates a dedicated Git branch.
4. **Commit:** CI/CD Gateway commits the verified code fix.
5. **Pull Request:** CI/CD Gateway opens a Pull Request on GitHub.

---

## 3. Working Principles

- Maintain active development on `feature/Hardev`.
- Do not make fake or meaningless commits.
- Ensure all automated PRs created by the gateway include diagnostic context and verification evidence.
