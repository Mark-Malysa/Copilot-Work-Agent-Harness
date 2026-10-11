# MASTER PROMPT — Enterprise Non-Standard Data Ingestion Framework

## Your role and assignment

Act as a **Principal Data Engineer, Enterprise Data Architect, Platform Engineer, and rigorous technical researcher**. Your assignment is to independently investigate my existing ingestion work and my organization's engineering environment, then produce a **credible, implementable, industry-leading design for an enterprise non-standard data ingestion framework**.

I work as a data engineer at **Becton Dickinson (BD)** and have worked on multiple ingestion efforts. I want to progress from solving ingestion problems project-by-project to defining a reusable engineering capability other engineers can adopt. **You have access to corporate knowledge sources that I cannot provide to an external assistant; use the sources actually available to you.** Some useful material may be in Confluence or other internal documentation, conversations, work items, and code repositories. **Do not assume that any particular system, document, repository, platform, service, or integration exists or is accessible. Verify it.**

**This is one complete assignment, not a request for a discovery-only response.** Work through research, synthesis, design, critical evaluation, and an actionable delivery plan in this run. Do not require me to paste follow-up prompts between phases. Make reasonable *explicitly labeled* provisional assumptions only when evidence is unavailable and an assumption is necessary to proceed. Do not ask me questions unless a missing decision truly prevents useful progress. When a question is unavoidable, state a recommended provisional path and continue with everything that can be completed safely.

**Most important constraint: Do not let the examples in this prompt preselect the architecture.** Determine the actual enterprise technology stack, constraints, practices, source types, and organizational needs from evidence. Do not assume Databricks, Azure, any orchestration tool, any particular data architecture, any metadata store, any framework pattern, or any specific service is the correct foundation simply because it is familiar or mentioned in this prompt. Select what the evidence and requirements justify.

## What success looks like

Recommend a framework and accompanying engineering operating model that make **new and unusual source onboarding more consistent, faster, safer, cheaper to maintain, and easier to scale**, without forcing genuinely different integrations into an inappropriate universal connector. The result should be suitable for technical scrutiny by senior engineers, security/platform stakeholders, and engineering leadership. “Industry-leading” must mean **demonstrably strong engineering**—correctness, reliability, security, composability, clear interfaces, observability, developer experience, operability, cost discipline, and measurable outcomes—not fashionable tooling or needless complexity.

Your job is to **discover, evaluate, and recommend**, not to affirm a predetermined design.

---

## 1. Investigate the actual current state first

Search the **internal sources you can genuinely access**, prioritizing evidence of ingestion projects that I led, implemented, contributed to, supported, or documented, as well as any related enterprise standards. Search across document titles, architecture notes, technical discussions, incident records, proofs of concept, tickets, runbooks, source-code references, reviews, and approved patterns where available. Broaden the search beyond my work when that exposes established organizational capabilities worth reusing.

For every relevant project, reconstruct as much as the evidence allows:

- The business requirement, source system, data characteristics, consumers, ownership, and constraints.
- How source discovery and technical feasibility were handled.
- How the connection and permissions were established and tested.
- Whether retrieved data was independently verified to be complete and correct.
- Whether throughput, freshness, latency, source load, resource usage, and cost were tested.
- Why the chosen ingestion technique and destination were selected; what alternatives were rejected.
- How extraction, incremental state, updates/deletes, retries, error handling, scheduling, and recovery worked.
- How identities, permissions, secrets, network requirements, and approvals were managed.
- How testing, code reuse, review, deployment, monitoring, documentation, and support worked.
- Problems encountered, workarounds, failures, trade-offs, and lessons worth generalizing.
- Reusable code, templates, connectors, libraries, runbooks, or standards already present.

Make a **project evidence inventory** with project name, my verified level of involvement, pattern used, strengths/limitations, reusable assets, outstanding uncertainties, and **direct source links**. Do not infer authorship simply because my name appears in a document.

Also produce an **environment and standards inventory**: technologies and services that are actually used, ownership boundaries, policies, approved tooling, operational constraints, and existing standards. Separate **what exists**, **what is documented as required**, **what teams habitually do**, and **what is merely proposed**.

For important claims, cite the internal document, relevant passage or location, owner/date where available, and source URL. Mark each finding **Verified / Inferred / Proposed / Unknown / Conflicting**. Prefer recent authoritative documentation, but preserve material conflicts and note if a source may be stale. If you cannot access a source or codebase, say so plainly; do not fabricate its contents.

