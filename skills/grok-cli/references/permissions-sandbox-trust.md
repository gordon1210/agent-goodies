# Permissions, sandbox, and trust

Treat a Grok invocation as remote model access plus local agent execution. A
prompt is not a security boundary. Control authority with independent layers,
then verify what happened.

This reference describes Grok Build 1.0.13. Inspect the installed permissions,
sandbox, hook, MCP, plugin, and configuration guides before depending on exact
behavior.

## Use layered controls

Apply all relevant layers:

1. **User authority:** what outcome and side effects the user actually asked
   for.
2. **Task scope:** exact working directory, owned files, allowed commands,
   external systems, and stop conditions.
3. **Tool selection:** omit capabilities the task does not need.
4. **Permission policy:** deny, ask, or allow each reachable operation.
5. **Hooks and managed requirements:** supplemental policy and auditing.
6. **OS sandbox:** kernel-level filesystem and child-process limits.
7. **Isolation and recovery:** dedicated worktree or disposable environment
   whose provenance is already established.
8. **Host verification:** inspect the diff, processes, external effects, and
   validation evidence.

No one layer substitutes for the others. A worktree does not prevent data
exfiltration or destructive commands. A sandbox does not decide whether an
external API mutation was authorized. A natural-language rule such as “never
delete files” is useful context but not enforcement.

## Filter tools before granting permissions

Headless mode accepts:

- `--tools`: built-in tool allowlist.
- `--disallowed-tools`: remove built-in tools from the selected profile.
- `--no-subagents`: block Grok's child-agent spawning.
- `--disable-web-search`: remove built-in web search and fetch behavior.

Use the supported stable CLI's operator-facing entries. Tested examples include
`read_file`, `search_replace`, `grep`, `list_dir`, and
`run_terminal_command`. Under a narrow `--tools` list, enable subagents with
the special `Agent` or `Agent(type,...)` entry; `spawn_subagent` is the
model-facing tool name, not the operator directive. Do not infer an entry from
permission classes such as `Bash` or `Read`. See the
[current stable notes](versions/1.0.13.md) for the exact contract.

The version note also gives a structured-output preflight for runtime
confirmation. It starts a real remote session, so use it only within the
caller's model-usage authority.

`--tools` is not a complete capability allowlist: MCP meta-tools can remain
available, and configured extensions or lifecycle hooks still matter. Inspect
effective MCP servers, plugins, hooks, agents, skills, rules, and config sources
with `grok inspect --json`.

When the host owns delegation, pass `--no-subagents` unless nested fan-out was
chosen deliberately. Authorized fan-out with a narrow `--tools` list also needs
`Agent` or `Agent(type,...)` and effective settings that leave subagents
enabled. Inspect the selected child-agent definition because its capabilities
must fit the same authority envelope. Otherwise one assignment can create
child sessions, multiply model usage, share inherited MCP access, and
complicate ownership.

### ACP bridge limitations

The tested `grok agent` launch surface is not identical to headless `grok -p`:
it does not expose per-launch `--tools`, `--disallowed-tools`,
`--no-subagents`, or `--permission-mode` flags. The bundled ACP bridge cannot
enforce a tool allowlist by omitting those unsupported arguments. Its
permission loop only mediates requests that Grok actually sends to the client;
it is not a sandbox and cannot intercept already allowed tool calls.

The bridge can pass one reviewed `--agent-profile` and can set
`GROK_SANDBOX` through its `--sandbox` option. Both select existing Grok
behavior; neither proves that the desired tool or operating-system boundary was
enforced. Inspect `grok inspect --json`, the profile, startup diagnostics, and
representative denied operations. If the task requires a strict per-call
read-only tool set with subagents disabled, use the constrained `grok -p`
baseline instead of ACP unless an audited Grok configuration already provides
equivalent controls.

## Permission modes

