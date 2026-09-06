# Screen contract

Screen / scene path:  
Purpose and player question:  
Version / date / status:

## Interaction

Entry trigger:  
Initial selection and focus:  
Primary action and prerequisites:  
Preview versus committed state:  
Back/cancel behavior:  
Pointer / keyboard / controller path:  
What pauses or remains active underneath:  
Focus/input ownership while opening, open, closing, hidden:  
What happens if the opening input is still held:  
Restoration target and fallback:

## Content and components

| Component | Data / stable identity | Action/event | State dimensions | Overflow and large-text behavior |
|---|---|---|---|---|
| | | | | |

## Composition

Logical coordinate frame and scale policy:  
Stable regions / expandable regions / comfort margins:  
Narrow and ultrawide adaptation:  
World/camera interaction:  
Text-safe regions and art layers:  
Layering and clipping policy:

## Motion contract

| Trigger | Semantic change time | Animated layers | End state | Interruption | Reduced motion |
|---|---|---|---|---|---|
| | | | | | |

## Data failures

Stale async result:  
Missing art / failed load:  
Unavailable action or changed cost:  
Empty state / long content / full capacity:  
Duplicate activation / teardown:

## Acceptance

| Player task / state | Expected outcome | Device / scale | Evidence path | Status |
|---|---|---|---|---|
| | | | | Not tested |

Hard blockers: unreadable required text, inaccessible essential action, wrong committed
state, leaked input, destructive ambiguity, or missing rights for shipped assets.