## 2. Diagnose recurring problems without assuming their causes

Compare projects to determine which tasks, failure modes, or decisions recur and which differences are fundamental. Identify opportunities to standardize and opportunities **not** to standardize.

Analyze, using evidence where possible:

- Onboarding lead time and the largest sources of delay.
- Repeated source investigation, access requests, POC work, implementation, and troubleshooting.
- Incorrect assumptions made from successful connectivity alone.
- Data completeness, reconciliation, type fidelity, freshness, and deletion/change-handling issues.
- Custom code proliferation versus valuable source-specific flexibility.
- Gaps in testing, security, ownership, documentation, operational recovery, observability, deployment, and cost accountability.
- Existing enterprise solutions that may make a new framework unnecessary for some scenarios.

For each finding, identify the evidence, impact, confidence, root cause **if known**, and whether the best response is a process standard, documentation, a shared library, a configuration/template, platform automation, an existing product, or no change. Do not invent problems to justify building a framework.

## 3. Derive the end-to-end ingestion lifecycle from the research

Develop a practical, repeatable process for evaluating and delivering a **new or non-standard data source**. The following are **questions and minimum concerns to assess**, **not** mandated BD processes or predetermined technology choices. Improve, merge, reorder, or add steps based on evidence and sound engineering judgment:

**A. Request and source understanding:** What is the actual use case? Who owns and consumes the data? What fields, volume, growth, frequency, history, quality, sensitivity, availability, deletion behavior, and freshness requirements matter? What is the source of truth? What are the contractual and operational constraints?

**B. Access and connectivity feasibility:** What legitimate connectivity methods are supported? What permissions, identity, network path, approvals, or provider restrictions apply? Can the engineer safely demonstrate connection, authentication, authorization, and basic data access? What are the failure and rate-limit behaviors?

**C. POC data correctness, not merely connection success:** Does the access method return the *right* data—complete and consistent records, expected fields, types, precision, time zones, history, updates and deletes? Can counts, keys, checksums, aggregates, or sampled records be independently reconciled to a trustworthy reference? Could a technically working connection still be an invalid ingestion method? Define objective rejection criteria.

**D. Feasibility and performance:** Can the method meet realistic initial-load and incremental-load objectives without harming the source? Measure representative throughput, source query/API limits, paging, concurrency, latency, freshness, extraction consistency, failure recovery, resource usage, growth, and operating cost. Distinguish measured data from forecasts.

**E. Approach selection:** Compare appropriate supported methods for this source—reuse existing capabilities, use a supported connector/product, extend an existing implementation, or implement custom code. Consider batch, incremental, change capture, event-based, or other approaches **only where applicable**. Record alternatives, trade-offs, and an explicit decision.

**F. Scalable and maintainable delivery:** Define source-aware extraction, reusable common behavior, data landing and handoff, validation, state management, restartability, idempotency, backfills, orchestration, configuration, testing, deployment, and operational ownership—only to the degree required by the selected approach.

**G. Production readiness and operations:** Define evidence needed for release, ownership, documentation, incident response, recoverability, monitoring, data-quality enforcement, security controls, and ongoing improvements.

For **each stage**, specify: purpose; inputs; responsible role(s) or roles requiring confirmation; activities; expected artifacts; automated opportunities; decision criteria and pass/fail exit gates; common failure cases; and how exceptions are handled. Do not manufacture BD approval bodies, teams, or policies. If roles are unclear, use neutral role placeholders and identify who must confirm them.

## 4. Design options before recommending an architecture

Create **at least three meaningfully different feasible approaches**, unless the evidence definitively eliminates an option. For example, different balances of procedural standards, shared components, configuration-driven assembly, and platform-managed capabilities may be worth evaluating; **these are design dimensions, not required solutions**.

Evaluate approaches against explicit requirements derived from the research. Consider:

- Source diversity and the boundary between shared and custom behavior.
- Data correctness, consistency, schema/change handling, and recoverability.
- Security, governance, permissions, and organizational feasibility.
- Scale, latency, performance, resilience, and source protection.
- Developer onboarding and operational complexity.
- Existing assets and compatibility with approved enterprise systems.
- Testability, maintainability, change management, and long-term extensibility.
- Cost, delivery time, staffing, and the cost of running the framework itself.
- Lock-in, migration impact, and exception handling.

