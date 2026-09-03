# Types, Modeling, Narrowing, and Errors

Read this reference for implementation-level TypeScript decisions: inference, annotations, `unknown`, `any`, narrowing, assertions, object and union modeling, generics, classes, branded values, error contracts, and runtime validation.

## 1. Keep the type system in its proper role

TypeScript checks a model of JavaScript code at development/build time. Types are generally erased and do not validate runtime values.

Consequences:

- A value arriving from JSON, HTTP, a database driver, environment, storage, a message channel, native code, or a third-party SDK is not trustworthy merely because a generic or annotation names a type.
- A type assertion changes what the checker believes; it does not inspect or transform the value.
- Structural compatibility can accept values with extra fields, forged brands, unexpected prototypes, accessors, or runtime semantics not represented by the type.
- `private` and `protected` are API-design tools, not access-control or secret-storage boundaries.
- Exhaustive checking is useful only when all runtime producers are constrained to the modeled variants.
- Declaration files describe a contract; they do not enforce that JavaScript implementations satisfy it.

Use types to make validated states and internal contracts clear. Use runtime checks at trust boundaries.

## 2. Inference versus annotation

Prefer inference when it is local, precise, and obvious. Add an explicit annotation when it:

- Defines a public or cross-package contract.
- Prevents accidental widening or captures intended optionality.
- Makes recursive code or mutually recursive types checkable.
- Constrains an implementation to an interface without changing inferred value precision.
- Prevents an exported declaration from naming private or unstable implementation details.
- Documents a unit, callback protocol, effect, or return guarantee that inference cannot express clearly.
- Stabilizes declaration output across implementation changes or compiler generations.
- Improves diagnostics at the construction site instead of far downstream.

Avoid annotations that merely repeat a trivial initializer or erase useful literal/inferred information.

### `satisfies`

Use `satisfies` when a value should be checked against a shape while preserving its own inferred type:

```ts
const routes = {
  health: "/health",
  users: "/users",
} satisfies Record<string, `/${string}`>;
```

It does not make runtime values safe and does not freeze mutability. Choose `as const` only when deep literal/readonly inference is genuinely part of the intended model; do not apply it mechanically to every object.

## 3. `unknown`, `any`, and `never`

### `unknown`

Use `unknown` for values whose structure is not yet established. Narrow or validate before use. It is appropriate for:

- Parsed external values when the parser's return type is unchecked.
- Caught exceptions.
- Plugin or message inputs.
- Generic boundary adapters before dispatch.
- Unstructured metadata intentionally preserved but not interpreted.

Do not spread `unknown` deep into trusted code. Validate once and pass a useful internal type.

### `any`

`any` disables important checker guarantees in both directions and propagates easily.

Use explicit `any` only when the actual contract is intentionally unchecked and no safer representation is practical, for example a narrowly isolated compatibility adapter around an untyped dynamic API. Even then:

- Keep it inside one boundary module.
- Convert to `unknown` or a validated type immediately when possible.
- Do not export it accidentally through inference.
- Document why the value cannot be modeled.
- Add runtime tests for behavior the checker cannot verify.

Never introduce `any` merely to make a type error disappear, avoid a generic constraint, or access a property on an uncertain value.

### `never`

Use `never` to represent impossible completion or impossible variants. An exhaustive check is useful when the set is genuinely closed:

```ts
function assertNever(value: never): never {
  throw new Error(`Unexpected state: ${String(value)}`);
}
```

Do not assume this protects against malformed external input; validate the discriminant first. Avoid including sensitive payloads in invariant errors.

## 4. Narrowing and guards

Prefer built-in control-flow narrowing where it expresses the evidence:

- `typeof` for primitives and functions.
- `Array.isArray` for arrays.
- `instanceof` only when constructor identity is reliable across realms, packages, bundles, and serialization boundaries.
- `in` only with awareness of inherited properties and optional-property behavior.
- Equality/discriminant checks for closed unions.
- Explicit nullish checks rather than truthiness when `0`, `false`, or `""` are valid.
- `Object.hasOwn` or an equivalent repository-supported own-property check when ownership matters.

### User-defined type predicates

A predicate such as `value is User` is a promise to the checker. Its implementation must validate every property/invariant that callers rely on. Weak predicates create unsound trusted code.

Rules:

