# Go

Use with the domain modules. Review against the version and build constraints declared by the repository because language/library semantics can vary.

## Contents

- [Errors and defer](#errors-and-defer)
- [Interfaces, nil, and zero values](#interfaces-nil-and-zero-values)
- [Slices, maps, and strings](#slices-maps-and-strings)
- [Goroutines, channels, and context](#goroutines-channels-and-context)
- [HTTP, I/O, and servers](#http-io-and-servers)
- [Database and transactions](#database-and-transactions)
- [Time and timers](#time-and-timers)
- [Serialization and APIs](#serialization-and-apis)
- [Packages, initialization, and builds](#packages-initialization-and-builds)
- [Verification](#verification)

## Errors and defer

Inspect:

- returned error ignored or replaced
- named return value modified by deferred function
- deferred cleanup error that must affect success but is dropped
- defer registered only after a step that can partially acquire a resource
- cleanup/rollback called twice or after ownership transfer
- wrapping that breaks `errors.Is`/`errors.As` expectations
- sentinel/type comparison done by string
- partial write/read semantics ignored
- success response/ack emitted before durable completion
- panic/recover boundary converting corrupted state into normal success

Do not require every close error to fail the operation; assess whether buffered/durable completion depends on it.

## Interfaces, nil, and zero values

Check:

- typed nil stored in a non-nil interface
- zero value treated as absent when it is valid
- nil map write, nil channel blocking forever, or nil function call
- interface method set/pointer receiver mismatch changing implementation
- optional dependency/interface left nil on a reachable path
- equality/comparability assumptions for interface dynamic values
- copying values containing mutexes or other no-copy state
- zero-value usability changed by constructor assumptions

## Slices, maps, and strings

Inspect:

- slice aliasing and append mutating shared backing arrays
- retaining a small subslice of a large buffer
- capacity exposed across API boundaries
- map concurrent read/write
- iteration order relied upon
- taking addresses/references of iteration values under the repository's declared Go version and construct
- byte versus rune indexing and UTF-8 boundaries
- string/byte conversion cost on a hot path
- mutation while iterating where semantics lose/duplicate work
- deduplication or map key using the wrong domain identity

## Goroutines, channels, and context

Check:

- goroutine can block forever on send/receive/lock/I/O
- caller cancellation not observed or context replaced with background context
- context stored beyond request lifetime or passed as struct state
- spawned work outlives required resources or request identity
- channel closed by a receiver/non-owner or sent after close
- multiple close paths
- WaitGroup add/wait ordering and missing Done on failure
- semaphore/token leaked
- lock held during network/blocking work
- unbounded goroutine fan-out
- select default causing busy loop or dropped required work
- cancellation between external effect and durable state

Provide a concrete interleaving or leak path.

## HTTP, I/O, and servers

Inspect:

- response body closed and, where connection reuse matters, consumed appropriately
- request body/response size limits
- client/server transport and timeout configuration
- shared `http.Client`/Transport lifecycle versus per-request creation
- headers/status written after body
- handler continuing after error response
- proxy/forwarded header trust
- URL/path resolution semantics
- streaming backpressure and flush errors
- file permissions and atomic replacement
- scanner/token size defaults for supported input
- shutdown draining and context deadlines

A default client without timeout is reportable when the call can hold shared resources or violates an established latency/shutdown contract.

## Database and transactions

Check:

- `rows.Close`, `rows.Err`, and scan errors
- transaction handle actually used by every intended query
- commit/rollback error and defer ordering
- context cancellation semantics
- affected-row checks
- nullable values and zero-value mapping
- statement/query lifetime
- read-modify-write races and constraints
- network call inside transaction
- connection pool settings and leaked rows/bodies

## Time and timers

Inspect:

- timer/ticker stop and channel draining where required
- repeated `time.After` allocation in loops
- wall clock versus monotonic elapsed-time behavior
- duration units and integer conversion
- zero/negative duration semantics
- timezone/calendar assumptions
- deadline derived from already-expired context
- ticker goroutine/listener cleanup

## Serialization and APIs

Check:

- exported fields/tags and `omitempty` changing zero/absent semantics
- unknown fields and compatibility expectations
- pointer versus value fields for optionality
- custom marshal/unmarshal preserving invariants
- map key/string conversion
- enum zero/default value
- embedded fields and name conflicts
- decoder accepting trailing or multiple values unexpectedly
- partial decode followed by use after error

## Packages, initialization, and builds

Inspect:

- `init` side effects and ordering
- package-level mutable state shared across requests/tests
- import cycle workarounds that duplicate state/policy
- build tags/GOOS/GOARCH/cgo variants
- generated code synchronization
- module replacement, workspace, vendoring, and checksum changes
- cgo ownership/thread/ABI boundaries
- executable relying on working directory

## Verification

Use the repository's Go version, build tags, race-sensitive tests, and platform targets. A clean `go test` does not prove race freedom unless relevant execution occurs; a race report requires a causal trace to changed code.