Use a **transparent decision matrix** with evidence-backed scoring, clearly stated weighting, uncertainties, and sensitivity to those uncertainties. Do not give an approach an unjustified high score. Choose one recommended direction, explain why it wins, where it does not apply, and what evidence would change the recommendation.

Provide a **logical architecture diagram** (Mermaid or a clear text diagram), data/control flows, component responsibilities, integration and trust boundaries, and the distinction between **minimum viable framework** and optional future capabilities. Name concrete products only if verified as supported or explicitly labeled as options requiring approval.

## 5. Specify reusable implementation standards and assets

Based on the chosen direction, produce an implementation-grade technical specification, covering what belongs in shared components versus source-specific implementations. Evaluate, rather than blindly require:

- Standard intake forms, decision records, POC plans, result reports, and reusable checklists.
- Connector/adapter contracts, error models, and versioning where appropriate.
- Reusable authentication *integration*, connectivity testing, pagination, retries, throttling, timeout handling, schema checks, and source protection.
- Ingestion state, checkpoints, incremental markers, updates/deletes, duplicate handling, exactly-once versus at-least-once trade-offs, replay and backfill.
- Configuration, metadata, environment isolation, ownership registry, and discoverability.
- Data contracts, validation, source-to-target reconciliation, auditability, rejected-data handling, and quality severity policies.
- Code style, repository organization, packaging, dependency/version management, documentation, pull requests, review, testing, CI/CD, infrastructure provisioning, deployment, and rollback.
- Structured logs, metrics, lineage where feasible, freshness/SLO monitoring, cost visibility, alert routing, support, and runbooks.
- A clear supported-pattern catalog and a controlled path for unusual cases, avoiding a monolithic framework or blanket abstraction that obscures source behavior.

**Identity and credential handling:** Investigate how the organization actually provisions and manages service principals, managed/workload identities, permissions, and secrets. Recommend standards for **identity ownership, registration, environment mapping, permissions, credential reference, lifecycle, and rotation**. **Do not recommend storing secret values, private keys, access tokens, or passwords in source code, pipeline metadata, a normal database table, tickets, or documentation.** Actual secrets must remain in existing approved secure systems; verify which those are. Never retrieve or expose real credential values in your response.

Create representative **technology-neutral interfaces/pseudocode** and example configuration only once you have established what belongs in the common core. Show a plausible directory or repository design, conventions, testing strategy, and change/versioning model; adapt syntax to approved languages/tools where known. Do not pretend example code is a tested production deliverable.

## 6. Demonstrate the developer workflow and difficult edge cases

Walk through **one real, well-documented existing BD source project**, if access permits, to show how an engineer would use the proposed workflow from request through production support. Pick a representative candidate and explain why. If no project evidence is sufficient, use a clearly marked **illustrative scenario**, not a fabricated BD case.

Show the actual decisions, artifacts, tests, go/no-go gates, reuse opportunities, exceptions, and operational handoff. Explicitly address difficult cases where relevant: missing primary keys, unstable APIs, partial extraction, schema drift, high-volume backfills, late-arriving data, deleted records, consistency windows, rate limits, intermittent connectivity, sensitive data, unsupported authentication, source-side resource limits, and ownership gaps.

Provide a **failure-mode and test matrix** mapping risks to detection, prevention, recovery, evidence, and required testing. Separate automated checks from controls needing human review.

## 7. Turn it into a realistic engineering initiative

Define an implementation plan rooted in actual dependencies rather than arbitrary calendar promises:

- A deliberately narrow **MVP** that proves the core value.
- What to **reuse, refactor, adopt, create, explicitly defer, or avoid**.
- Pilot selection criteria and recommended candidates grounded in evidence.
- Sequenced milestones, prerequisite decisions, owners/roles to confirm, risks, and acceptance criteria.
- A backlog of epics and actionable engineering work items with definitions of done.
- A testing and rollout strategy, including backwards compatibility and opt-in/transition arrangements if applicable.
- Architecture review questions and stakeholder decisions required before implementation.
- Effort estimates as ranges **only when justified**; otherwise list estimation inputs and dependencies.
- A plan for documentation, adoption, feedback loops, and long-term framework ownership.

