# Python

Use with the domain modules. Type annotations and validators help only where they execute on the reviewed path.

## Contents

- [Values, truthiness, and typing](#values-truthiness-and-typing)
- [Mutability and binding](#mutability-and-binding)
- [Exceptions and control flow](#exceptions-and-control-flow)
- [Async and concurrency](#async-and-concurrency)
- [Resources and I/O](#resources-and-io)
- [Data, numeric, and time behavior](#data-numeric-and-time-behavior)
- [Parsing, models, and serialization](#parsing-models-and-serialization)
- [Imports, packaging, and runtime](#imports-packaging-and-runtime)
- [Verification](#verification)

## Values, truthiness, and typing

Check:

- `None`, absent key, empty collection/string, zero, and false conflated through truthiness
- mutable values accepted under overly broad protocols/unions then used with narrower assumptions
- cast/type-ignore suppressing a reachable runtime mismatch
- annotations assumed to validate external input
- bool accepted where int is expected
- iterator/generator consumed once and reused
- bytes versus text and encoding/error policy
- equality versus identity
- NaN behavior in equality, ordering, sets, and dictionaries

Do not report typing style without a runtime or contract consequence.

## Mutability and binding

Inspect:

- mutable default arguments
- shared class attributes used as per-instance state
- shallow copy where nested isolation is required
- aliasing of dictionaries/lists/models across cache/request/tenant boundaries
- closure late binding
- loop variable/callback capture
- dataclass/model default object reuse depending on actual framework behavior
- in-place mutation while iterating
- function/module global state changed by requests/tests
- copy-on-write assumptions across processes

## Exceptions and control flow

Check:

- broad `except` swallowing cancellation, exit, invariant, or programmer errors
- exception converted to success/default on a required path
- `finally` return/raise masking the original result
- context manager suppressing an exception unintentionally
- exception chaining/source lost where callers classify errors
- cleanup skipped before context manager ownership begins
- partial update followed by exception without rollback/compensation
- generator exception/close semantics
- assertion used for required runtime validation when optimization may remove it
- retry decorator covering non-idempotent side effects

## Async and concurrency

Inspect:

- coroutine created but never awaited
- blocking I/O or CPU work on the event loop
- task created and forgotten despite relevant error/lifetime
- cancellation swallowed or converted into normal result
- timeout without cancelling/cleaning underlying work
- shared mutable state across tasks/threads/processes
- lock held across external I/O unnecessarily or wrong lock type for execution model
- semaphore/queue task completion leaked
- async generator/client/session not closed
- concurrent requests racing to update cache/database/file
- thread/process executor serialization and context propagation

The GIL does not make compound application operations atomic and does not protect multi-process state.

## Resources and I/O

Check:

- files, responses, cursors, sessions, temporary resources, and subprocesses closed on all paths
- atomic file replacement and permissions
- text encoding/newline/platform assumptions
- iterator/stream materialized into unbounded memory
- partial read/write and flush/fsync contract where durability matters
- subprocess shell/args/environment/cwd
- temporary filename races and cleanup
- HTTP client lifecycle, timeout, and streaming response close
- database transaction/session scope

## Data, numeric, and time behavior

Inspect:

- float used for money or exact identifiers
- Decimal context/rounding and conversion from float
- integer/unit conversion and negative values
- naive versus aware datetimes
- local timezone and DST ambiguity
- mutable timezone/config globals
- pandas/NumPy truthiness, view-versus-copy, dtype coercion, overflow, missing values, and index alignment when used
- sorting/grouping with null/NaN behavior
- serialization of Decimal, datetime, bytes, enum, UUID, or large int across contracts

Only load data-library-specific concerns when those libraries are present on the in-scope path.

## Parsing, models, and serialization

Check:

- schema/model validation actually invoked
- pre/post-validation transformations changing validated meaning
- extra/unknown field behavior
- alias/name/default changes
- `None` versus missing handling
- model copy/update bypassing validation
- YAML/object deserialization, pickle-like formats, and dynamic imports
- JSON decoder accepting non-standard values or duplicate keys where relevant
- custom serializer dropping required fields or changing types
- configuration values remaining strings unexpectedly

Framework/version semantics must come from the repository's pinned version or approved primary documentation, not memory.

## Imports, packaging, and runtime

Inspect:

- import-time side effects and circular imports yielding partial modules
- module name shadowing standard/third-party packages
- relative/absolute import behavior under actual entry point
- optional dependency imported unconditionally
- development dependency required at runtime
- package data omitted from build
- editable/local path behavior differing from built wheel/container
- environment variables read at import rather than runtime when reconfiguration/testing requires otherwise
- multiprocessing entry-point guards and picklability
- generated code/schema synchronization

## Verification

Use the pinned Python and dependency versions, environment configuration, and actual entry point. Focused tests/type checks/linters are supporting evidence; they do not replace tracing runtime values and side effects.