| Mode | Operational meaning | Appropriate use |
|---|---|---|
| `default` | Read-only built-ins run; other calls normally ask | Human-supervised TUI |
| `acceptEdits` | File edits are accepted without the normal prompt | Local interactive editing with later diff review |
| `auto` | A safety classifier may allow work and block or escalate the rest | Interactive convenience, not a closed policy |
| `dontAsk` | Pre-approved and built-in read-only operations run; unmatched asks are denied | Strict headless allowlists and CI |
| `bypassPermissions` | Always-approve behavior | Only separately constrained trusted automation |
| `plan` | Compatibility mode related to planning | Planning UX, not enforcement |

`--always-approve` is the product spelling for bypass behavior; `--yolo` can
exist as an alias. Prefer the descriptive spelling if the current help
advertises it.

### Rule semantics

CLI permission rules use forms such as:

```text
Bash(git status*)
Edit(src/component/**)
Write(src/component/**)
Read(docs/**)
Grep(src/**)
WebFetch(domain:docs.example.com)
MCPTool(server__tool)
```

Important properties:

- Deny wins over ask, which wins over allow.
- A bare class such as `MCPTool` matches that whole class.
- `*` and `**` have class-specific matching rules; review the current guide.
- Shell commands are split into segments for matching where possible.
- Every segment of a chain must satisfy an allow rule before the chain is
  approved by those rules.
- Complex shell constructs can be evaluated as one unit.
- Allow rules are not a closed allowlist. An unmatched call falls through to
  the active permission mode.

For deny-by-default automation, combine `dontAsk` with narrow allow rules.
Do not pair broad `auto` behavior with a few allow rules and call the result an
allowlist.

Under `dontAsk`, a denied shell request can terminate the prompt as
`permission_cancelled`. Ensure every required compound-command segment matches
an exact allow rule. Treat cancellation as incomplete even after partial
output, and never widen permissions automatically to retry it.

Recognized read-only tools and shell commands can run automatically even under
`dontAsk`. That classifier is a convenience, not a security boundary. Repository
configuration can affect how an apparently read-only Git or build command
behaves, and build commands can execute project code.

### Always-approve

Always-approve skips ordinary interactive prompts, but deny rules, hooks,
administrative restrictions, and selected shell ask rules can still apply. It
does not grant OS privileges and does not make the environment disposable.

Use it only when all of these are true:

- The user intended autonomous execution.
- The working environment and its provenance are known.
- Filesystem and network reach are independently constrained.
- Plugins, hooks, MCP servers, agent profiles, and inherited environment have
  been inspected.
- Destructive and remote actions remain outside the authority envelope.
- The host can review and recover the resulting state.

Prefer `dontAsk` plus exact allows for bounded code delegation. If the task
cannot be expressed that way, explain the broader grant before using
always-approve.

## Sandbox profiles

Sandbox mode is off by default. The tested built-in profiles are:

| Profile | Read access | Write access | Child network |
|---|---|---|---|
| `off` | Unrestricted | Unrestricted | Unrestricted |
| `workspace` | Broad filesystem | Working directory, Grok state, temp | Allowed |
| `devbox` | Broad filesystem | Most top-level paths except protected areas | Allowed |
| `read-only` | Broad filesystem | Grok state and temp, not the project | Blocked on Linux only |
| `strict` | Working directory and system paths | Working directory, Grok state, temp | Blocked on Linux only |

Consequences:

- `read-only` protects project integrity but not confidentiality of all files
  readable by the user.
- `strict` narrows reads but still permits writes inside the working directory.
- `workspace` limits write locations but allows broad reads and network.
- `devbox` is intended for an already disposable development VM. Its name does
  not establish disposability or authorize deletion.
- On macOS, the built-in child-network restriction is a no-op.
- Built-in web tools, the model connection, and other in-process HTTP behavior
  are not stopped by child-process network restrictions.
- A built-in profile can either warn and continue without full enforcement or
  fail closed when a mandatory protection cannot be established. Treat startup
  diagnostics and the process result as authoritative; never infer enforcement
  from the selected profile name.

The sandbox is OS-level confinement of the Grok process, not a container or
virtual machine. A non-off profile also keeps tool execution in-process instead
of delegating it through a shared leader.

