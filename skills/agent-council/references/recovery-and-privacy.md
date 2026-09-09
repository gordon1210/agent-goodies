# Recovery, concurrency, and privacy

## Durable ownership

`state.json` is authoritative. It stores the immutable task/config snapshot,
ordered committed contributions, peer session IDs, final assessments, pending
attempt, and recovery decisions. State replacements use a temporary file,
fsync, and atomic rename; POSIX directory fsync is also requested. This does not
promise stronger crash semantics than the underlying filesystem provides.

`transcript.md`, `transcript.jsonl`, and `report.md` are derived. Regenerate them
with `export` if a crash occurred after a state commit but before an export.
Message/charter/config checksums detect accidental edits; they are not signatures
or protection against a malicious local actor who can rewrite the state file.

Writers hold an OS lock for the whole mutation, including peer calls. Another
writer fails rather than racing. Read-only `status`/`brief` observe an atomic
snapshot without waiting for a model. The lock file remains in place and the OS
releases its lock when a process exits; never delete it to break an active lock.
Do not share native peer session IDs with unrelated processes or concurrent jobs.
The run lock cannot control an external CLI started manually against the same ID.

## Call journal

Each attempted peer call has a unique UUID directory under `attempts/`:

- `prompt.txt`: the exact full input snapshot submitted to this peer.
- `request.json`: argv, cwd, non-secret override values, prompt hash and coverage.
- `stdout.json`, `stderr.log`: separate raw captures.
- `outcome.json`: completed local process status and timeout/interruption state.

The pending attempt is committed **before** starting the process. Only a
validated successful result advances the logical speaker. A failure therefore
cannot silently disappear or become an accepted contribution. There is no
exactly-once promise for remote inference or billing: a process can fail after
sending a request or saving part of its native session.

The full discussion remains intact on failures. Do not infer that a timed-out
native session is clean, retry the same message automatically, skip a participant,
or change provider/model/permissions to force progress.

## Recovery commands

Inspect `status` and the pending attempt's files first. If a completed successful
response was captured but not committed, this command validates and commits it
without another model call:

```bash
python3 "$COUNCIL" recover --run-dir /approved/work/council-01 --accept
```

It requires a successful `outcome.json`, valid terminal JSON, matching prompt
hash and discussion snapshot, and the expected session identity. Running it
again after commitment does not append a duplicate contribution.

When the attempt is incomplete, invalid, or deliberately abandoned, first verify
that the **actual old invocation has stopped**. A stored PID alone is not proof:
PIDs may be reused, and a run directory may be on a shared filesystem. The helper
does not kill arbitrary saved PIDs or silently override locks. Then:

```bash
python3 "$COUNCIL" recover \
  --run-dir /approved/work/council-01 \
  --discard --confirm-stopped \
  --reason "Inspected the failed attempt; the old CLI process has exited."
python3 "$COUNCIL" advance --run-dir /approved/work/council-01
```

`--confirm-stopped` is a human/host attestation, not a process discovery result.
Discard records the reason and clears **only that peer's** native session ID.
The next call starts fresh with the full canonical discussion, even in resume
mode. It can consume another paid/quota-bearing request; no rollback is implied.
Other peers' committed contributions and sessions remain untouched.

On ordinary POSIX timeout, Ctrl-C, or a handled supervisor SIGTERM, the transport
terminates its owned process group. SIGKILL cannot run cleanup; inspect possible
remaining child processes before recovery. Native Windows only terminates the
owned CLI process and offers no process-tree guarantee in this implementation.

## Partial closure

After resolving any pending attempt, use `finalize --partial --reason ...` with
a real host report and a fresh revision to stop an incomplete council. The
report is marked PARTIAL and includes the number of actual contributions/calls.
Disclose which requested inputs are missing. Do not report a failed provider's
error as that provider's opinion or imply it endorsed the host's conclusion.

## Data boundary

Only approved topic/context, approved updates, and public discussion contributions
are sent to peers. `preflight.json`, CLI diagnostics, credentials, the host's
private chat, and hidden reasoning traces are not included in council prompts.
The prompt explicitly labels peer material as evidence, not executable authority.
That is defense in depth, not a mathematical prompt-injection guarantee.

The council is not an offline model system: the official CLIs normally send
prompts to their configured remote providers. Tools-disabled does not mean
network-disabled. Existing authentication and provider billing remain intact.

Place run artifacts in an approved private location, preferably outside Git.
Files are 0600 and new directories 0700 on POSIX; these settings are not portable
Windows ACL guarantees or encryption. Raw CLI logs and native sessions can retain
sensitive data. Do not upload/commit the run directory or automatically delete
native sessions. Retention and cleanup are separate caller decisions.
