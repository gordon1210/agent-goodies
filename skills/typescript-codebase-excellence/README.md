# TypeScript Codebase Excellence Skill

A production-oriented Agent Skill for designing, implementing, reviewing, refactoring, testing, securing, optimizing, packaging, and operating small-to-medium TypeScript codebases.

The skill is intentionally non-dogmatic. It preserves repository contracts and favors the smallest sound change over speculative architecture, type-system theater, blanket lint policies, or automatic toolchain migration. It treats TypeScript as a compile-time aid around JavaScript runtime behavior: external values still require validation, emitted artifacts still require testing, and package/runtime compatibility remains an explicit contract.

## Contents

```text
typescript-codebase-excellence/
├── SKILL.md
├── README.md
├── EVALUATION.md
├── LICENSE
└── references/
    ├── architecture-packages-api.md
    ├── async-concurrency-lifecycle.md
    ├── build-generated-code-frameworks.md
    ├── documentation-observability-operations.md
    ├── frontend-browser-ui.md
    ├── performance-resource-use.md
    ├── persistence-wire-contracts.md
    ├── review-playbooks.md
    ├── runtime-modules-platforms.md
    ├── security-dependencies-supply-chain.md
    ├── sources.md
    ├── testing-verification.md
    ├── tooling-baseline.md
    ├── types-modeling-errors.md
    └── typescript-6-7-compatibility.md
```

`SKILL.md` contains the operating workflow and core rules. It routes the agent to focused references only when the task requires them, keeping normal context use bounded while retaining broad coverage for reviews and repository audits.

## Installation

Place the `typescript-codebase-excellence` directory in the Agent Skills directory used by the host application. The directory name must remain identical to the `name` field in `SKILL.md`.

Host paths and loading behavior differ. Follow the host's current Agent Skills documentation rather than assuming a universal location.

## Intended use

Use the skill for:

- Focused TypeScript implementation, debugging, and refactoring.
- Patch and pull-request review.
- Repository-wide quality, security, or production-readiness audits.
- Applications, services, CLIs, libraries, browser UIs, SSR systems, workers, serverless functions, Electron applications, and mixed JavaScript/TypeScript projects.
- Workspaces, package boundaries, public declarations, package exports, and SemVer review.
- ESM/CommonJS, runtime, bundler, browser, and platform compatibility.
- Async behavior, cancellation, streams, background work, shutdown, and backpressure.
- Runtime input validation, authorization, browser/server security, and dependency supply-chain review.
- Unit, integration, type, browser, E2E, package-consumer, and CI design.
- Performance work across runtime, event loop, memory, bundle size, build time, and type-checker cost.
- TypeScript 6 maintenance and deliberate TypeScript 7 migration or coexistence.

It is optimized for small-to-medium repositories but scales to a bounded package, application, or subsystem inside a larger monorepo.

## TypeScript 6 and 7 posture

The skill supports both compiler generations without treating either as a universal default.

- Preserve the compiler generation pinned by the repository unless migration is part of the task.
- Separate command-line compiler adoption from tools that import the TypeScript compiler or language-service API.
- Treat TypeScript 6 as a valid maintained baseline, not technical debt merely because TypeScript 7 exists.
- For a TypeScript 7 migration, first remove TypeScript 6 deprecation debt and make module, target, root, ambient-type, and strictness decisions explicit.
- Compare diagnostics, declaration output, package artifacts, runtime tests, lint/parser compatibility, editor behavior, and compiler-API integrations—not only `tsc` exit status.
- Tune TypeScript 7 parallelism only against measured build time and memory limits.

The detailed migration gates are in `references/typescript-6-7-compatibility.md`.

## Design constraints

The skill deliberately avoids common failure modes:

- No assumption that a compile-time type validates runtime input.
- No casual `any`, type assertion, double assertion, non-null assertion, `@ts-ignore`, or broad `skipLibCheck` workaround.
- No automatic TypeScript, runtime, package-manager, framework, bundler, linter, test-runner, or module-system upgrade.
- No blanket interface, generic, class, dependency-injection, repository-layer, schema-library, or monorepo-tool introduction.
- No claim that installing or testing an unknown package is safe; package lifecycle scripts and toolchains can execute code.
- No assumption that `paths` aliases, bundler resolution, source execution, or editor success match runtime/package behavior.
- No optimization without a defined contract and representative evidence.
- No review finding without a concrete trigger, evidence, and impact.
- No invented defects when a focused patch is correct.

## Validation

From the repository root, validate the package with the Agent Skills reference validator when available:

```bash
skills-ref validate ./skills/typescript-codebase-excellence
```

Also run the behavioral scenarios in `EVALUATION.md` when materially changing the skill. A repository-specific validator may additionally enforce metadata, link, naming, or packaging rules.

## Versioning

The skill uses semantic versioning in `SKILL.md` metadata:

- Patch: source refresh, wording correction, or clarification that does not materially change expected decisions.
- Minor: additional guidance, supported context, or reference that expands behavior compatibly.
- Major: changed rule hierarchy, required workflow, migration posture, or decision policy that can materially alter generated code or review outcomes.

## License

MIT. See `LICENSE`.
