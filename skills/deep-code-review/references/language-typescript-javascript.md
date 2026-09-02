# TypeScript and JavaScript

Use with the domain modules. TypeScript types are compile-time evidence, not runtime validation of external data.

## Contents

- [Runtime values and narrowing](#runtime-values-and-narrowing)
- [Async and promises](#async-and-promises)
- [Functions, closures, and callbacks](#functions-closures-and-callbacks)
- [Objects and collections](#objects-and-collections)
- [Errors and control flow](#errors-and-control-flow)
- [Node and server runtime](#node-and-server-runtime)
- [Package and build semantics](#package-and-build-semantics)
- [Verification](#verification)

## Runtime values and narrowing

Check:

- `undefined`, absent properties, `null`, empty string, zero, and false kept distinct when the contract distinguishes them
- `||` versus `??`
- optional chaining silently converting a required operation into `undefined`
- non-null assertion or cast masking a reachable invalid value
- narrowing invalidated by mutation, aliasing, callback, or `await`
- discriminated unions handled exhaustively at runtime
- `in` including inherited properties where own-property behavior is required
- object spread order overwriting validated/trusted fields with untrusted ones
- destructuring/defaults applying only to `undefined`, not `null`
- numeric string coercion, `NaN`, `Infinity`, `-0`, and precision beyond safe integers
- JSON round trips dropping `undefined`, symbols, non-finite numbers, class prototypes, maps/sets, or exact integer precision

Do not report type looseness alone. Show a reachable runtime value and wrong behavior.

## Async and promises

Inspect:

- missing `await` causing early success, lost error, or cleanup before completion
- `async` callbacks passed to APIs that ignore returned promises
- `map`/`forEach` producing unawaited work
- `Promise.all` fail-fast/partial side effects versus intended all-settled behavior
- sequential awaits accidentally replacing required parallelism, or parallelism violating ordering/limits
- promise created but not returned from a chain
- rejection swallowed by catch/finally or fire-and-forget path
- `finally` return/throw masking prior result/error
- abort/cancellation signal not passed through
- race between overlapping requests/tasks updating shared state
- timeout implemented without cancelling underlying work
- event-loop blocking CPU or synchronous I/O on a request path

A floating promise is a finding only when its lifetime/error/result matters.

## Functions, closures, and callbacks

Check:

- stale closure over mutable state
- loop/callback binding semantics for the project's runtime/transpilation target
- method detached from object and losing `this`
- callback invoked more than once despite single-completion contract
- callback-to-promise wrappers resolving and rejecting on different paths
- default parameter evaluated at call time versus reused object stored elsewhere
- function overload/types promising behavior the implementation does not provide
- comparator failing antisymmetry/transitivity or returning boolean instead of numeric ordering

## Objects and collections

Inspect:

- shallow copy used where nested isolation is required
- mutation of inputs, cached objects, or state containers
- `Array.sort`, `reverse`, `splice`, and similar in-place operations
- Map/Set key identity versus structural identity
- object key coercion and prototype-sensitive dictionaries
- unsafe merge allowing protected fields or prototype keys
- iteration order relied on across incompatible sources
- sparse arrays and holes versus explicit `undefined`
- deduplication with a key that is not the domain identity
- concurrent mutation of module-level singleton state across requests/tests

## Errors and control flow

Check:

- `catch` assuming the thrown value is `Error`
- broad catch converting programmer/invariant failures to success/defaults
- rejected response/body parsing errors incorrectly retried or ignored
- error wrapping that loses machine-readable type/code/cause
- unreachable switch/default behavior after new enum values
- fallthrough or missing return in callback/handler
- Express-like middleware calling `next` after sending or not returning after terminal response
- stream/event emitter errors without a listener or with double completion

## Node and server runtime

Inspect:

- request/response/stream body lifecycle and backpressure
- timers/listeners/watchers not cleared
- Buffer allocation, slicing, shared backing storage, and encoding assumptions
- filesystem path and atomic-write behavior
- child-process executable/args/environment
- server/client timeouts and socket pooling
- process-global environment/config changed per request/test
- worker/thread message serialization and transferable ownership
- ESM/CJS interop, import side effects, and package export conditions
- server-only data bundled into client code

## Package and build semantics

Check `package.json`, lockfile, tsconfig, bundler, and runtime target together:

- source/module target mismatch
- path alias available to typechecker but not runtime
- tree-shaking removing required side-effect registration
- development-only dependency needed at runtime
- conditional export selecting different implementations
- generated declarations/types diverging from runtime API
- optional peer dependency assumed present
- changed transpilation target altering built-in/polyfill behavior

## Verification

Use the declared TypeScript/JavaScript/runtime versions and repository config. Do not rely on latest-language assumptions. Focused typecheck and tests can strengthen evidence, but a clean typecheck does not validate external input or async lifecycle.