- Accept `unknown` at external boundaries.
- Check object-ness, null, arrays versus records, own properties, primitive types, ranges, formats, and nested structures as required.
- Bound recursion, arrays, strings, and aggregate work for untrusted input.
- Do not call getters or arbitrary methods unintentionally while “validating” hostile objects.
- Test near misses and adversarial cases, not only valid examples.

### Assertion functions

Assertion functions are useful when failure should throw and successful return establishes an invariant:

```ts
function assertNonEmpty(value: string): asserts value is string & { readonly __nonEmpty: unique symbol } {
  if (value.length === 0) {
    throw new Error("Expected a non-empty string");
  }
}
```

Keep the assertion implementation simple and trustworthy. Do not use an assertion signature to lie about checks the body does not perform.

## 5. Type assertions and non-null assertions

A type assertion is justified only when stronger evidence exists outside what TypeScript can express.

Before asserting, ask:

1. Can inference or an annotation express the contract?
2. Can control-flow narrowing establish it?
3. Can a type predicate or assertion function prove it?
4. Can the external value be parsed into a validated representation?
5. Is the library typing incorrect, and can it be augmented or wrapped locally?
6. Does the repository forbid assertions entirely?

Reject:

- `value as DesiredType` immediately after parsing untrusted data.
- `as unknown as T` used to bypass incompatible structures.
- `as any` used to access private or missing members.
- Assertions that discard nullability, readonly-ness, variance, or incompatible discriminants without evidence.
- Assertions scattered through callers instead of one reviewed interop boundary.

When an assertion remains necessary:

- Assert the narrowest fact possible.
- Keep it adjacent to the runtime or API evidence.
- Avoid exporting the asserted value before validation.
- State the current invariant, not historical justification.
- Add a test that would fail if the assumption changes.

### Non-null assertions

`value!` suppresses null/undefined checking and emits no runtime check. Prefer:

- Explicit checks.
- Validated construction.
- Early returns.
- A map lookup API or helper that throws with an invariant-specific message.
- Restructuring initialization so required state exists before use.

A non-null assertion can be acceptable for a framework lifecycle guarantee or immediately adjacent proven invariant when the repository permits it. It must not hide ordinary race, optional configuration, DOM lookup, or external-data failure.

## 6. Objects, optionality, and indexed access

Distinguish:

- Property absent.
- Property present with `undefined`.
- Property present with `null`.
- Empty string/collection.
- Default inherited from another source.

`exactOptionalPropertyTypes` can make optional-property intent more precise. Enabling it repository-wide is a migration decision; do not toggle it incidentally.

### Index signatures and records

`Record<string, T>` describes a static mapping shape but does not guarantee every arbitrary key exists at runtime. With unchecked indexed access, `record[key]` can still be absent.

Use:

- `Map` when arbitrary keys, explicit absence, insertion order, or non-string keys are natural.
- A record/object for JSON-like finite string-keyed data when prototype and key-safety semantics are controlled.
- A finite mapped type when the key set is closed.

For untrusted keys:

- Consider prototype-related names and own-property checks.
- Avoid merging into privileged configuration through generic recursive assignment.
- Bound key count and nesting.
- Do not rely on a TypeScript index signature as a runtime access guarantee.

`noUncheckedIndexedAccess` can expose missing-key assumptions. Preserve repository policy and address findings semantically rather than adding non-null assertions everywhere.

## 7. Discriminated unions and state

Use discriminated unions when a closed set of states carries different data:

```ts
type LoadState<T> =
  | { readonly status: "idle" }
  | { readonly status: "loading"; readonly requestId: string }
  | { readonly status: "ready"; readonly value: T }
  | { readonly status: "failed"; readonly error: AppError };
```

Benefits:

- Invalid combinations are harder to construct.
- Exhaustive handling can be verified.
- State-specific data is present only where valid.

Avoid:

- Multiple booleans whose combinations are unclear.
- One giant union shared across unrelated workflows.
- Generic state-machine types that obscure simple local state.
- Optional fields on every variant plus assertions in consumers.
- Treating unvalidated external discriminants as exhaustive.

Use ordinary object state or an enum when payload differences and exhaustive handling do not justify a union.

## 8. Literal types, enums, and constants

Choose from runtime and API needs:

