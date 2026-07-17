---
name: plan-implementation
description: Turn an explicitly approved, implementation-ready design doc or equivalent specification into an actionable plan of vertical, independently verifiable slices with requirement traceability and explicit dependencies. Use when design decisions are settled and the user wants implementation tasks, tickets, sequencing, or a build plan; do not use to invent unresolved product or architecture decisions.
---

# Plan Implementation

Produce the plan, not the implementation. Use
[`assets/implementation-plan-template.md`](assets/implementation-plan-template.md)
as the output structure. Read
[`references/planning-quality.md`](references/planning-quality.md) before
decomposing non-trivial work and use it for the final quality pass.

## Pass the readiness gate

1. Locate the approved design, its requirements and acceptance criteria, the
   relevant repository instructions, and any existing project structure.
2. Confirm explicit approval of the design. Do not infer approval from the
   presence or polish of a document.
3. Identify unresolved questions that could change scope, user-visible behavior,
   architecture, interfaces, data, security, rollout, or acceptance criteria.
4. Stop without drafting the plan if approval is missing or any such question
   remains. Report the smallest decision needed and return the work to design or
   design review. Do not bury a design decision inside an implementation task.

Allow only local implementation choices that preserve the approved behavior and
contracts. State consequential assumptions instead of silently converting them
into facts.

## Ground the plan

Confirm the project context before naming files, components, commands, or test
targets. Do not infer `Greenfield` merely because a repository is unavailable.

- **Existing system:** Inspect the project and use exact paths and commands only
  when the available project proves them.
- **Greenfield:** Distinguish observed facts from planned structure. Name a
  planned path or initialization command only when the approved design or an
  authoritative scaffold establishes it, and label that basis. Otherwise name
  the responsibility to create and the evidence that will confirm its location.
- **Hybrid:** Apply the corresponding rule to each side and identify work at the
  seam explicitly.

When an existing location is unknown or inaccessible, name the responsibility
or area to locate and include that discovery in the relevant slice.
Describe the intended verification when an exact command is not grounded;
never fabricate command syntax.

Assign stable local identifiers to unnumbered requirements, acceptance criteria,
and design decisions. Preserve existing identifiers when present.

## Decompose vertically

1. Start with the thinnest end-to-end slice that produces observable behavior or
   decisive implementation evidence.
2. Add slices that extend complete behavior, including relevant failure paths,
   migration, observability, security, compatibility, and rollout work.
3. Keep each slice coherent enough for one focused implementation session and
   independently verifiable at a meaningful boundary.
4. Embed supporting layer work in the first slice that consumes it. In
   greenfield work, include the necessary bootstrap in the first end-to-end
   slice. Create a separate foundation slice only when it delivers independently
   useful, verifiable value.
5. Give every slice an outcome, traceability links, scope, expected changes,
   implementation work, dependencies, and verification evidence.

Avoid plans organized only by technical layers such as database, backend,
frontend, and tests. Prefer slices that demonstrate a usable capability across
the necessary layers.

## Order and trace

Map every in-scope requirement, acceptance criterion, and consequential design
decision to at least one slice and one verification method. Map every slice back
to an approved outcome, requirement, or risk reduction.

Express dependencies by slice identifier and distinguish actual blockers from a
preferred order. Minimize the serial chain, call out safe parallel work only
when shared contracts are stable, and include rollout or recovery ordering when
state can change irreversibly.

## Write and review

Complete the template and remove all unused guidance. Run the quality checks in
`references/planning-quality.md`, then confirm:

- no in-scope requirement is orphaned;
- no slice exists without a justified outcome;
- each slice has observable completion evidence;
- all paths and commands are grounded in inspected or explicitly approved
  context;
- dependencies form a workable order; and
- no blocking decision or placeholder remains.

Present the plan, summarize any non-blocking assumptions, and ask for explicit
approval. Stop there. Do not implement, publish tickets, or begin another stage
until the user approves the plan.
