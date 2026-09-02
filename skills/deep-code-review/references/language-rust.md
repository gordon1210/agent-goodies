# Rust

Use with correctness, concurrency, security, and native-memory modules as applicable. Compilation rules remove many classes of defects but do not establish application invariants.

## Contents

- [Panic and failure boundaries](#panic-and-failure-boundaries)
- [Results and error propagation](#results-and-error-propagation)
- [Ownership and lifetimes at the semantic level](#ownership-and-lifetimes-at-the-semantic-level)
- [Async and concurrency](#async-and-concurrency)
- [Numeric and conversion behavior](#numeric-and-conversion-behavior)
- [Collections and iteration](#collections-and-iteration)
- [Serialization and protocols](#serialization-and-protocols)
- [Unsafe and FFI](#unsafe-and-ffi)
- [Cargo, features, and build](#cargo-features-and-build)
- [Verification](#verification)

## Panic and failure boundaries

Inspect reachable use of:

- `unwrap`, `expect`, indexing, assertions, `panic!`, `unreachable!`, `todo!`
- integer operations that panic in some build modes or wrap in others
- parsing/conversion assumptions
- poisoned locks and task join errors
- destructor/drop code that can panic during unwinding
- panic crossing FFI or task/process isolation boundaries

A panic on invalid packaged startup configuration may be intentional. A panic from untrusted request/data on a shared service path may be a real availability defect.

## Results and error propagation

Check:

- `?` converting errors into a broader type that changes retry/status behavior
- `map_err` or context wrapping losing source/category needed by callers
- ignored `Result` or return values from writes, flushes, closes, renames, and process exits
- partial success followed by error without compensation/idempotency
- retry loops consuming ownership or repeating non-idempotent effects
- `Drop` used for fallible required completion
- error branch leaving state marked successful

## Ownership and lifetimes at the semantic level

Safe Rust can still have wrong ownership behavior:

- cloning state so updates affect a copy rather than the shared source of truth
- `Arc`/`Rc` cycles leaking long-lived objects
- interior mutability allowing re-entrant borrow panic or hidden shared state
- values removed/taken before a later fallible step and not restored
- guards dropped too early or held too long
- temporary files/resources deleted when a handle/object drops earlier than expected
- references/views tied to a buffer that is logically reused or mutated through safe APIs

Do not flag cloning only for cost unless the path and scale make it material.

## Async and concurrency

Inspect:

- blocking filesystem/network/CPU work on an async executor thread
- mutex/RwLock guard held across `.await`
- inconsistent lock order and re-entrancy
- spawned task whose error/lifetime/cancellation is ignored
- detached task accessing state after request/shutdown
- cancellation between side effect and durable state
- select/race branches that are not cancellation-safe
- channel capacity, sender/receiver lifetime, and close behavior
- semaphore permit leaked or released before protected work
- async recursion or fan-out without bounds
- thread-local/task-local/request context lost across spawn
- atomics whose ordering does not establish the intended publication invariant

Prove a concrete interleaving; do not infer deadlock from “multiple locks” alone.

## Numeric and conversion behavior

Check:

- `as` casts truncating, wrapping, changing sign, or losing pointer/integer width
- `try_from` errors ignored/defaulted
- byte/element/unit calculations
- overflow before a bounds/allocation check
- float-to-int behavior and NaN ordering
- duration/time conversion and zero/negative semantics represented through signed inputs
- index derived from external length or offset

## Collections and iteration

Inspect:

- HashMap iteration order relied upon
- entry/update logic with the wrong identity or default
- draining/removing while partial failure occurs
- iterator laziness changing when side effects execute
- `collect` losing errors through an unintended target type
- `filter_map` silently discarding error/invalid states
- range inclusivity
- Vec capacity/length confusion in unsafe adjacency
- shared cache key missing tenant/version/context

## Serialization and protocols

Check serde and custom formats for:

- defaults hiding missing required fields
- `deny_unknown_fields` or permissive behavior changing compatibility intentionally/unintentionally
- untagged enum ambiguity and variant ordering
- enum rename/tag/content changes
- `skip_serializing_if` changing absent versus null/zero semantics
- flattening collisions
- borrowed deserialization lifetime/use assumptions
- binary length/version validation
- custom `Deserialize` maintaining invariants

Do not impose strict unknown-field rejection without a contract; forward compatibility may require permissiveness.

## Unsafe and FFI

When `unsafe`, raw pointers, transmute, manual allocation, or FFI changes appear, load `native-memory-safety.md`.

Additionally check:

- safety comments match all callers and are enforceable by the API
- unsafe function preconditions are validated or clearly delegated
- `Send`/`Sync` implementations are sound
- pinning/self-reference assumptions
- allocator and ownership agreement across FFI
- Rust panic does not unwind across forbidden ABI boundary
- C strings, lengths, nulls, and encodings
- repr/layout/discriminant compatibility

Treat unsafe blocks as proof obligations, not automatic findings.

## Cargo, features, and build

Inspect:

- feature combinations, including no-default/default/all-features paths used by the repo
- optional dependency activated only in some builds
- target-specific cfg/build tags
- `build.rs`, procedural macros, and generated code
- crate type, panic strategy, LTO, and profile changes that affect behavior
- lockfile/source/checksum changes
- public feature unification changing dependency behavior

## Verification

Use the repository's pinned toolchain, edition, features, targets, and lint policy. Run focused `cargo check/test` only when safe. Compiler acceptance does not disprove logical races, authorization failures, rollout breaks, or cancellation ambiguity.
