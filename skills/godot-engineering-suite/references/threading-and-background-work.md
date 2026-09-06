# Threading and background work

Use for Thread, Mutex, Semaphore, WorkerThreadPool, background loading and CPU-heavy jobs.

## Default rule

Keep Node lifecycle, SceneTree mutation, rendering, physics-world mutation and most Resource operations on the main thread unless official documentation explicitly marks an API thread-safe.

Move pure computation over immutable/copied data to workers. Return plain results and apply them on the main thread.

## Job contract

Each job needs:

- immutable input snapshot or synchronized ownership;
- cancellation/staleness token;
- bounded work and memory;
- explicit result/error channel;
- main-thread application point;
- shutdown behavior.

Do not capture short-lived Nodes in long-running worker closures. Use stable IDs and re-resolve/validate on completion.

## Synchronization

Minimize shared mutable state. Prefer message passing or ownership transfer. When locks are required:

- define lock ordering;
- keep critical sections short;
- never wait for the main thread while holding a lock the main thread may need;
- do not emit signals or call unknown callbacks while locked;
- protect condition predicates against spurious or repeated wakeups.

## WorkerThreadPool

Use task groups for independent uniform work and single tasks for coarse jobs. Avoid flooding the pool with tiny tasks. Store task IDs only as long as needed and wait from a context that cannot deadlock or freeze a frame unexpectedly.

## Resources and loaders

Use documented threaded resource loading APIs rather than loading arbitrary resources from custom threads. Poll progress sparingly and validate request identity before activation.

## Shutdown

Cancel or join owned threads before freeing their dependencies or quitting. Editor tool scripts and hot reload make shutdown paths especially important.

## Verification

Run with repeated start/stop, scene reload, cancellation, application exit and thread sanitizers/native diagnostics where available. Look for races by stressing timing; a single successful run is weak evidence.