- String/number literal unions for compile-time closed values with no required runtime namespace.
- Frozen/readonly constant objects when runtime values and derived union types are both useful.
- `enum` when its runtime object, reverse mapping, declaration behavior, or framework integration is deliberately required.
- Avoid `const enum` across published package boundaries unless every consumer and transpiler contract supports its inlining semantics. Version skew can produce incorrect runtime values.

Adding a member to a public union or enum may break exhaustive consumers even when runtime compatibility appears additive. Review SemVer and caller behavior.

## 9. Interfaces, type aliases, and classes

### Interface versus type alias

Use either according to semantics and repository convention:

- Interfaces are useful for extendable object contracts, declaration merging when intentionally required, and class implementation.
- Type aliases are useful for unions, intersections, tuples, primitives, mapped/conditional types, and closed data models.

Do not rewrite between them solely for style. Be cautious with public declaration merging: it is a compatibility and extension contract.

### Classes

Use a class when identity, encapsulated lifecycle, mutation, inheritance/polymorphism, or framework expectations make it clearer than functions and plain data.

Rules:

- Keep constructors valid on return; avoid partially initialized public instances.
- Prefer explicit composition over deep inheritance hierarchies.
- Do not expose mutable public fields when invariants matter.
- Remember that TypeScript parameter properties and access modifiers generally compile to ordinary JavaScript properties unless native private fields are used.
- Native `#private` fields have runtime brand checks and different compatibility/serialization behavior from `private`.
- Avoid relying on `instanceof` across serialized data, realms, duplicated packages, or structurally compatible objects.
- Define cleanup explicitly when a class owns subscriptions, workers, handles, or async lifecycle. Garbage collection is not a deterministic shutdown protocol.

## 10. Generics and type-level computation

Add a generic when callers or implementations genuinely vary over a type while preserving a meaningful relationship.

Good reasons include:

- Input/output correlation.
- Container element type.
- Reusable algorithm over a capability.
- Framework or library boundary with several real type instances.
- Public API that must preserve caller-specific information.

Avoid a generic when:

- It has one credible instantiation.
- It exists only to avoid naming a concrete type.
- The implementation repeatedly asserts back to one concrete type.
- It makes diagnostics and declarations substantially worse without preventing a real bug.
- A union or overload expresses the finite behavior more clearly.

### Constraints and defaults

- Constrain only capabilities the implementation uses.
- Avoid `T extends object` when a specific record or interface is required.
- Do not use `{}` to mean an empty object; it accepts most non-nullish values.
- Keep generic defaults conservative; changing them can alter inference for downstream callers.
- Ensure optional generic parameters do not produce impossible or misleading combinations.

### Conditional and mapped types

Use them when they express a stable relationship callers benefit from. Avoid:

- Deep recursive types with poor termination behavior.
- Large distributive conditional types over broad unions.
- Types that parse arbitrary strings or mirror a runtime parser without corresponding runtime checks.
- Clever transformations that make public errors unreadable.
- Type computation used to avoid a small explicit domain model.

Measure compiler cost and inspect emitted declarations for shared/public type utilities.

## 11. Variance, callbacks, and mutability

TypeScript's structural type system and method/function variance rules can permit assignments that require care.

- Prefer readonly views for data callers should not mutate, while remembering `readonly` is shallow unless nested types are also readonly.
- Do not cast away readonly-ness to mutate shared state.
- Be explicit about callback parameter and return contracts at public boundaries.
- Avoid methods that both accept and return highly generic mutable containers without a clear variance story.
- Treat event handlers and callback registries as lifecycle resources; unregistering and error ownership matter beyond their types.
- Do not assume a function accepting a narrower callback is safe solely because an assignment compiles under relaxed settings.

Use strict function checking and repository lint policy as evidence, then reason about actual call direction.

## 12. Branded and opaque values

Brands can distinguish structurally identical primitives such as `UserId`, `OrderId`, validated paths, or units.

Use them when:

- Confusion is credible and costly.
- Values cross important APIs repeatedly.
- A small set of constructors/validators can own creation.
- Serialization converts deliberately back to primitives.

Do not:

- Export a brand that callers can obtain only by assertion.
- Brand every primitive in a small local function.
- Treat a compile-time brand as runtime validation or secrecy.
- Use a brand when separate object fields or names are already clear.

A branded value must have a trustworthy constructor or parser. Keep unsafe construction internal.

## 13. Error taxonomy

Classify failures before choosing representation:

