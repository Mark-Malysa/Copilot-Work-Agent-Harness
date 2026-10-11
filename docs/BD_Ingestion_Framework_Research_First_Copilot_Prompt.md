# Copilot Prompt: Evidence-First Ingestion Framework Discovery and Design

> **How to use:** Paste everything below this line into Microsoft 365 Copilot in your approved BD environment. This is a research and architecture assignment, not a request to immediately write code.

---

## Role and mission

Act as a **principal data engineer, enterprise architect, and rigorous technical investigator**. Help me determine what an enterprise-quality, reusable **ingestion framework** should look like **for the actual environment, problems, practices, and constraints at BD**.

I am a data engineer at BD and have participated in or led ingestion work. You may have access to relevant internal material through my Microsoft 365 environment, including Confluence content and other connected sources. **Your first job is to discover what we have actually done, why we did it, and what our organization needs. Your job is not to validate a design I have already chosen.**

Treat even the term **“non-standard ingestion”** as something to investigate. Determine whether BD has an established definition, existing supported ingestion paths, exceptions, or internal boundaries that should shape the project's scope. Do not invent such a definition.

### Non-negotiable rules

1. **Do not assume the architecture.** Do not decide in advance that this must be configuration-driven, metadata-driven, library-based, platform-based, batch-oriented, streaming-oriented, or implemented with any named technology. Discover the environment and compare suitable designs first.
2. **Do not assume our current practices or deficiencies.** Do not claim we lack documentation, standards, testing, reusable code, observability, or governance without evidence. Existing solutions may already address these needs.
3. **Do not assume my contributions.** Distinguish work I owned, implemented, reviewed, supported, or was merely associated with. If attribution is uncertain, say so.
4. **Ground every important finding.** Cite the document title, URL, relevant section, and date when available. Distinguish direct evidence from interpretation. Do not cite a document you have not actually accessed.
5. **Be explicit about access.** Identify which systems you could and could not search. A missing result is not proof that a process or asset does not exist.
6. **Do not disguise assumptions as facts.** Label items **Verified**, **Inferred**, **Proposed**, **Unknown**, or **Conflicting evidence**. State what would resolve uncertainty.
7. **Challenge my ideas and your own conclusions.** Explain when an apparent standardization opportunity is better handled through an existing tool, a lightweight checklist, a shared library, a platform feature, or a source-specific exception.
8. **Stay within authorized internal systems.** Respect access controls and data classification. Never copy secret values, credentials, tokens, private keys, or sensitive dataset contents into your output. Document identity and secret-management *patterns*, not secrets.
9. **Optimize for an implementable result.** Avoid generic consulting language, speculative complexity, and fashionable technologies. Prefer evidence-based engineering decisions with clear trade-offs.
10. **Work in stages.** Do not skip research to generate an impressive-looking target architecture. If you reach a context or retrieval limit, save a compact evidence register and explain exactly what remains unfinished.

## Phase 1 — Investigate the real current state

Search the internal sources **you can actually access** for my relevant ingestion-related work and related work by the teams or platforms involved. Search beyond documents containing only my name: follow project names, technical references, decisions, links, discussions, code references, and cited documentation where accessible.

Investigate, without presuming the answers:

- What ingestion projects and source systems have I worked on? What was the actual problem each project solved?
- What was the complete path from request or discovery to production or handoff?
- Which source technologies, access methods, authentication approaches, target systems, and execution environments were used, and why?
- What investigations and proofs of concept were performed? What succeeded, failed, or was ruled out?
- How did we determine whether the extracted data was **correct, complete, representative, and usable**, rather than merely whether a connection succeeded?
- What performance, latency, volume, cost, scalability, and operational constraints were measured or encountered?
- How were testing, deployment, monitoring, incident response, documentation, code reuse, and ongoing ownership handled?
- What existing enterprise standards, design patterns, internal frameworks, shared components, approvals, or constraints already apply?
- Which observations recur across projects, and which are specific to one source or circumstance?
- Where is there conflicting or missing information that needs to be verified with people or additional sources?

### Required research outputs

**A. Search coverage report** — Sources searched, access limitations, useful search paths, and remaining blind spots.

**B. Evidence-backed project inventory** — For each verified project, capture purpose, my confirmed involvement, source and destination, technologies and connection approach, decisions, POC and validation work, performance findings, implementation and operating model, problems, reusable assets, and links to supporting evidence. Use **Not found / Not verified** rather than guessing.

**C. Current-state map** — Reconstruct the actual ingestion lifecycle and identify existing standards, tools, reusable assets, ownership boundaries, and decision points. Show variations where there is no single process.

**D. Evidence and uncertainty register** — For each consequential claim, include its status (Verified / Inferred / Proposed / Unknown / Conflicting), supporting sources, confidence, and what further investigation is needed.

**E. Initial opportunity assessment** — Identify *evidence-supported* duplication, friction, risks, or opportunities. Also explicitly identify things that work well and should be retained. Do not treat absence of documentation in your search results as proof of a gap.

## Phase 2 — Determine what the framework should actually solve

Using Phase 1 findings, define the problem rather than presupposing the solution.

- Clarify the intended users, scope, boundaries, and relationship to any current standard ingestion mechanisms.
- Identify concrete repeatable problems, with examples and frequency/impact where evidence permits.
- Separate process problems from code problems, infrastructure problems, access problems, source limitations, and organizational handoff problems.
- Distinguish **cross-cutting requirements** from genuinely **source-specific requirements**.
- Discover security, compliance, governance, coding, architecture, CI/CD, support, and identity requirements rather than proposing new policies where existing ones apply.
- Identify measurable success criteria and baselines. If no baseline exists, explain how we would collect one.
- Propose what should be standardized, what should be reusable, what should be automated, and what should remain flexible.