### Fail-closed startup and runtime sockets

Grok Build 1.0.13 adds mandatory deny protections for known Docker, Podman,
and containerd socket locations under every non-`off` sandbox. A container
runtime socket can bypass filesystem confinement, so refusal is preferable to
starting with that socket exposed. Some built-in-profile failures only warn in
documented platform cases, but a mandatory protection failure can exit before
the model turn. The exact stderr and process exit status decide which occurred.

On macOS arm64 with Docker Desktop's documented
`/var/run/docker.sock -> ~/.docker/run/docker.sock` endpoint symlink, Grok Build
1.0.13 emits `runtime-socket deny resolution failed` with `endpoint is a
symlink`, then exits with status 1. The endpoint symlink, not the ordinary
`/var -> /private/var` parent alias, is the object named by the failure. This is
fail-closed behavior, but it prevents the advertised `read-only` review profile
from starting in that common environment.

There is no documented Grok Build 1.0.13 per-call exception that disables only
this protection while safely denying both the link and its resolved socket.
Do not present a custom profile extending `read-only` as a workaround unless
representative tests prove the mandatory socket deny remains enforced. Do not
switch to `workspace`, `strict`, `devbox`, a permissive custom profile, or
`always-approve` merely to make the call start: none establishes the requested
boundary, and `devbox` is intended only for an already disposable development
VM. Never alter a runtime socket or symlink, or stop, restart, or reconfigure
Docker Desktop, as an incidental Grok workaround.

Use one of two resolution paths:

1. **Preferred product resolution:** update Grok only with explicit user
   authorization, re-run the minimal sandbox reproduction, and verify from
   startup diagnostics plus representative denied operations that the profile
   applies. Remove the version-specific fallback only after host-side
   confirmation.
2. **Optional machine-level choice:** a user may choose to disable Docker
   Desktop's **Allow the default Docker socket to be used** setting. This is
   not an agent action and must never be recommended or performed as an
   incidental Grok fix. It can break third-party clients fixed to
   `/var/run/docker.sock`, even though the Docker CLI can use the
   `desktop-linux` context and per-user socket.

### Custom profiles

Custom profiles can extend a built-in profile and add literal read-only or
read-write paths, network restriction, and kernel-enforced deny paths or globs.
Creating or changing one mutates security configuration and requires explicit
user intent. Do not generate a permissive profile merely to make a task pass.

Current platform caveats include:

- macOS evaluates deny globs at runtime through Seatbelt.
- Linux expands deny globs against files that exist at launch; later-created
  matches may not be covered. Use exact paths for critical Linux denials.
- A custom profile with an invalid or unenforceable deny configuration is
  designed to fail closed, unlike some built-in-profile startup failures.
- A resumed session retains its original sandbox profile and refuses a
  different one. Start a fresh session to change the boundary.

Validate custom profiles with representative allowed and denied operations
before entrusting them with sensitive work.

## Secrets and environment inheritance

The default shell environment policy in the tested version leaves the child
environment intact. A Grok shell command can therefore inherit tokens, keys,
cloud context, SSH agent access, and other ambient authority.

For a consultation, omit the shell tool. For a client integration, spawn Grok
with a deliberately filtered environment. Persistent configuration supports a
shell environment policy, but do not edit it unless requested. Pay attention to
login-shell startup files and persistent shells, which can reintroduce values.

Never put credentials in:

- Prompts or task packets.
- CLI arguments or checked-in prompt files.
- Debug logs, traces, captured ACP fixtures, or session exports.
- Plugin or marketplace configuration.
- WebSocket secrets committed to a repository.

Grok sessions, memory, logs, crash reports, and trace exports can retain prompt
or tool data. Apply the user's retention policy and do not clear or delete
pre-existing data without explicit authority.

## Project instructions and trust

Grok discovers instructions and extensions from the project root down to the
working directory, including Grok-native locations and selected compatibility
formats. This is valuable context and also a trust boundary.

Before trusting an unfamiliar repository:

