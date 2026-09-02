# Network, Files, and Processes

## Contents

- Outbound requests and SSRF
- Redirects, callbacks, and webhooks
- Protocol and proxy boundaries
- Filesystem operations
- Temporary files and archives
- Process execution and privilege
- Resource abuse
- Verification and calibration

## Outbound requests and SSRF

When a lower-trust actor influences a URL, host, path, port, protocol, proxy, or redirect, trace the final destination resolution.

Check:

- accepted schemes and parser behavior
- userinfo, fragments, encoded delimiters, Unicode/IDNA, IPv4 variants, IPv6, zone identifiers
- hostname validation before and after DNS resolution
- private, loopback, link-local, multicast, and special-purpose ranges
- cloud/container metadata and internal control planes
- DNS rebinding and time-of-check/time-of-connect differences
- redirects, including cross-scheme and credential/header forwarding
- proxy environment variables and custom resolvers
- alternate protocols supported by the client library
- request headers, methods, bodies, and credential attachment
- response size, streaming, timeout, decompression, and redirect limits

An allowlist must constrain the property that matters at connection time. A string prefix/suffix check on the original URL is rarely sufficient by itself.

Do not call every user-supplied URL Critical. Prove the reachable internal/sensitive target and the capability gained.

## Redirects, callbacks, and webhooks

Inspect changes to:

- login/OAuth redirect targets
- post-action return URLs
- webhook registration and delivery
- callback verification
- signed URL generation
- service-to-service callbacks

Check exact origin/host/path matching, scheme restrictions, canonicalization, state/nonce binding, signature verification, replay control, tenant ownership, and whether credentials follow redirects.

An open redirect is severity-relevant only through its actual phishing, token leakage, or policy-bypass path.

## Protocol and proxy boundaries

When code implements or configures HTTP/proxy behavior, examine:

- duplicate or conflicting length/framing headers
- hop-by-hop header handling
- forwarded-host/proto/client-IP trust
- cache keys and authorization-sensitive variation
- host routing and absolute-form requests
- normalization differences between CDN, proxy, framework, and application
- CORS as a browser read policy, not server-side authorization
- WebSocket origin/authentication and message limits
- gRPC/message limits and metadata forwarding

Only report request-smuggling/cache-poisoning classes when the repository proves a relevant multi-hop topology or protocol parser mismatch.

## Filesystem operations

Trace the effective path and credentials at the final open/read/write/delete.

Check:

- path traversal and canonical containment
- symlink/hard-link following and race windows
- overwrite/truncate/append semantics
- atomicity and partial-write recovery
- file and directory permissions, umask, ownership, and inherited ACLs
- shared directories across users/tenants
- device files, named pipes, sockets, or special paths
- recursive delete/copy behavior and mount boundaries
- case sensitivity and normalization assumptions across platforms
- untrusted filenames reused in headers, logs, HTML, or commands

Validate containment using filesystem-aware semantics appropriate to the platform, not textual prefix alone.

## Temporary files and archives

Check:

- unpredictable names created atomically
- permissions before content is written
- cleanup on success, failure, cancellation, and process crash where required
- avoidance of shared predictable names
- archive traversal, symlinks, hard links, and overwrite
- file-count, expanded-size, depth, and compression-ratio limits
- processing untrusted content in privileged directories
- handoff between validation and use without attacker substitution

## Process execution and privilege

Beyond command injection, inspect:

- executable identity and PATH search
- inherited environment, credentials, working directory, stdin/stdout, file descriptors
- privilege level, user/group, Linux capabilities, container/host boundary
- sandbox/resource limits and network/filesystem access
- output and error handling, timeout, cancellation, and orphan cleanup
- plugin/helper binaries replaced through writable paths
- scripts downloaded or generated before execution

A child process may be safe from shell injection yet still receive an option, file, configuration, or environment value that expands its capability.

## Resource abuse

Network/file/process inputs can create denial of service or cost amplification through:

- unlimited body/response/download size
- decompression or archive expansion
- recursive imports/includes/redirects
- high fan-out callbacks or scans
- slow streams and missing timeouts
- unbounded subprocess count or output buffering
- repeated failed retries without backoff/budget

Require a plausible cheap trigger and measurable resource path. Do not infer broad outage from a single rejected request.

## Verification

A valid finding includes:

- who controls the destination/path/process input
- parser and normalization steps
- final resolved target or operation
- credentials/privilege at that point
- containment, allowlist, sandbox, and deployment controls checked
- resulting capability and blast radius

## Severity calibration

- Proven arbitrary host command execution or access to a sensitive control plane can be Critical.
- SSRF reaching internal APIs or credentials with meaningful capability is usually High and may be Critical only when compromise is broad/systemic.
- Path traversal enabling bounded tenant-file read/write is usually High.
- Open redirect without token leakage or policy bypass is often Low/Medium.
- Missing timeout or size limit is Medium/High only when a realistic workload can exhaust shared resources.
