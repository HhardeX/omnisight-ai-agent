# Project Specification: OmniSight AI Agent

**Project:** OmniSight: Multimodal UI Self-Healing & RPA Agent  
**Framework:** Infotact Solutions Project Requirement Specification

---

## 1. Overview

OmniSight is an autonomous agent system for visual UI testing, visual anomaly detection, self-healing UI repair, and RPA workflows. The system integrates browser automation, Vision-Language Models (VLMs), agentic orchestration, and CI/CD gateway integrations.

---

## 2. Core Modules (Official Infotact Requirements vs. Proposed Implementation Details)

### Module 1: Headless Navigator
- **Official Infotact Requirement:**
  - Playwright + Python browser automation.
  - Responsive screenshot capture across multi-device viewports.
  - Page navigation and HTML/DOM state extraction.
- **Proposed Implementation Details (Not Infotact Requirements):**
  - Proposed viewport size defaults: Mobile (375x812), Tablet (768x1024), Desktop (1920x1080).
  - Proposed bounding box mapping for interactive elements.

### Module 2: Vision-Language Model (VLM) Engine
- **Official Infotact Requirement:**
  - VLM integration for visual + HTML/DOM paired analysis.
  - Visual anomaly detection (identifying UI bugs, alignment issues, layout regressions).
  - Extraction of generated CSS/React fixes to heal broken components.
- **Proposed Implementation Details (Not Infotact Requirements):**
  - Proposed choice of multimodal model providers (e.g. OpenAI / Anthropic / Local VLM APIs).
  - Proposed custom prompt templates and structured JSON schema outputs.

### Module 3: Agentic Orchestrator
- **Official Infotact Requirement:**
  - LangChain / AutoGen agentic orchestration.
  - Multi-step self-healing loop execution:
    1. Capture broken UI state and DOM via Headless Navigator.
    2. Analyze state with VLM Engine.
    3. Apply generated CSS/React fix.
    4. Re-screenshot patched UI.
    5. Perform VLM verification of post-fix state.
- **Proposed Implementation Details (Not Infotact Requirements):**
  - Proposed retry count limits and visual confidence threshold scoring metrics.
  - Proposed memory persistence mechanisms (Redis or SQLite execution state store).

### Module 4: CI/CD Gateway
- **Official Infotact Requirement:**
  - FastAPI integration for webhook event reception.
  - Automated GitHub branch creation, commit assembly, and Pull Request submission for verified fixes.
  - React QA Dashboard (Week 4 deliverable).
- **Proposed Implementation Details (Not Infotact Requirements):**
  - Proposed REST API payload schemas for webhooks.
  - Proposed React component hierarchy and frontend state management library choices.

---

## 3. High-Level Data Flow (ASCII Diagram)

```
[ CI/CD Webhook / Trigger ]
            |
            v
+-----------------------+
|    FastAPI Gateway    |
+-----------+-----------+
            |
            v
+-----------------------+
|  Agentic Orchestrator | <---------------------------------+
+-----+-----------+-----+                                   |
      |           |                                         |
      v           v                                         |
+-----------+ +-----------+                                 |
| Headless  | |    VLM    |                                 |
| Navigator | |  Engine   |                                 |
+-----+-----+ +-----+-----+                                 |
      |             |                                       |
      +------+------+                                       |
             |                                              |
             v                                              |
+-----------------------+                                   |
|   Self-Healing Loop   | (If fix unverified / re-evaluate) |
| (Apply Fix & Re-scan) +-----------------------------------+
+-----------+-----------+
            | (If verified)
            v
+-----------------------+
|  GitHub Branch & PR   |
|   + React QA Board    |
+-----------------------+
```
