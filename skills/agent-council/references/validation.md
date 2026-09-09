# Validation

## Offline automated tests

```bash
python3 -m unittest discover -s skills/agent-council/tests -v
```

Use the installed skill's actual path when not running from a repository root.
The fake executable fixture is explicitly labeled and creates no provider calls.
Tests run subprocesses against that fixture and check complete three-round
execution, per-peer exact resumes, fresh-session replay, full-history transport,
identical final-review snapshots, host turn enforcement, revision guards,
timeout, malformed/incomplete/nonzero results, recovery without duplicate
commits, partial reports, run isolation, and private artifacts.

Fixtures are executable POSIX scripts. Linux execution was recorded for the original
bundle. The repository integration check below adds macOS offline execution;
neither native Windows execution nor real macOS CLI sandbox behavior is claimed. The transport has Windows handling, but that is not a
substitute for testing the target native CLI installation.

The sibling Claude skill tests its independently packaged transport. The repository
validator checks packaged JSON and references. CI compares both copies of the
common runtime with:

```bash
cmp skills/agent-council/scripts/cli_runtime.py skills/claude-cli/scripts/cli_runtime.py
```

Run both suites separately to avoid Python module-name collisions when two
standalone skill directories each provide their own `cli_runtime` module.

## Opt-in live smoke test

This uses real account quota and must be separately authorized on the target
machine. Do not run it merely to install the skill.

Start a one-round council using a non-sensitive topic with one unique marker,
then submit a short host contribution. Advance both discussion calls and final
assessments. Check that Claude received input via stdin and Grok via a prompt
file, exact UUID resumes were used for the assessments, both assessments used
the same final discussion hash, and stderr shows no degraded safety boundary.
Finalize with an actual host synthesis. Keep the local CLI versions and result
shapes with the private smoke-test artifacts.

This verifies the real CLI/session transport, not that a particular model's
engineering recommendation is correct. For quality, use the separate scenarios
in `evals/evals.json` and independently inspect their expected behaviors.
Those model-level evaluations are **provided, not executed**, in this bundle.

## Repository integration check — 2026-09-09

All 37 tests passed on macOS using Python's unittest discovery. The local runner
retained task-created temporary directories instead of recursively deleting them;
all test bodies and assertions executed. No installed provider CLI or account was
called. Python syntax, JSON, skill frontmatter/UI metadata, repository links, and
the Claude marketplace passed validation. The two independently packaged runtime
copies matched byte for byte. CI runs the two suites in separate Python processes.
Native CLI smoke tests and model-level evaluations remain unexecuted.
