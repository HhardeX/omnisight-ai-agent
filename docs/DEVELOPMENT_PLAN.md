# Official 4-Week Development Plan: OmniSight

**Project:** OmniSight: Multimodal UI Self-Healing & RPA Agent  
**Framework:** Infotact Solutions Official Project Plan

---

## 4-Week Roadmap Summary

```
Week 1: Playwright + Screenshots + FastAPI Webhook
  |
  v
Week 2: VLM Integration + Screenshot/HTML Analysis + Anomaly Detection + Fix Extraction
  |
  v
Week 3: Self-Healing Loop + Apply Fix + Re-screenshot + VLM Verification + GitHub Integration
  |
  v
Week 4: Image Chunking/Cropping Optimization + React QA Dashboard + Final Refinement
```

---

## Week 1: Headless Navigator & Gateway Foundation

### Official Deliverables
- Playwright browser automation
- Responsive screenshots
- FastAPI webhook receiver

### Proposed Task Breakdown (Implementation Details)
- [ ] Initialize Python Playwright browser engine.
- [ ] Configure screenshot capture module for responsive viewports.
- [ ] Create FastAPI endpoint to receive incoming webhooks.
- [ ] Implement DOM HTML snapshot serializing helper.

---

## Week 2: Vision-Language Model Integration & Visual Analysis

### Official Deliverables
- VLM integration
- Screenshot + HTML analysis
- Visual anomaly detection
- Extraction of generated CSS/React fixes

### Proposed Task Breakdown (Implementation Details)
- [ ] Set up VLM API client interface.
- [ ] Build prompt pipeline combining rendered screenshot images with HTML DOM text.
- [ ] Implement visual anomaly detection output parser.
- [ ] Implement CSS/React code block extractor for patch application.

---

## Week 3: Self-Healing Loop & GitHub Pipeline Integration

### Official Deliverables
- Self-healing loop
- Apply generated fix
- Screenshot again
- VLM verification
- GitHub branch, commit and pull request integration

### Proposed Task Breakdown (Implementation Details)
- [ ] Build Agentic Orchestrator execution loop (LangChain / AutoGen).
- [ ] Implement patch applier to inject generated CSS/React changes.
- [ ] Trigger re-screenshot and secondary VLM verification pass.
- [ ] Integrate GitHub API for automated branch creation, commit pushing, and Pull Request creation.

---

## Week 4: Optimization, React QA Dashboard & Final Polish

### Official Deliverables
- Image chunking/cropping optimization
- React QA dashboard
- Final refinement

### Proposed Task Breakdown (Implementation Details)
- [ ] Implement image chunking and region-of-interest cropping for large or scrollable pages.
- [ ] Develop React QA Dashboard UI for viewing test runs, visual diffs, and PR statuses.
- [ ] Perform end-to-end testing and final system refinement.
