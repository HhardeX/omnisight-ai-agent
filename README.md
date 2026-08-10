# OmniSight: Multimodal UI Self-Healing & RPA Agent

> **Infotact Solutions -- Generative AI Project**

OmniSight is an intelligent, multimodal agentic platform designed for automated visual UI testing, visual anomaly detection, self-healing UI repairs, and Robotic Process Automation (RPA). By combining Playwright browser automation with Vision-Language Models (VLMs) and Agentic Orchestration, OmniSight automatically detects visual regressions, generates UI code fixes, verifies fixes, and integrates into CI/CD pipelines via GitHub pull requests.

---

## Architecture & Core Modules

OmniSight is structured around four major core modules specified by the Infotact Solutions project document:

```
+-----------------------------------------------------------------+
|                       CI/CD Gateway                             |
|             (FastAPI + GitHub Integration)                      |
+-------------------------------+---------------------------------+
                                |
                                v
+-------------------------------+---------------------------------+
|                      Agentic Orchestrator                       |
|                     (LangChain / AutoGen)                       |
+-------------------------------+---------------------------------+
                                |
                +---------------+---------------+
                |                               |
                v                               v
+-------------------------------+ +-------------------------------+
|      Headless Navigator       | |   Vision-Language Model       |
|     (Playwright + Python)     | |         (VLM) Engine          |
+-------------------------------+ +-------------------------------+
```

1. **Headless Navigator (Playwright + Python)**
   - Controls browser automation, page navigation, and DOM state collection.
   - Captures responsive screenshots across multiple viewports.

2. **Vision-Language Model (VLM) Engine**
   - Performs multimodal evaluation of rendered screenshots alongside HTML/DOM state.
   - Performs visual anomaly detection.
   - Extracts generated CSS/React code fixes.

3. **Agentic Orchestrator (LangChain / AutoGen)**
   - Manages state machine and self-healing loop execution.
   - Coordinates re-navigation, patch application, re-screenshot verification, and post-fix evaluation.

4. **CI/CD Gateway (FastAPI + GitHub Integration)**
   - Accepts CI/CD webhooks.
   - Handles GitHub branch creation, commit creation, and automated Pull Requests.
   - Provides a React QA Dashboard.

---

## Official 4-Week Development Plan

| Week | Focus Area | Official Deliverables |
| :--- | :--- | :--- |
| **Week 1** | **Headless Navigator & Gateway** | Playwright browser automation, responsive screenshots, FastAPI webhook receiver. |
| **Week 2** | **VLM & Visual Analysis** | VLM integration, screenshot + HTML analysis, visual anomaly detection, extraction of generated CSS/React fixes. |
| **Week 3** | **Self-Healing & GitHub Pipeline** | Self-healing loop, apply generated fix, screenshot again, VLM verification, GitHub branch, commit and pull request integration. |
| **Week 4** | **Optimization & Dashboard** | Image chunking/cropping optimization, React QA dashboard, final refinement. |

---

## Project Documentation

Detailed specifications and architectural guides are located in the [`docs/`](file:///h:/PROJECTS/omnisight-ai-agent/docs) directory:

- [Project Specification (`docs/PROJECT_SPEC.md`)](file:///h:/PROJECTS/omnisight-ai-agent/docs/PROJECT_SPEC.md) -- Core module requirements vs. proposed implementation details.
- [Development Plan (`docs/DEVELOPMENT_PLAN.md`)](file:///h:/PROJECTS/omnisight-ai-agent/docs/DEVELOPMENT_PLAN.md) -- Official 4-week roadmap breakdown.
- [GitHub Workflow (`docs/GITHUB_WORKFLOW.md`)](file:///h:/PROJECTS/omnisight-ai-agent/docs/GITHUB_WORKFLOW.md) -- Branching strategy and PR integration flow.

---

## Working Branch Notice

Active working branch: `feature/Hardev`.