- **Validation/domain:** caller can correct input or state.
- **Authentication/authorization:** identity or permission failure.
- **Not found:** absent resource under the system's disclosure policy.
- **Conflict/precondition:** concurrency, duplicate, or state mismatch.
- **Transient dependency:** retry may help under a bounded policy.
- **Permanent dependency/configuration:** retry without change will not help.
- **Timeout/cancellation:** operational outcome distinct from arbitrary failure.
- **Invariant/bug:** the program reached a state its own logic should prevent.

Do not collapse materially different caller actions into one opaque string.

## 14. Exceptions, result unions, and error classes

Follow the repository's established model unless the task justifies a local boundary.

### Exceptions

Use exceptions when failure is exceptional and surrounding APIs already use throw/reject semantics.

- Throw `Error` instances for errors created by the application.
- Preserve a causal chain with the platform-supported `cause` mechanism when useful.
- Normalize unknown thrown values at a boundary before logging or exposing them.
- Avoid catch-and-rethrow that loses stack/cause or adds no context.
- Do not use exceptions for ordinary high-frequency branch control when explicit results are clearer.

### Result unions

A discriminated result can be useful when failure is an expected branch callers must handle:

```ts
type Result<T, E> =
  | { readonly ok: true; readonly value: T }
  | { readonly ok: false; readonly error: E };
```

Do not introduce a repository-wide result framework for one function. Ensure callers cannot easily ignore the error branch and that async APIs do not mix arbitrary throws with undocumented result failures.

### Error classes

Use custom classes when runtime identity, codes, structured fields, or framework mapping has real value.

- Set a stable `name`/code contract if callers use it.
- Keep sensitive fields out of default formatting and serialization.
- Test subclass behavior in supported transpilation/runtime targets when relevant.
- Avoid one class per message with no behavioral distinction.
- Do not expose low-level dependency classes as public API unless intentional.

## 15. Catching and reporting errors

Caught values are uncertain:

```ts
try {
  await operation();
} catch (error: unknown) {
  // narrow, classify, translate, clean up, or rethrow
}
```

At a reporting boundary:

- Preserve the operation that failed.
- Include safe bounded identifiers.
- Distinguish expected user errors from operator failures.
- Emit once to the owning log/trace/metric path.
- Map to protocol status, CLI exit code, UI state, or retry policy deliberately.
- Avoid exposing stack traces, raw database errors, environment values, credentials, tokens, or payloads.

Never use an empty catch or `.catch(() => undefined)` unless best-effort loss is an explicit, documented contract and the failure remains observable where required.

## 16. Runtime validation design

Before adding a validator, inspect what the repository already uses. Avoid parallel schema systems without a real boundary need.

A good validator/parser:

- Accepts `unknown` or raw primitives.
- Validates structure and semantic invariants.
- Distinguishes missing, null, and invalid values.
- Applies size, count, depth, range, and normalization limits.
- Returns a validated internal type or structured error.
- Does not mutate hostile input or preserve dangerous prototypes accidentally.
- Provides safe diagnostics without echoing secrets or giant payloads.
- Has tests for valid, malformed, boundary, adversarial, and versioned cases.

Schema inference is useful only when runtime and static representations remain aligned. If code generation owns the schema, identify the source of truth and verify generated changes.

## 17. Naming and comments

- Names should expose domain intent, units, lifecycle, and whether a value is raw, parsed, validated, cached, or persisted.
- Avoid meaningless suffixes such as `Data`, `Info`, `Manager`, `Helper`, or `Service` when a precise role exists.
- Comments explain current rationale, invariants, security assumptions, compatibility constraints, and non-obvious algorithms.
- Do not narrate syntax, justify a change relative to old code, mention that code was generated by an agent, or preserve stale implementation history.
- Make TODOs actionable with the missing condition or tracking reference; do not leave vague future plans.

## Implementation completion checklist

- External uncertainty becomes a validated internal representation.
- Inference and annotations preserve useful contracts without noise.
- `unknown`, `any`, assertions, and non-null assertions are used only with deliberate evidence.
- Optionality, indexed access, and state variants reflect runtime possibilities.
- Generics and type-level computation prevent real mistakes without excessive cost.
- Public declarations remain stable and understandable.
- Errors preserve actionable classification, causes, and safe context.
- Runtime validation and tests back the static model.
- Names and comments describe the current system rather than implementation history.