- Inspect `grok inspect --json` and its config warnings.
- Read the discovered project instructions.
- Review project permission rules and sandbox configuration.
- Review session-start and tool hooks.
- Review project plugins, agent profiles, MCP definitions, skills, and shell
  startup behavior.
- Inspect build scripts before allowing builds or tests to execute code.

Do not use `--system-prompt-override` to suppress inconvenient repository rules.
Append task-specific `--rules` only when they do not conflict with higher-level
instructions.

## Hooks

Hooks can observe lifecycle events, rewrite tool input, deny a pre-tool call,
or keep an agent working at stop. They can also execute commands or HTTP calls.

Treat hooks as executable code. In the tested version, a hook timeout, crash,
or malformed result normally fails open; only an explicit valid deny blocks the
operation. Hooks are therefore useful for policy defense and audit, but are not
the sole safety boundary.

Global hooks can be active independent of the repository. Project hooks depend
on folder trust. Inspect provenance, command paths, HTTP destinations, and
timeouts before starting a session.

## MCP servers

MCP tools may read or mutate local, remote, or shared state. Tool names and
descriptions do not prove that a call is read-only. Before allowing MCP:

1. Identify the exact configured server, transport, executable or URL, and
   authentication source.
2. Inspect the tool schema and intended target account, project, repository, or
   database.
3. Grant only named tools needed for the task.
4. Keep remote writes and destructive calls within explicit user authority.
5. Remember that Grok subagents can inherit parent MCP servers.

Adding, removing, enabling, or disabling an MCP server mutates configuration.
Do not do it as an incidental workaround.

## Plugins, skills, and agent profiles

- A skill adds instructions and can steer behavior.
- An agent or persona can change tool and model behavior.
- A plugin can bundle skills, agents, hooks, MCP servers, and other executable
  integrations.
- `grok agent --plugin-dir` is the highest-priority process scope and is always
  trusted; hooks and MCP servers activate without a trust prompt.

Install, enable, trust, update, or load a plugin directory only when the user
intends that code to run. A local path is not inherently trustworthy. Validate
structure and inspect executable components before use.

## Memory, sessions, and independence

Cross-session memory and resumed conversations can leak assumptions across
tasks. For an independent second opinion, start a fresh session and disable
memory for the process when supported (`GROK_MEMORY=0` in the tested version).
For pairing, resume an exact session ID intentionally.

Do not use `grok memory clear`, `grok sessions delete`, worktree cleanup, or
similar commands to manufacture a clean environment. They destroy state and
need separate authority and validated targets.

## Plan mode is not confinement

Plan mode gates normal edit tools to a plan file, but it is not a complete
security boundary. In the tested version, shell writes are not inspected by
the plan edit gate, and subagent behavior is not fully covered by it. Combine
planning with tool filtering, permissions, and a sandbox.

## Destructive and external actions

Grok never receives more authority than the caller has. A broad outcome such
as “clean up,” “fix the tests,” or “make the deployment work” does not
implicitly authorize:

- Recursive deletion, Git clean/discard/reset, or removal of user work.
- Branch, stash, session, worktree, memory, credential, plugin, or marketplace
  deletion.
- Database reset or destructive migration.
- Cloud, Kubernetes, CI, issue-tracker, messaging, or other remote mutations.
- Commit, push, publish, deploy, release, telemetry upload, or feedback
  submission.

If a delegated task reaches one of these boundaries, Grok must stop and report
the exact proposed action and target. The host must independently validate it
and obtain any required approval.

## Preflight checklist

- Installed version and relevant help confirmed.
- `--cwd` and project root resolved.
- Existing work and file ownership inspected.
- Effective config, instructions, plugins, hooks, MCP, agents, and skills
  reviewed.
- Remote prompt contents minimized and scrubbed of secrets.
- Tools and subagents reduced to the task minimum.
- Permission mode and rules form a real deny-by-default boundary when needed.
- Sandbox semantics and platform enforcement checked.
- Shell environment and network reach understood.
- Timeout, turn limit, output parser, and failure handling selected.
- Host-side diff and validation planned.
