# Design Review: [Design title]

| Field | Value |
| --- | --- |
| Reviewed document | [Link, path, or version] |
| Review date | [Date] |
| Reviewer | [Name or role] |
| Assessed risk | Low / Medium / High — [reason] |
| Verdict | Ready / Ready with follow-ups / Not ready |
| Planning approval | Pending / Approved by [person] on [date] / Not requested |

## Verdict

**[Verdict]** — [Briefly explain why this verdict follows from the findings.]

**Conditions:** [None, or the bounded items that must be resolved before or during planning.]

**Approval requested:** [Approve this reviewed design for implementation planning / Accept the listed follow-ups / Not applicable because the design is not ready.]

## Fresh-reader summary

- **Problem and outcome:** [What the document says is changing and why]
- **Chosen direction:** [The proposed solution and rationale]
- **Boundaries:** [What is included, excluded, and externally owned]
- **Validation and delivery:** [How success and safe rollout will be established]
- **Unclear from the document:** [Material ambiguity that required inference]

## Findings

### Blockers

| ID | Location | Evidence and finding | Credible impact | Resolution needed |
| --- | --- | --- | --- | --- |
| B1 | [Section or absent] | [What the document states, omits, or contradicts] | [Failure or unsafe decision this enables] | [Decision, evidence, or clarification required] |

### Major findings

| ID | Location | Evidence and finding | Credible impact | Resolution needed |
| --- | --- | --- | --- | --- |
| M1 | [Section or absent] | [Material gap] | [Likely rework or operational consequence] | [Required resolution] |

### Minor findings

| ID | Location | Evidence and finding | Credible impact | Resolution needed |
| --- | --- | --- | --- | --- |
| m1 | [Section or absent] | [Bounded ambiguity or weakness] | [Limited consequence] | [Useful clarification] |

Remove empty severity sections and state “No findings at this severity” when the absence matters to the verdict.

## Coverage and traceability

| Concern | Design evidence | Validation evidence | Gap or residual risk |
| --- | --- | --- | --- |
| [Goal, flow, interface, data rule, failure mode, or delivery concern] | [Section] | [Test, signal, or acceptance scenario] | [Uncovered area] |

## Assumptions and open decisions

| Item | Stated or inferred? | Blocking? | Owner or next action |
| --- | --- | --- | --- |
| [Assumption or question] | [Status and evidence] | Yes / No | [Decision-maker or validation action] |

## Residual risks

- [Risk that remains even if every finding is addressed]

## Recommended next decision

[State the smallest decision or evidence-gathering step that would move the document forward.]
