# Deep Code Review

A portable Agent Skill for high-signal review of code changes and explicitly requested current-state audits. It is designed around progressive disclosure: the small `SKILL.md` routes the agent to focused reference files instead of loading a giant universal checklist.

## What it optimizes for

- Real correctness, security, data-integrity, compatibility, reliability, and performance defects
- Repository-aware reasoning beyond changed lines
- Aggressive false-positive removal through explicit disproof
- Rare, defensible `CRITICAL` ratings
- Read-only operation and no required runtime dependencies
- Portability across clients implementing the Agent Skills format

## Structure

```text
deep-code-review/
├── SKILL.md
├── README.md
├── LICENSE
├── references/
│   ├── core-method.md
│   ├── severity-evidence.md
│   ├── output-format.md
│   ├── correctness.md
│   ├── security-*.md
│   ├── data-state-concurrency.md
│   ├── contracts-compatibility.md
│   ├── reliability-performance.md
│   ├── frontend-browser.md
│   ├── tests-validation.md
│   ├── design-maintainability.md
│   └── language-*.md
└── evals/
    ├── README.md
    └── cases.md
```

## Install from the extracted directory

Interactive, project-local installation:

```bash
npx skills add ./deep-code-review
```

Global installation for a selected agent:

```bash
npx skills add ./deep-code-review --global --agent codex
npx skills add ./deep-code-review --global --agent claude-code
npx skills add ./deep-code-review --global --agent grok
```

Use `pnpm dlx skills` instead of `npx skills` when preferred. The CLI can also install the directory into multiple supported agents interactively.

A manual copy into the client's supported skills directory also works because the package has no executable dependency.

## Suggested prompts

```text
Use deep-code-review to review the changes between <base> and <head>.
Report only evidence-backed defects introduced by the change. Do not modify files.
```

```text
Review the current working-tree changes with deep-code-review.
Prioritize security, data integrity, rollout compatibility, and regressions.
```

```text
Review this PR with deep-code-review. Treat CRITICAL as exceptional and prove every blocking finding from the repository.
```

```text
Use deep-code-review for a full audit of <scope>. Report reachable current defects even when they predate the latest change. Do not modify files.
```

## Project-specific guidance

Keep product invariants, architecture constraints, generated-code rules, and safe validation commands in the repository's normal agent instructions. This skill deliberately avoids assuming a framework, deployment model, or severity policy that the repository has not established.

## Validation

The package contains evaluation cases under `evals/`. They test both recall and restraint. A useful review skill must catch dangerous defects and decline attractive but unsupported findings.

For format validation, use the Agent Skills reference validator when available:

```bash
skills-ref validate ./deep-code-review
```

## Safety properties

The skill contains only Markdown and the MIT license. It does not execute code, access the network, install packages, or request credentials. Review the files before installation as you would any third-party agent instruction package.
