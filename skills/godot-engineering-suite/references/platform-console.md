# Console platforms

Use for console-readiness architecture and work performed inside an authorized console SDK environment.

## Boundaries

Official console SDKs, export templates and documentation are generally provided through platform-holder or approved third-party agreements. Do not invent commands, APIs, certification rules or distribution paths from public desktop guidance.

Confirm that the user and environment are authorized before handling confidential SDK material. Keep such material out of public repositories, prompts, logs and artifacts.

## Portable project design

- Abstract platform services, storage, users, achievements and commerce.
- Support controller-only UI and user reassignment.
- Avoid desktop-only filesystem, process and window assumptions.
- Bound memory, loading stalls and shader/render complexity.
- Plan suspend/resume, sign-out and storage-device failure.
- Keep feature flags and platform resources isolated.

## Certification mindset

Build deterministic error handling for network loss, controller disconnect, user change, storage full, corrupted save, suspend/resume and service unavailability. Do not defer these paths until submission.

## Native dependencies

Every addon/GDExtension must support the target SDK, compiler, architecture and packaging rules. A desktop binary is irrelevant. Verify source availability and license compatibility early.

## Validation

Use the approved porting/export provider and current platform-holder test suites. Track platform-specific failures separately from shared game behavior. Public CI should test portable core logic; confidential builds belong in the authorized environment.
