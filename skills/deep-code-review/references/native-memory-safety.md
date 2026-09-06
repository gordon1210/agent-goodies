# Native Memory Safety

Use for C, C++, unsafe Rust, FFI, kernel/driver code, binary parsers, manual allocation, and direct pointer arithmetic.

## Contents

- [Establish the memory model](#establish-the-memory-model)
- [Bounds and integer arithmetic](#bounds-and-integer-arithmetic)
- [Lifetime and ownership](#lifetime-and-ownership)
- [Initialization and representation](#initialization-and-representation)
- [Concurrency](#concurrency)
- [FFI and system boundaries](#ffi-and-system-boundaries)
- [Verification](#verification)
- [Severity calibration](#severity-calibration)

## Establish the memory model

Identify:

- allocation owner and deallocator
- object lifetime and aliasing rules
- buffer base, length, capacity, and element size
- thread ownership and synchronization
- representation across FFI/ABI boundaries
- whether input lengths, offsets, counts, or tags are attacker-controlled

Compilers and sanitizers are evidence, not proof of all runtime paths.

## Bounds and integer arithmetic

Trace arithmetic before allocation, indexing, copying, serialization, and pointer movement.

Check:

- addition/multiplication overflow in `count * size`, `offset + length`, alignment, and capacity growth
- signed/unsigned conversion and negative values becoming large
- truncation across integer widths or ABI types
- units: bytes versus elements, code units, pixels, frames, sectors
- inclusive/exclusive ends and sentinel space
- validation performed before versus after overflow
- partial reads/writes and return-value handling
- parser-declared length versus actual remaining buffer

A bounds check on an already-overflowed expression may be ineffective.

## Lifetime and ownership

Inspect:

- use-after-free, double free, invalid free, and ownership transfer
- pointers/references retained beyond backing storage or callback scope
- container reallocation invalidating pointers/iterators/views
- stack addresses escaping scope
- callbacks after object destruction or cancellation
- destructor/drop ordering and re-entrancy
- reference counting cycles, weak references, and atomicity
- exception/error paths that skip initialization or cleanup

In unsafe Rust, require a documented and actually maintained safety invariant for every unsafe block or API boundary.

## Initialization and representation

Check:

- uninitialized reads and padding disclosure
- partial struct initialization
- union/tag mismatches
- invalid enum/discriminant values from bytes or FFI
- alignment and packed structures
- strict aliasing/effective-type assumptions
- endianness and wire-layout assumptions
- null termination and embedded NUL behavior
- format strings and variadic argument types

## Concurrency

Inspect:

- data races and non-atomic publication
- lock ordering and lifetime of protected data
- atomic memory ordering relative to the required invariant
- ABA and reclamation schemes
- callbacks/signals interrupting non-reentrant code
- object destruction while another thread can access it
- reference counts or flags modified without the required synchronization

Do not report a race without a concrete concurrent access path.

## FFI and system boundaries

Check:

- ABI, calling convention, layout, ownership, allocator, and exception/panic boundaries
- length and encoding contracts
- callbacks stored by the foreign side
- thread-affinity requirements
- error codes and partial-success semantics
- file descriptor/handle ownership
- pinning/movement assumptions

Never allow exceptions or unwinds to cross an ABI boundary that forbids them.

## Verification

Use in-scope code plus callers, allocation sites, cleanup, and parser entry points. Existing sanitizer/fuzz tests can strengthen evidence. Do not run unsafe fuzzing against production or external systems.

A finding should name the exact invalid state and operation: out-of-bounds read/write, use-after-free, uninitialized disclosure, double free, race, or ABI violation.

## Severity calibration

- Production-reachable memory corruption with credible attacker control and code-execution potential may be Critical.
- Bounded out-of-bounds access, use-after-free, or parser corruption is generally High when reachable.
- A deterministic local CLI crash from malformed input may be Medium.
- “Unsafe exists” or “raw pointer used” is not a finding without a violated invariant.
