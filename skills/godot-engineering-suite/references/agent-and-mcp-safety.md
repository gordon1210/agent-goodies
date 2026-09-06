# Agent and MCP safety

Use before agent-driven project execution, scene mutation, editor launch, plugin installation or MCP use.

## Default posture

This suite requires no MCP server and grants no tools. Use normal repository tools and the matching Godot CLI under the agent host's existing permission policy.

Do not add hooks, permission allowlists, MCP configuration, editor plugins or background processes merely to complete ordinary Godot work.

## Execution boundary

Running Godot may execute:

- project startup scripts and autoloads;
- `@tool` scripts and EditorPlugins when the editor/import path loads them;
- post-import scripts;
- GDExtension/native libraries;
- platform SDK initialization.

Review these before launching an unfamiliar repository. Prefer an isolated worktree/container/VM with minimal credentials and network access for untrusted projects.

## MCP rules

When a repository already uses a Godot MCP server:

- pin and review its implementation and dependencies;
- constrain accessible project roots;
- separate read/run/debug tools from scene/resource mutation tools;
- do not blanket-approve a wildcard such as `mcp__godot__*`;
- require confirmation for editor launch, global project search, resource resave, export and UID-wide mutation;
- ensure paths cannot escape the repository;
- do not let setup scripts overwrite existing MCP configuration;
- avoid MCP when direct CLI/file operations are clearer and more auditable.

An MCP tool is not a sandbox. It runs with the server process's operating-system privileges.

## Agent mutation rules

- Work on a branch or isolated worktree.
- Start from a clean or understood working tree.
- Keep scene/resource edits small and inspect the diff.
- Never auto-install addons or export SDKs.
- Never launch long-lived watch loops or background editors without an explicit user request.
- Do not claim continuous monitoring after the turn ends.

## Secrets

Run agents without unrelated cloud credentials, signing keys, SSH agents or customer data when project code is untrusted. Never place secrets in prompts, project resources, logs or MCP environment templates.