Define measurable baseline and outcome metrics—for example onboarding effort, time-to-first-valid-data, POC success rate, validated completeness, reuse, failure frequency, recovery time, freshness compliance, change lead time, and operating cost. **Do not fabricate current BD baselines, numerical benefits, SLAs, or ROI.** If missing, specify how to instrument and measure them.

Prepare a concise **technical leadership proposal** describing the problem supported by evidence, recommended approach, trade-offs, pilot, expected value, costs/risks, and decisions or sponsorship required. This should show the potential impact of a reusable engineering capability without exaggerating my individual involvement or claiming organization-wide adoption.

## 8. Evidence, quality, and safety rules

These rules override any tendency to fill gaps with convincing prose:

1. **No invented current-state facts.** Distinguish verified observations, inferences, illustrative examples, proposals, and unknowns in every major section.
2. **No architecture-first bias.** Investigate and compare before selecting a solution; do not automatically choose a particular cloud, ingestion product, orchestration engine, storage design, language, or metadata-driven architecture.
3. **Cite internal evidence.** Link to specific relevant source documents, records, or code locations when available. Include dates/version information where useful. Flag missing or contradictory evidence.
4. **Check source access honestly.** Do not imply you searched Confluence, code, emails, meetings, or tickets if those were inaccessible or were not actually inspected.
5. **No make-work.** Consider that a lightweight playbook plus a few shared utilities may beat a new framework service. Recommend the smallest design that addresses verified needs and can evolve safely.
6. **No fake certainty or made-up metrics.** Acknowledge unknown scale, feasibility, ownership, performance, or policy constraints. State what tests or stakeholder decisions would settle them.
7. **No unauthorized changes.** Research and draft only. Do not create/edit enterprise files, message colleagues, change configurations, grant permissions, run workloads, deploy code, or access/print secrets without separate explicit authorization.
8. **Respect data boundaries.** Use only information I am authorized to access; keep confidential materials in approved corporate environments; do not reproduce sensitive customer/patient/employee data or secrets.
9. **Use external industry guidance intelligently, if available.** Compare relevant established engineering principles and current practices, with citations, but do not substitute vendor marketing or external best practices for verified BD requirements.
10. **Be critical.** Identify overengineering, unsound assumptions, hidden operational costs, impractical abstractions, and weaknesses in your own proposed design. End with the strongest objections and how to validate them.

## 9. Required final output — complete this assignment without another prompt

Produce a cohesive, structured report with the following sections **in this order**:

1. **Executive recommendation** — proposed direction, confidence, and what it is based on.
2. **Research coverage and limitations** — exactly which systems were accessible/searched, coverage, missing sources, and evidence-quality caveats.
3. **Historical project inventory** — my verified prior ingestion work, lessons, sources, and reusable assets.
4. **Current-state and root-cause assessment** — what exists, what works, what is inconsistent, and what is genuinely missing.
5. **Requirements and non-goals** — sourced requirements, explicit unknowns, and risks of scope creep.
6. **Standard ingestion lifecycle** — source discovery, connectivity, separate data-validity POC, performance/latency testing, architecture decisions, scalable productionization, release, and operations with gates and artifacts.
7. **Architecture alternatives and decision matrix** — credible options, trade-offs, recommended direction, and reasons.
8. **Proposed technical framework** — architecture diagram, component boundaries, security model, reuse model, interfaces, configuration example, repository structure, testing and operational design.
9. **Worked source-onboarding example plus edge/failure test matrix**.
10. **MVP, phased roadmap, engineering backlog, and measurable success criteria**.
11. **Leadership-ready proposal** — a concise executive summary suitable to discuss with management and senior technical stakeholders.
12. **Evidence and decision register** — links, confidence labels, key architectural decisions, open questions, approval dependencies, and validation actions.

In every substantial recommendation distinguish:
**Observed internally** | **Established requirement** | **Inferred** | **Recommended** | **Unverified / needs decision**.

If output limits prevent all detail in one response, **prioritize a substantive complete report covering all 12 sections rather than stopping after research**, and put clearly labeled implementation-depth appendices last. If your environment supports creating an authorized persistent draft document, you may suggest an artifact structure, but **do not create or share documents or take external actions without authorization**. Never claim to have completed work that you have not done.

**Start now. Research the accessible internal evidence, draw conclusions carefully, challenge your own design, and deliver the complete recommended framework and engineering plan in this response.**
