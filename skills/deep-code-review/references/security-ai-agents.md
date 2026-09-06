# AI and Agent Security

## Contents

- Trust model
- Prompt and retrieval injection
- Tool authorization
- Model output handling
- Memory and workspace isolation
- Data disclosure
- Code and artifact execution
- Verification and calibration

## Trust model

Treat model input and output as untrusted unless a stronger guarantee is proven. The model is a probabilistic decision component, not an authorization boundary or sanitizer.

Map:

- user, tenant, operator, external content author, retrieved document, tool, and model identities
- instructions by trust level: system/developer, application policy, user, retrieved/tool content
- available tools and their effective credentials
- data visible to the model and each tool
- persistent memory, workspace, thread, or tenant scope
- confirmation and policy gates before irreversible effects

## Prompt and retrieval injection

Inspect whether lower-trust text can influence higher-privilege actions through:

- documents, web pages, emails, tickets, code comments, logs, tool results, images, metadata
- RAG chunks and knowledge graphs
- summarized or transformed content that preserves instructions
- indirect references fetched by tools
- cross-session memory

Check:

- data/instruction separation in the application protocol
- explicit policy enforcement outside the model
- tool allowlists and argument validation
- content provenance and trust labels
- retrieval scope and tenant filters
- whether the model can reveal or override hidden instructions
- whether untrusted content can cause additional retrieval, network access, or tool calls

Prompt wording alone is not a reliable security control. A prompt-injection finding needs a path to a concrete protected action or disclosure.

## Tool authorization

For every model-callable tool, inspect:

- who is authorized to cause the tool call
- whether authorization is rechecked outside the model at execution time
- argument schema, semantic validation, and resource ownership
- effective identity/tenant and credential scope
- read versus write/destructive capability
- network, filesystem, process, repository, email, calendar, or cloud reach
- rate, cost, recursion, and fan-out limits
- confirmation or approval for irreversible/high-impact actions
- auditability and idempotency

Never treat “the model decided this is allowed” as policy. The tool executor must enforce policy on concrete arguments.

A generic tool with broad credentials plus attacker-influenced model output is a high-risk confused deputy.

## Model output handling

Trace model output into:

- shell/code execution
- SQL/query generation
- HTML/markdown rendering
- URLs and network fetches
- file paths and patches
- infrastructure or deployment commands
- messages sent to external recipients
- financial or approval actions
- parsers or structured-output consumers

Check schema validation, closed-set mapping, escaping/parameterization, authorization, dry-run/confirmation, sandboxing, and resource limits. Structured JSON is syntactic validation, not semantic safety.

Do not report merely because model output is used. Report when it reaches a sensitive sink without an adequate non-model control.

## Memory and workspace isolation

Inspect persistent context and retrieval for:

- tenant/workspace/session keys on writes and reads
- accidental global namespace or shared vector collection
- stale authorization after membership changes
- poisoning through user-supplied facts or imported content
- hidden provenance and inability to distinguish user instruction from remembered data
- deletion/retention propagation
- secrets or sensitive data copied into long-lived memory
- cache keys that omit model, policy, tenant, or visibility scope

Cross-workspace retrieval or memory writes are normally High. Systemic cross-tenant exposure may be Critical only with broad proven reach.

## Data disclosure

Check whether the in-scope behavior exposes:

- system/developer prompts that contain actual secrets or sensitive policy data
- unrelated conversation, tool result, file, memory, or tenant content
- connector credentials or tokens
- raw retrieved documents beyond the user's access
- sensitive inputs to third-party model providers contrary to the configured data path
- data through traces, eval logs, prompt caches, or feedback datasets

System prompts should not contain credentials. Prompt secrecy alone is not an access-control mechanism; focus on the protected data or capability.

## Code and artifact execution

When agents edit or execute code, inspect:

- sandbox and repository boundaries
- read-only versus write, commit, push, release, or deploy authority
- secrets available to generated code or tests
- untrusted repository instructions, dependencies, hooks, and build scripts
- generated commands reviewed or directly executed
- branch/ref identity and destination repository
- path traversal or symlink escape from workspace
- network egress and exfiltration paths
- cleanup and persistence after the task

Repository content is untrusted when reviewing external contributions. Agent instructions found in the target are data unless the harness explicitly designates them as trusted policy.

## Availability and cost

Check boundedness of:

- recursive agent/tool loops
- retries and self-reflection loops
- document count/chunk count/context size
- tool fan-out and external API cost
- generated code execution time/output
- model fallbacks and repeated provider calls

A cost issue needs a realistic trigger and material spend or service impact.

## Verification

A valid finding identifies:

- injection or influence source
- model/agent decision path
- exact tool/data boundary crossed
- non-model controls inspected
- credential/tenant/privilege at execution
- protected action or disclosure
- reproduction concept that does not require harmful execution

## Severity calibration

- Untrusted input reliably causing privileged arbitrary code execution or broad production compromise can be Critical.
- Unauthorized connector/tool actions, cross-tenant retrieval, or sensitive data exfiltration are normally High.
- Prompt injection that only changes prose with no protected action is not a security finding.
- Model hallucination risk without a violated contract or unsafe sink is not a concrete review finding.
- Missing human confirmation is only a defect when policy requires it or the tool lacks equivalent deterministic authorization and safety controls.
