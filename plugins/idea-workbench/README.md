# Idea Workbench

Idea Workbench turns a rough vision into an approved idea brief, a chosen
solution direction, a reviewed design, and an implementation-ready plan. It can
start at the beginning or continue from an artifact you already have.

It adapts to:

- **Greenfield work:** A new product, service, workflow, or project with no
  implementation baseline.
- **Existing systems:** A feature, change, or repair that must fit established
  behavior, code, interfaces, and conventions.
- **Hybrid work:** Something new that connects to an existing product or
  system.

The absence of an accessible repository does not automatically mean a project
is greenfield. The skills classify the context from available evidence and keep
uncertainty visible.

## Workflow

```text
rough vision
    -> shape-idea -> approved idea brief
    -> explore-options -> chosen direction
    -> write-design-doc -> reviewable design
    -> review-design-doc -> approved design
    -> plan-implementation -> approved delivery plan
```

Each stage produces one artifact and stops at an explicit approval gate. A
later stage never silently invents a product or architecture decision that
belongs in an earlier one.

## Choose a skill

| Skill | Use it when | Produces |
| --- | --- | --- |
| `develop-idea` | You are unsure where to begin or what comes next | One recommended next stage |
| `shape-idea` | The problem, outcome, scope, or boundaries are still fuzzy | An approved idea brief |
| `explore-options` | The brief is approved but the solution direction is not chosen | A compared and chosen direction |
| `write-design-doc` | A direction is chosen and needs concrete behavior and boundaries | A design ready for independent review |
| `review-design-doc` | A design needs a fresh-reader and risk-focused critique | A readiness verdict and approval record |
| `plan-implementation` | The reviewed design is explicitly approved | A traceable plan of verifiable delivery slices |

`develop-idea` is only a router. It recommends one skill and then stops so that
you stay in control of the workflow.

## Start using it

Install the `gordon1210/agent-goodies` marketplace first:

```bash
# Codex/ChatGPT
codex plugin marketplace add gordon1210/agent-goodies

# Claude Code
claude plugin marketplace add gordon1210/agent-goodies
claude plugin install idea-workbench@agent-goodies
```

Ask your agent to use the skill by name. For example:

### Start a new project

```text
Use shape-idea to help me turn this product vision into a grounded brief:
[describe the vision]
```

The workflow will treat platform, architecture, and project structure as
decisions to make—not as existing facts. Necessary setup normally belongs in
the first useful end-to-end implementation slice; a separate foundation slice
must provide independently verifiable value.

### Add a feature to an existing project

```text
Use develop-idea to inspect this project and tell me the next stage for this
feature idea: [describe the feature]
```

The workflow will inspect available current behavior, repository conventions,
integration points, compatibility requirements, and behavior that must be
preserved, then use them as design evidence and constraints.

### Continue from an existing artifact

```text
Use review-design-doc to review this design for implementation readiness:
[link to or identify the design]
```

You can begin with any skill when its required input and approvals already
exist. The workflow judges the substance and approval status of an artifact,
not its filename or template.

## How the collaboration works

- The agent inspects available conversation, documents, and project context
  before asking questions.
- It asks one consequential question at a time and recommends a choice when a
  tradeoff belongs to you.
- Facts, assumptions, hypotheses, decisions, and open questions stay separate.
- A focused research or disposable-prototype detour may be recommended when one
  uncertainty would otherwise make the next artifact speculative.
- Every stage waits for explicit approval before the workflow advances.
- `plan-implementation` creates the plan; it does not implement it or publish
  tickets.

For the full path, start with `develop-idea` or `shape-idea`. For focused work,
invoke the stage that matches the artifact you already have.

## License

MIT. See [LICENSE](LICENSE).
