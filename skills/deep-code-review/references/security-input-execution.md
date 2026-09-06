# Untrusted Input and Execution

## Contents

- Source-to-sink method
- Query and expression injection
- Shell and process arguments
- HTML, templates, and browser sinks
- Paths, archives, and uploads
- Deserialization and parser boundaries
- Secondary channels
- Verification and calibration

## Source-to-sink method

For each changed sink, trace the exact value back to its source and record transformations in order.

Distinguish:

- allowlist validation from denylist filtering
- syntax validation from semantic authorization
- normalization from canonicalization
- output encoding from input validation
- prepared data values from dynamic identifiers or query fragments
- argument-vector execution from shell parsing
- safe rendering context from raw HTML/script/URL/CSS contexts

A sanitizer valid for one sink may be unsafe for another.

## Query and expression injection

Inspect dynamic construction of:

- SQL, NoSQL, graph, search, or analytics queries
- ORM raw fragments, identifiers, sort/order clauses, filters, projections, and includes
- LDAP, XPath, JSONPath, regular expressions, glob patterns, or policy expressions
- template or expression engines
- spreadsheet formulas and CSV exports

Check whether:

- data values use the library's actual parameter API
- identifiers and operators come from a closed internal mapping
- escaping matches the specific grammar and encoding
- second-order values stored earlier become executable later
- decoded or normalized values differ from the validated representation
- query composition helpers preserve parameterization
- user-controlled regular expressions or patterns have bounded complexity

Do not flag string construction when all dynamic fragments are trusted closed-set values and untrusted data remains parameterized.

## Shell and process arguments

Trace data into process creation, scripts, interpreters, package managers, and command wrappers.

Differentiate:

- direct executable plus argument vector
- invocation through a shell
- interpreter flags that evaluate code
- environment variables, working directory, PATH, executable lookup, and inherited file descriptors

Check:

- shell metacharacters and quoting across the actual shell/platform
- user-controlled executable names or PATH lookup
- arguments that are themselves interpreted as code, templates, URLs, config, or filenames
- option injection through values beginning with `-`
- command separators introduced after decoding
- privileged process context and sandbox boundaries
- whether timeouts/output limits prevent resource abuse

`spawn(executable, args)` is safer than a shell string, but the called program may still interpret dangerous arguments.

## HTML, templates, and browser sinks

Inspect untrusted data reaching:

- raw HTML insertion, DOM APIs, markdown renderers, email templates
- script, event-handler, CSS, URL, SVG, or attribute contexts
- server-side templates and client hydration payloads
- redirects, links, iframe sources, postMessage, and clipboard/download content

Check context-specific encoding, URL scheme restrictions, sanitizer configuration, and whether sanitized content is later mutated. Trusted authorship alone may not be sufficient when content is imported or collaborative.

Do not report XSS from normal framework text interpolation unless the in-scope implementation bypasses or defeats escaping.

## Paths, archives, and uploads

Trace filename and path handling through decoding, normalization, joining, canonicalization, filesystem resolution, and final open/write.

Check:

- absolute paths, parent traversal, alternate separators, device paths, UNC paths, encoded traversal
- canonical path containment after symlink resolution where relevant
- archive entries with traversal, absolute paths, symlinks, hard links, or duplicate names
- extraction size, file count, compression ratio, and recursive archives
- upload type determined by content and intended use, not only extension or client MIME
- overwrite behavior, permissions, atomic replacement, and executable locations
- filename use in headers, HTML, logs, or downstream commands

A prefix string comparison is not reliable containment without correct path-boundary handling.

## Deserialization and parser boundaries

Inspect changed use of:

- native object serialization, pickle-like formats, YAML object tags, XML entities
- polymorphic type metadata or class-name resolution
- binary/protocol parsers and schema evolution
- image, media, document, and archive libraries
- custom parsers with recursion, length, offset, or integer arithmetic

Check whether untrusted data can instantiate behavior, resolve arbitrary types, fetch external entities, allocate unbounded memory, recurse deeply, or produce ambiguous interpretations between validators and consumers.

Use safe modes and explicit schemas where the library provides them. Do not assume “internal file” means trusted when users, imports, artifacts, or compromised services can influence it.

## Secondary channels

Also inspect:

- header splitting and response-splitting values
- log forging only where logs drive security decisions or operational response
- email header/recipient injection
- format strings in native languages
- prototype/property pollution and unsafe object merging
- mass assignment of roles, ownership, status, pricing, or internal flags
- Unicode confusables or normalization when identity/security comparisons depend on them
- parser differentials across proxy, framework, signature verifier, and application

## Verification

A valid finding identifies:

- attacker-controlled source
- exact dangerous sink or security decision
- transformations and why they fail
- a representative payload or input class when safe to describe
- resulting capability, not merely malformed output
- privilege and deployment reachability

Check framework/library documentation available in the repository or via approved primary sources when semantics are uncertain. Do not guess.

## Severity calibration

- Injection yielding broad remote code execution can be Critical when production reachability and privilege are proven.
- Injection yielding bounded data access or action is usually High.
- Stored XSS, formula injection, or parser abuse varies from Medium to High based on victim, capability, and deployment.
- A parser crash on a single bounded request is not Critical unless it reliably causes broad outage.
- Untrusted regex or archive expansion needs a plausible resource-exhaustion path, not just unbounded syntax.
