# Testing

Use for test strategy, test implementation, headless validation and regression coverage.

## Follow the existing framework

Detect GUT, GdUnit4, custom scene runners, C# test projects, native tests or CI wrappers. Do not add a framework merely to test one small change without user approval.

## Test layers

- Pure logic tests: plain GDScript/C#/native objects without a scene tree where possible.
- Resource/schema tests: definitions, migrations and validation.
- Scene tests: lifecycle, signals, input adapters and node contracts.
- Integration tests: multiple scenes/services, persistence or networking.
- Smoke tests: project import/startup and representative target scenes.
- Visual/performance tests: separate evidence with tolerances and target hardware.

Keep the majority of fast rules outside heavyweight scene setup.

## Testability design

Pass clocks, RNGs, storage and service adapters through explicit seams when behavior must be controlled. Do not globalize everything for test access. Reset autoload or static state between tests.

## Async tests

Use explicit timeouts and await observable conditions rather than arbitrary long sleeps. Ensure failed assertions still clean up nodes, peers, temp files and threads.

## Fixtures

Version save/replay/network fixtures with the schema they represent. Keep minimal test scenes purpose-built; giant production scenes make failures slow and ambiguous.

## Headless limitations

Headless checks can validate parsing, logic and many scenes, but not every rendering, audio, window, input-device, mobile, XR or platform-service behavior. State the gap.

## Suggested validation order

1. language/build check;
2. changed-unit tests;
3. changed-scene tests;
4. headless import/startup;
5. broader suite;
6. target export/device checks.

## Test quality

Assert externally meaningful state and contracts, not implementation trivia. A regression test should fail before the fix for the intended reason. Avoid snapshots of whole `.tscn` files unless exact serialization is the contract.
