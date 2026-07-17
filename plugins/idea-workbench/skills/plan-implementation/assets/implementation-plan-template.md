<!-- Copy this template, replace every bracketed prompt, and remove this comment and all unused optional sections. -->

# Implementation Plan: [Title]

- **Status:** Draft — awaiting approval
- **Source design:** [Approved design artifact]
- **Design approval:** [Who approved it and where]
- **Project context:** Greenfield / Existing system / Hybrid — [evidence]
- **Plan owner:** [Owner]

## Outcome and boundaries

**Outcome:** [Observable result this plan delivers]

**In scope:**

- [Approved capability or requirement]

**Out of scope:**

- [Explicit boundary]

**Constraints and assumptions:**

- [Grounded constraint or non-blocking assumption]

## Implementation strategy

[Summarize the delivery shape, the first end-to-end slice, and the reason for
the sequence. Do not reopen the approved design.]

## Traceability

| Requirement, criterion, or decision | Source | Slice(s) | Verification |
| --- | --- | --- | --- |
| [Stable ID and short label] | [Section or link] | [S1] | [Observable evidence] |

## Slice overview

| Slice | Vertical outcome | Depends on | Verification boundary |
| --- | --- | --- | --- |
| S1 | [Working behavior or decisive evidence] | None | [Test, demonstration, or inspection] |

## S1 — [Vertical outcome]

**Outcome:** [What becomes observably possible]

**Covers:** [Requirement, criterion, and decision IDs]

**Depends on:** None

**Scope:**

- [Included behavior]
- [Relevant failure or boundary behavior]

**Expected changes:**

- `[Confirmed existing path or approved planned path]` — [Basis,
  responsibility, and intended change]
- [Responsibility or area to create or locate] — [Evidence needed to establish
  its path]

**Implementation work:**

1. [Concrete, design-aligned action]
2. [Concrete, design-aligned action]

**Verification:**

- Automated: `[Grounded existing or planned command]` — [Basis and expected result]
- Behavioral: [Observable scenario and expected result]
- Operational, when applicable: [Telemetry, migration, rollback, or recovery evidence]

**Completion evidence:** [Artifact, passing check, demonstration, or recorded result]

**Risks and notes:** [Slice-specific risk or `None`]

<!-- Repeat the slice section for S2, S3, and later slices. -->

## Delivery and recovery

- **Release sequence:** [How completed slices become available]
- **Compatibility or migration:** [State transition and verification, if applicable]
- **Rollback or recovery:** [How to return to a safe state, if applicable]
- **Observability:** [Signals that confirm success or expose failure]

## Plan readiness

- **Coverage:** [Evidence that every in-scope item maps to work and verification]
- **Dependency check:** [Evidence that ordering and parallel work are sound]
- **Grounding check:** [Evidence that existing details were inspected and
  greenfield details follow approved decisions or authoritative scaffolding]
- **Blocking decisions:** None
- **Plan approval:** Pending
