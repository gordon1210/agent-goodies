# Signals, events, and state

Use for communication patterns, event buses, state machines and authoritative game state.

## Communication choice

Prefer the narrowest mechanism:

- Parent calls an owned child's method to issue a command.
- Child emits a signal to report an event to its owner.
- Siblings communicate through their common owner.
- A resource or domain object exposes typed state when no scene lifecycle is needed.
- A scoped coordinator mediates communication across independently owned scenes.
- A global bus is a last resort for genuinely process-wide events.

Signals describe something that happened. They should not become hidden commands with unclear execution order.

## Signal contracts

- Declare argument types when supported by the project version and style.
- Keep names in past tense or event-oriented where practical.
- Connect once at a stable ownership point.
- Avoid anonymous lambdas when later disconnection or stack traces matter.
- Do not emit from constructors or partial initialization states unless listeners can handle it.
- Avoid chains where one signal synchronously mutates several unrelated systems with order dependence.

## State ownership

One component owns each mutable fact. Other components read snapshots, subscribe to changes or submit commands. Avoid mirrored writable state between UI, gameplay and persistence.

For complex behavior, model states and transitions explicitly. A state machine is justified when:

- allowed transitions matter;
- enter/exit behavior exists;
- concurrent states must be ruled out;
- debugging benefits from a named current state.

A boolean is preferable when there are only two independent conditions.

## Event bus constraints

If a bus already exists:

- keep event types documented and typed;
- define publisher and subscriber lifetimes;
- clear subscriptions during tests/session resets;
- prevent global events from carrying scene-internal node references unnecessarily;
- do not add request/response flows that hide control flow.

## Save and network boundaries

Do not serialize signal connections or transient state-machine objects as the canonical save model. Persist stable state, then reconstruct listeners and derived state. In multiplayer, only the authority changes authoritative state; signals are local notifications unless explicitly replicated.