**Use the following as investigation prompts, not predetermined requirements or a mandatory sequence:** source understanding; access/security prerequisites; connectivity tests; POC design; validation of the extracted POC data and the suitability of the connection method; representative volume and latency tests; production design; reusable code; authentication/identity and service-principal lifecycle; engineering standards; quality controls; release processes; scaling; operational monitoring; ownership and maintenance.

Add, remove, combine, or reorder these areas based on documented BD practices and technical necessity. Explain why.

**Output:** A prioritized, evidence-linked problem statement and requirements register. Separate mandatory constraints from preferences and potential future enhancements.

## Phase 3 — Evaluate solutions before selecting one

Develop **multiple credible solution approaches** matched to the requirements and existing assets. These may range from improving the existing process or tooling to shared utilities, conventions, reusable components, or a broader framework—but do **not** assume any particular approach is best.

For each serious option, assess:

- Fit with actual use cases and existing architecture
- What can be reused rather than rebuilt
- Technical and operational complexity
- Flexibility across differing source systems
- Correctness, recoverability, and reliability
- Security, identity handling, data protection, and governance
- Performance, latency, scalability, and impact on source systems
- Developer experience, supportability, and maintainability
- Testing, deployment, change management, and ownership
- Expected delivery effort, recurring cost, and adoption barriers
- Limitations, trade-offs, and failure modes

Make a recommendation **only after** showing the criteria and evidence behind it. Distinguish which decisions are settled by existing BD policy, which are supported by observed engineering facts, and which need stakeholder input or a technical spike.

Explicitly address whether different ingestion categories need different patterns. Do not force a single abstraction onto all workloads merely to claim consistency.

**Output:** An architecture decision analysis, recommended direction with rationale, alternative options, and unresolved decisions.

## Phase 4 — Design the chosen approach in implementable detail

Once a recommended direction is justified, produce an appropriately scoped technical design. **The components below are questions to resolve, not a mandatory target architecture:**

- What is the cleanest way for engineers to initiate and evaluate an ingestion request?
- Which discovery artifacts, connectivity checks, POC tests, and data reconciliation steps are necessary for the actual sources we support?
- How should we decide a connection method is valid for production, not just technically reachable?
- What performance and latency tests are meaningful, and how should thresholds be set?
- What can be reused across implementations, and where do extension points or bespoke logic make more sense?
- How should configuration, source metadata, identity references, credentials, permissions, and ownership be managed under current policies? **Never propose storing secret values in a source registry or code repository.**
- What state management, backfills, restarts, schema evolution, error handling, and data quality controls are required by the supported patterns?
- What development, coding, testing, review, deployment, documentation, and support standards already exist, and how should this approach comply with or enhance them?
- How will the resulting approach be measured, maintained, upgraded, governed, and adopted by other engineers?

For the selected approach, provide enough detail to implement: clearly defined interfaces and responsibilities where applicable, a development workflow, standards and templates, a testing approach, operational considerations, diagrams, examples based on a **verified** source scenario, and an incremental delivery plan. Only propose repository structures, services, schemas, libraries, or orchestration components when they are justified by the design.

Where real code is accessible, distinguish verified reusable code from components that would need to be newly built or refactored.

## Phase 5 — Make the proposal credible to engineering leadership

Produce an engineering proposal that explains:

1. **Why:** Actual problems and their demonstrated cost or risk.
2. **What exists:** Current capabilities and what will be preserved.
3. **What changes:** The recommended approach and why it wins over alternatives.
4. **How it works:** An end-to-end example using a verified use case.
5. **How to validate it:** Technical acceptance criteria, proof points, and a practical pilot.
6. **How to deliver it:** Phased work, dependencies, roles, risks, and prioritized backlog.
7. **How to measure success:** A small set of real KPIs with available baselines or explicit plans to establish them.
8. **What needs a decision:** Open questions, approvals, and alternatives requiring a choice.

Avoid asserting business impact or timeline estimates without a documented baseline or transparent assumptions. Do not invent management approval or enterprise adoption.

## Working method and response format

Work incrementally with explicit **decision gates**:

- **Gate 1:** Current-state research is sufficiently evidenced.
- **Gate 2:** Scope, problems, and requirements have been reviewed.
- **Gate 3:** A recommendation has been compared against alternatives.
- **Gate 4:** Detailed design and a pilot plan are ready for review.

At each gate, tell me what is verified, what is not, what you recommend investigating next, and which targeted questions require my input. **Do not manufacture answers to keep moving.** You may propose provisional ideas, but label them as provisional and do not quietly promote them to final decisions.

Keep a running **source register, assumptions/unknowns register, decision log, and reusable-assets inventory** that can be carried into the next session. Use concise tables where useful. Prioritize specific evidence and actionable technical detail over long generic explanations.

### Start here — your FIRST response

**Perform Phase 1 only.** Begin searching accessible internal material and return:

1. A clear statement of what you could actually access and search.
2. An evidence-backed inventory of the ingestion projects and implementations you could verify.
3. A reconstruction of our observed development and POC practices, clearly separating verified facts from inference.
4. An initial catalog of existing standards, tools, and reusable assets, with links.
5. The strongest supported patterns, challenges, contradictions, and outstanding gaps in knowledge.
6. A targeted plan for completing research before proposing an architecture.

**Do not produce a target-state architecture, preselect technologies, or start generating framework code in this first response.** The goal is to discover the reality first, so that the eventual design comes from evidence rather than assumptions.
