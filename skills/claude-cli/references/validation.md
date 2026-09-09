# Validation

## Deterministic tests

From a checkout containing this skill:

```bash
python3 -m unittest discover -s skills/claude-cli/tests -v
```

Alternatively point `-s` at this installed skill's `tests/` directory. Tests
exercise actual local subprocesses, but their responses are fixtures: no Claude
account, model request, or SDK is used. POSIX-specific tests cover group cleanup,
file permissions, symlinks, FIFOs, and writer locking. The executable fixtures
are intended for Linux/macOS tests; the original bundle was tested on Linux only. The repository integration check
below adds macOS offline execution.

## Target-installation smoke test

The following is a **separate opt-in validation using real account usage**:

1. Run `doctor` in the approved target working directory; inspect the actual
   version, authentication setup, safe-mode support, and managed policy.
2. Submit a tool-free prompt asking Claude to retain an arbitrary non-secret
   marker such as `amber-pine-47` and acknowledge it in one sentence.
3. Capture its exact session UUID. In a new artifact directory, resume that ID
   and ask which marker was supplied. Do not put the marker in this follow-up.
4. Check the process status, terminal envelope, session identity, result, and
   retained diagnostics. This validates the CLI/session contract, not general
   model reasoning quality.

No native smoke-test success is claimed in this distribution. The behavioral
skill evaluation prompts in `evals/evals.json` are also supplied but not claimed
to have been executed by a model evaluator.

## Repository integration check — 2026-09-09

All 37 tests passed on macOS using Python's unittest discovery. The local runner
retained task-created temporary directories instead of recursively deleting them;
all test bodies and assertions executed. No installed provider CLI or account was
called. Python syntax, JSON, skill frontmatter/UI metadata, repository links, and
the Claude marketplace passed validation. The two independently packaged runtime
copies matched byte for byte. CI runs the two suites in separate Python processes.
Native CLI smoke tests and model-level evaluations remain unexecuted.
